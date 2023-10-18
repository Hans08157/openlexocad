#pragma once

#include <Base/Persistence.h>
#include <Core/PropertyValue.h>
#include <QRegExp>
#include <bitset>

namespace Base
{
class AbstractWriter;
}

//@note mondzi: _parentProp_ must be whole name with namespace
#define TYPESYSTEM_PROPERTY_HEADER(_prop_, _parentProp_) \
public: \
    static void* create() \
    { \
        return new _prop_(); \
    } \
    static void init(const char* propName) \
    { \
        initSubclass(_prop_::classTypeId, propName, #_parentProp_, &(_prop_::create)); \
    } \
    static Base::Type getClassTypeId() \
    { \
        return _prop_::classTypeId; \
    } \
    virtual Base::Type getTypeId() const \
    { \
        return _prop_::classTypeId; \
    } \
\
private: \
    static Base::Type classTypeId;


namespace App
{
class ElementTool;
}

namespace Core
{
class Property;
class PropertyContainer;
class CoreDocument;
class CoreVisitor;
class DbgInfo;
class DocObject;
typedef std::map<Core::DocObject*, Core::DocObject*> DocObjectMap;


/// The PropertyKind enum determines what a modification of
/// this property does to the object it is contained in.
/// The setting of the PropertyKind has direct influence on
/// the recompute of an object:
enum PropertyKind
{                                  // Triggers execute     Triggers Observer notification      Triggers ViewProvider update
    P_NO_MODIFICATION = 0,         // NO                   NO                                  NO
    P_MODIFY_PLACEMENT = 1 << 0,   // YES                  YES                                 YES
    P_MODIFY_LINK = 1 << 1,        // YES                  YES                                 YES
    P_MODIFY_VISIBLITY = 1 << 2,   // NO                   YES                                 YES
    P_MODIFY_SHAPE = 1 << 3,       // YES                  YES                                 YES
    P_MODIFY_APPEARANCE = 1 << 4,  // NO                   YES                                 YES
    P_MODIFY_BACKLINK = 1 << 5,    // YES                  YES                                 YES
    P_MODIFY_DATA = 1 << 6,        // YES                  YES                                 YES
                                   // DrawStyle was changed
    P_MODIFY_DRAWSTYLE = 1 << 7    // NO                   YES                                 YES
};


// This pattern is used to remove all characters not valid in XML 1.0 from text before saving.
// Without this, saved document cannot be loaded.
// (User is able to enter invalid character for example using clipboard.)
// Adopted from original here: http://stackoverflow.com/questions/4237625/removing-invalid-xml-characters-from-a-string-in-java
// -mh-2016-03-18
static QRegExp xml10TextValidityPattern = QRegExp("[^\\x0009\\r\\n\\x0020-\\xD7FF\\xE000-\\xFFFD\\xd800\\xdc00-\\xdbff\\xdfff]");

// Jaroslaw: we need to store the line endings too, but it seems that the xml reader removes all line endings so we need to encode them
static QString lexocadLineBreakMark = QString("#LecoxadLineBreak#");



class LX_CORE_EXPORT PropertyFactory
{
public:
    friend class Property;
    static std::map<std::string, PropertyFactory*> registry;

private:
    static Core::Property* create(const std::string& type);
    virtual Core::Property* createByFactory() = 0;
};


class LX_CORE_EXPORT Property : public Base::Persistence
{
    TYPESYSTEM_HEADER();
    friend class ::App::ElementTool;
    friend class DynamicProperty;

public:
    enum Status
    {
        New = 1 << 1,
        Valid = 1 << 2,
        Updated = 1 << 3
    };

    // Extended Property Status (Used for transactions)
    enum ExStatus
    {
        Touched = 0,             // touched property
        Immutable = 1,           // can't modify property
        ReadOnly = 2,            // for property editor
        Hidden = 3,              // for property editor
        Transient = 4,           // for property container save
        MaterialEdit = 5,        // to turn ON PropertyMaterial edit
        NoMaterialListEdit = 6,  // to turn OFF PropertyMaterialList edit
        Output = 7,              // same effect as Prop_Output
        LockDynamic = 8,         // prevent being removed from dynamic property
        NoModify = 9,            // prevent causing Gui::Document::setModified()
        PartialTrigger = 10,     // allow change in partial doc
        NoRecompute = 11,        // touch owner for recompute on property change
        Single = 12,             // for save/load of floating point numbers
        Ordered = 13,            // for PropertyLists whether the order of the elements is
                                 // relevant for the container using it
        EvalOnRestore = 14,      // In case of expression binding, evaluate the
                                 // expression on restore and touch the object on value change.

        // The following bits are corresponding to PropertyType set when the
        // property added. These types are meant to be static, and cannot be
        // changed in runtime. It is mirrored here to save the linear search
        // required in PropertyContainer::getPropertyType()
        //
        PropStaticBegin = 21,
        PropDynamic = 21,      // indicating the property is dynamically added
        PropNoPersist = 22,    // corresponding to Prop_NoPersist
        PropNoRecompute = 23,  // corresponding to Prop_NoRecompute
        PropReadOnly = 24,     // corresponding to Prop_ReadOnly
        PropTransient = 25,    // corresponding to Prop_Transient
        PropHidden = 26,       // corresponding to Prop_Hidden
        PropOutput = 27,       // corresponding to Prop_Output
        PropStaticEnd = 28,

        User1 = 28,  // user-defined status
        User2 = 29,  // user-defined status
        User3 = 30,  // user-defined status
        User4 = 31   // user-defined status
    };

    Property();
    virtual ~Property() = default;

    // inline void setName(const std::string& name);  //@warning: does nothing
    inline std::string getName() const;

    Core::PropertyContainer* getContainer() const;
    void setContainer(Core::PropertyContainer* container);
    void addToContainer(const std::string& name);

    virtual Core::Variant getVariant() const = 0;
    virtual bool setValueFromVariant(const Core::Variant& value) = 0;
    /// Returns a new copy of the property (mainly for Undo/Redo and transactions). The copy has no container.
    virtual Property* copy() const = 0;
    /// Paste the value from the property (mainly for Undo/Redo and transactions)
    virtual void paste(const Property& from) = 0;

    /// Sets a sub key in this property
    virtual bool setKeyValue(const std::string& key, const Core::Variant& value);
    /// Returns all keys  and their values of this property
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;
    /// Gets the variant for a key
    Core::Variant getVariantFromKey(const std::string& key) const;
    /// Returns all keys of this property
    std::vector<std::string> getKeys() const;

    virtual void copyValue(Core::Property* p) = 0;
    virtual void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap);

    /// Controls whether to call container's aboutToSetValue() and hasSetValue(), if the parameter is false the integrity of the container is lost,
    /// when the parameter is true and the integrity isn't intact ensureIntegrity is called to resolve this
    inline bool enableNotify(bool on);
    inline bool isNotifyEnabled() const;
    /// Simulates the value being changed - calls aboutToSetValue() and hasSetValue(), aboutToSetValue() is called without the optional argument
    /// Core::Variant &newValue,
    /// - more info at the PropertyContainer's onBeforeChange() method
    inline void touch();

    // True; Default, hasSetValue() will change Status to Core::PropertyContainer::Updated
    // False: The Status of the Container will not changed, useful to store information
    inline bool setWillChangeStatusOnChange(bool on);

    inline long getTransactionNumber() const;

    /// Checks if the property was updated
    bool isUpdated() const;
    /// Checks if this is the only updated property in the container
    // bool isTheOnlyUpdatedPropertyInContainer() const;

    virtual const Core::PropertyKind getPropertyKind() const;
    virtual void setPropertyKind(Core::PropertyKind p);

    /// Returns 'true' if the property has a value. This is mainly for optional properties
    bool hasValue() const;
    /// Checks if this is an optional property
    virtual bool isOptional() const { return false; }
    /// is called when a property holds a value. For optional properties.
    void setHasValue(bool yes);
    /// compare properties
    virtual bool isEqual(const Property*) const = 0;
    /// Check if Property is of type PropertyLink, LinkSet etc. for better performance
    virtual bool isLink() const { return false; }
    /// Returns the debug information for this property
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const;

    /** @name StatusBits*/
    //@{
    inline unsigned long getExStatus() const { return StatusBits.to_ulong(); }
    inline bool testExStatus(ExStatus pos) const { return StatusBits.test(static_cast<size_t>(pos)); }
    void setExStatus(ExStatus pos, bool on);
    void setExStatusValue(unsigned long status);
    //@}

    inline void setStatus(const Property::Status& in);
    inline Property::Status getStatus() const;
    inline bool isDefaultValue() const;
    inline void setDefaultValue(bool on);

    /// Registers the properties with default values for type 't'
    static void registerProperties(Base::Type t, const Core::PropertyValueMap& pvm);
    /// Returns the properties with default values of type t;
    static bool getRegisteredProperties(Base::Type t, Core::PropertyValueMap& pvm);
    static const char* getXMLPropertyAttributeName();
    static const char* getXMLPropertyAttributeValue();

    void accept(Core::CoreVisitor* visitor);

    bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;

    /// Get the type of the property in the container
    short getType() const;

protected:
    /// Should be called by all setValue() methods after the value was changed
    void hasSetValue();
    /// Should be called by all setValue() methods before the value is changed, returns true if the change is validated by container (false
    /// otherwise), so far only properties (and only their setValue() methods, copyValue() doesn't use it) in the following files use the container
    /// validation functionality: PropertyReal, PropertyInteger, PropertyBoolean, PropertyDrawStyle
    bool aboutToSetValue(const Core::Variant& newValue = Core::Variant());

    /** Status bits of the property
     * The first 8 bits are used for the base system the rest can be used in
     * descendant classes to mark special statuses on the objects.
     * The bits and their meaning are listed below:
     * 0 - object is marked as 'touched'
     * 1 - object is marked as 'immutable'
     * 2 - object is marked as 'read-only' (for property editor)
     * 3 - object is marked as 'hidden' (for property editor)
     */
    std::bitset<32> StatusBits;

private:
    // Sync status with Property_Type
    void syncType(unsigned type);
    bool isPerformingTransaction();

    long _transactionNumber = 0;
    Core::PropertyContainer* _container = nullptr;

    unsigned char _pstate;
    unsigned char _propertyKind;
    unsigned char _status;

    // Registry for each type with a map of their propertyNames/propertyTypes/defaultValues
    static std::map<Base::Type, Core::PropertyValueMap> propertyRegistry;
};
}  // namespace Core

using DocObjectMap = Core::DocObjectMap;

//----------------------------------------------------------------------------
// Macros
//----------------------------------------------------------------------------

// Add property macro
#define __ADD_PROPERTY(_prop_, _defaultval_, _propertyKind_) \
    do \
    { \
        assert(!this->_prop_.isOptional() && "Don't set a default value for an optional property!"); \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        this->_prop_.addToContainer(#_prop_); \
        this->_prop_.setValue(_defaultval_); \
        this->_prop_.setHasValue(true); \
        this->_prop_.enableNotify(true); \
        this->_prop_.setStatus(Core::Property::New); \
        this->_prop_.setDefaultValue(true); \
        this->_prop_.setPropertyKind(_propertyKind_); \
    } while (0)

#define LX_ADD_PROPERTY(_prop_, _defaultval_, _propertyKind_) \
    do \
    { \
        assert(!this->_prop_.isOptional() && "Don't set a default value for an optional property!"); \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        /* this->_prop_.addToContainer(#_prop_);*/ \
        this->_prop_.setValue(_defaultval_); \
        this->_prop_.setHasValue(true); \
        this->_prop_.enableNotify(true); \
        this->_prop_.setStatus(Core::Property::New); \
        this->_prop_.setDefaultValue(true); \
        this->_prop_.setPropertyKind(_propertyKind_); \
        this->fieldData->addField((Core::PropertyContainer*)this, #_prop_, (Core::Property*)&this->_prop_); \
    } while (0)

// Add optional property macro
#define __ADD_PROPERTY_OPT(_prop_, _propertyKind_) \
    do \
    { \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        this->_prop_.addToContainer(#_prop_); \
        this->_prop_.enableNotify(true); \
        this->_prop_.setPropertyKind(_propertyKind_); \
        this->_prop_.setHasValue(false); \
    } while (0)

#define LX_ADD_PROPERTY_OPT(_prop_, _propertyKind_) \
    do \
    { \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        /*this->_prop_.addToContainer(#_prop_);*/ \
        this->_prop_.enableNotify(true); \
        this->_prop_.setPropertyKind(_propertyKind_); \
        this->_prop_.setHasValue(false); \
        this->fieldData->addField(this, #_prop_, &this->_prop_); \
    } while (0)

// Add property without initializing value macro
#define __ADD_PROPERTY_EMPTY(_prop_, _propertyKind_) \
    do \
    { \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        this->_prop_.addToContainer(#_prop_); \
        this->_prop_.enableNotify(true); \
        this->_prop_.setStatus(Core::Property::New); \
        this->_prop_.setPropertyKind(_propertyKind_); \
        this->_prop_.setHasValue(false); \
    } while (0)

#define LX_ADD_PROPERTY_EMPTY(_prop_, _propertyKind_) \
    do \
    { \
        this->_prop_.enableNotify(false); \
        this->_prop_.setContainer(this); \
        this->_prop_.enableNotify(true); \
        this->_prop_.setStatus(Core::Property::New); \
        this->_prop_.setPropertyKind(_propertyKind_); \
        this->_prop_.setHasValue(false); \
        this->fieldData->addField(this, #_prop_, &this->_prop_); \
    } while (0)



#define DECLARE_PROPERTY_FACTORY(_factoryName_, _property_) \
    class _factoryName_ : public Core::PropertyFactory \
    { \
    private: \
        virtual Core::Property* createByFactory() \
        { \
            Core::Property* p = new _property_; \
            return p; \
        } \
    };

#define REGISTER_PROPERTY_FACTORY(_factoryName_, _property_) \
    Core::PropertyFactory::registry[#_property_] = (Core::PropertyFactory*)new _factoryName_();

#define DECLARE_OPTIONAL_PROPERTY_HEADER(_class_, _parentclass_) \
    class LX_CORE_EXPORT _class_ : public _parentclass_ \
    { \
        TYPESYSTEM_HEADER(); \
\
    public: \
        void copyValue(Core::Property* p) override; \
        void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version); \
        void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version); \
        bool isOptional() const \
        { \
            return true; \
        } \
    };

#define DECLARE_OPTIONAL_PROPERTY_SOURCE(_class_, _parentclass_) \
    void _class_::copyValue(Core::Property* p) \
    { \
        if (p->hasValue()) \
        { \
            _parentclass_::copyValue(p); \
        } \
    } \
    void _class_::save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) \
    { \
        if (hasValue()) \
        { \
            writer << "<Opt hasValue=\"" \
                   << "true" \
                   << "\"/>"; \
            _parentclass_::save(writer, save_version); \
        } \
        else \
        { \
            writer << "<Opt hasValue=\"" \
                   << "false" \
                   << "\"/>"; \
        } \
    } \
    void _class_::restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) \
    { \
        reader.readElement("Opt"); \
        Base::String s = reader.getAttribute(L"hasValue"); \
        s = Base::StringTool::toUpper(s); \
        if (s == L"TRUE") \
            setHasValue(true); \
        else \
            setHasValue(false); \
        if (hasValue()) \
        { \
            _parentclass_::restore(reader, version); \
        } \
    }



/**
 * @brief DECL_PROPERTY and DEFINE_PROPERTY are macros used for
 *        accessing the properties via a getter and setter method.
 *
 * @author   HPK
 * @since    24.0
 */
#define DECL_PROPERTY_ACCESS(_name_, _type_) \
public: \
    _type_ get##_name_() const; \
\
public: \
    void set##_name_(const _type_& aValue);

#define DEFINE_PROPERTY_ACCESS(_class_, _name_, _propname_, _type_) \
    _type_ _class_::get##_name_() const \
    { \
        return _propname_.getValue(); \
    } \
    void _class_::set##_name_(const _type_& aValue) \
    { \
        _propname_.setValue(aValue); \
    }
