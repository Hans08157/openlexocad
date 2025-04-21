#pragma once

#include <Core/PropertyMacros.h>
#include <Core/DynamicProperty.h>
#include <Core/Property.h>
namespace Base { class AbstractWriter; }
namespace Base { class AbstractXMLReader; }

#define USE_PROPERTYMAP

constexpr const char* PropertyName = "Property";

class QFont;


namespace Core
{
class FieldData
{
public:
    FieldData(const Core::FieldData* /*fd*/){};
};
}  // namespace Core

namespace App
{
class ElementTool;
}
namespace Draw
{
}  // namespace Draw
namespace Geom
{
}


#define MUTABLE_CONTAINER(_class_) \
public: \
    static bool isMutableStatic() { return true; } \
\
public: \
    virtual bool isMutable() const { return true; }

#define IMMUTABLE_CONTAINER(_class_) \
public: \
    friend class Core::PropertyBundle<_class_>; \
\
public: \
    static bool isMutableStatic() { return false; } \
\
public: \
    virtual bool isMutable() const { return false; } \
\
public: \
    Core::PropertyBundle<_class_> getPropertyBundle() const \
    { \
        Core::PropertyBundle<_class_> dsBundle; \
        dsBundle.setPropertyValues(this); \
        return dsBundle; \
    }


namespace Core
{
class CoreDocument;
class DocObject;
class PropertyUser;

enum PropertyType
{
    Prop_None = 0,         /*!< No special property type */
    Prop_ReadOnly = 1,     /*!< Property is read-only in the editor */
    Prop_Transient = 2,    /*!< Property content won't be saved to file, but still saves name, type and status */
    Prop_Hidden = 4,       /*!< Property won't appear in the editor */
    Prop_Output = 8,       /*!< Modified property doesn't touch its parent container */
    Prop_NoRecompute = 16, /*!< Modified property doesn't touch its container for recompute */
    Prop_NoPersist = 32,   /*!< Property won't be saved to file at all */
};

class LX_CORE_EXPORT LxFieldData
{
public:
    LxFieldData(void);
    LxFieldData(const LxFieldData* fd);
    void addField(void* base, const char* fieldname, void* fieldptr);
    std::unordered_map<std::string, ptrdiff_t> m_fieldmap;
    bool fieldsAdded = false;
};



class LX_CORE_EXPORT PropertyContainer : public Base::Persistence
{
    TYPESYSTEM_HEADER();
    LX_NODE_HEADER();
    MUTABLE_CONTAINER(Core::PropertyContainer);

public:
    friend class PostInitClass;
    friend class CoreDocument;
    friend class ObjectExecutor;
    friend class Property;
    friend class ::App::ElementTool;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    PropertyContainer(void);
    // Copy constructor
    PropertyContainer(const PropertyContainer& rhs);
    virtual ~PropertyContainer(void) = default;

    /// Adds a property to the PropertyContainer. The PropertyContainer takes ownership of the property. Returns 'true' on success, 'false' on
    /// failure.
    bool addProperty(Core::Property* p, const std::string& name);
    /// Adds a property to the PropertyContainer. Returns the added property on success, '0' on failure.
    Core::Property* addProperty(Base::Type t, const std::string& name, const Core::Variant& defaultValue);
    /// Convenience method for Python bindings
    Core::PropertyUser* addPropertyUser(const std::string& name, const Core::Variant& value);
    /// Removes a property from the PropertyContainer and deletes it.
    void removeProperty(Core::Property* p, std::string pName);
    /// Removes all properties from the PropertyContainer and deletes them.
    void removeAllProperties();
    /// Returns the property with name 'name'. Returns '0' on failure
    inline Core::Property* getPropertyByName(const std::string& name) const;
    /// Returns the property with name 'name'. Returns '0' on failure
    inline Core::Property* getPropertyByName(const Base::String& name) const;
    /// get the name of a property
    virtual const char* getPropertyName(const Property* prop) const;

    /// Returns the property of type T with name 'name'. Returns 'nullptr' on failure
    template <typename T>
    T* getPropertyByName(const std::string& name) const
    {
        Core::Property* p = getPropertyByName(name);

        if (p && dynamic_cast<T*>(p))
        {
            return static_cast<T*>(p);
        }

        return nullptr;
    }

    /// Fills a PropertyMap
    void getPropertyMap(Core::PropertyMap&) const;
    /// Returns all properties of type 'type'
    std::vector<std::pair<Core::Property*, std::string> > getPropertiesAndNameByType(Base::Type type) const;
    std::vector<Core::Property*> getPropertiesByType(Base::Type type) const;
    void getLinkProperties(  std::vector<Core::Property*>& properties1,                           
                             std::vector<Core::Property*>& properties2,                           
                             std::vector<Core::Property*>& properties3) const;
    void getPropertiesByType(Base::Type type, std::vector<Core::Property*>& props) const;
    std::vector<Core::Property*> getPropertiesByTypes(const std::vector<Base::Type>& type) const;
    /// Sets a property to value
    bool setPropertyFromVariant(const std::string& name, const Core::Variant& value);

    bool setProperty(const std::string& name, int value);
    bool setProperty(const std::string& name, const std::vector<int>& value);
    bool setProperty(const std::string& name, const std::list<std::list<int>>& value);

    bool setProperty(const std::string& name, double value);
    bool setProperty(const std::string& name, const std::vector<double>& value);
    bool setProperty(const std::string& name, const std::list<std::list<double>>& value);

    bool setProperty(const std::string& name, const Geom::Pnt& value);
    bool setProperty(const std::string& name, const std::vector<Geom::Pnt>& value);
    bool setProperty(const std::string& name, const std::list<std::list<Geom::Pnt>>& value);

    bool setProperty(const std::string& name, const Geom::Vec& value);
    bool setProperty(const std::string& name, const std::list<Geom::Vec>& value);
    bool setProperty(const std::string& name, const std::list<std::list<Geom::Vec>>& value);
    
    bool setProperty(const std::string& name, const Geom::Pnt2d& value);
    bool setProperty(const std::string& name, const std::vector<Geom::Pnt2d>& value);

    bool setProperty(const std::string& name, const Geom::Trsf& value);
    bool setProperty(const std::string& name, const std::string& value);
    bool setProperty(const std::string& name, const char* value);
    bool setProperty(const std::string& name, const Base::String& value);
    // bool setProperty(const std::string& name, const std::list<std::string>& value);
    // bool setProperty(const std::string& name, const Core::Placement& value);
    bool setProperty(const std::string& name, const MD5& value);
    bool setProperty(const std::string& name, bool value);
    bool setProperty(const std::string& name, Core::DocObject* value);
    // without this method, method setProperty(const std::string& name, bool value) is called for const Core::DocObject
    bool setProperty(const std::string& name, const Core::DocObject* value);
    bool setProperty(const std::string& name, const std::unordered_set<Core::DocObject*>& value);
    bool setProperty(const std::string& name, const std::list<Core::DocObject*>& value);
    bool setProperty(const std::string& name, const QFont& value);
    bool setProperty(const std::string& name, const Draw::DrawStyle& value);
    bool setProperty(const std::string& name, const Draw::Arrowheads& value);
    bool setProperty(const std::string& name, const Geom::Dir& value);
    bool setProperty(const std::string& name, const Geom::Dir2d& value);
    bool setProperty(const std::string& name, const Base::Color& value);
    bool setProperty(const std::string& name, const Geom::Ax1& value);
    bool setProperty(const std::string& name, const Geom::Ax2& value);
    // bool setProperty(const std::string& name, const gp_Ax22d& value);
    bool setProperty(const std::string& name, const Draw::Texture2Transform& value);
    bool setProperty(const std::string& name, pBrepData& value);



    /// Is called before a property in a PropertyContainer has been changed.
    /// Checks if the change is possible - returns true if it is, otherwise returns false,
    /// Can be used to update other variables in the container according to the change being made.
    /// Beware, newValue is an optional argument - whenever you use it, make sure that this condition holds true:
    /// newValue.getType() != Core::Variant::Type::Undefined, otherwise you are checking invalid data
    virtual bool onBeforeChange(Core::Property* p, const Core::Variant& newValue = Core::Variant());
    /// Is called after a property in a PropertyContainer has been changed
    virtual void onChanged(Core::Property* p);
    /// Is called when a PropertyContainer's status is set to MarkedForDelete
    virtual void onDeleted();
    /// Is called when a PropertyContainer's status is set to New
    virtual void onNew();
    /// Is called when the Property StatusBits are changed
    virtual void onPropertyStatusBitsChanged(const Property& /*prop*/, unsigned long /*oldStatus*/) {}
    /// Saves the PropertyContainer to writer
    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& version);
    /// Restores the PropertyContainer from reader in specified version.
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    /// Sets whether notification will be propagated on changing the values of the contained properties.
    /// The old value of the flag is returned.
    bool enableNotify(const bool enable);
    /// Returns whether notification of changes to the field values in the container is propagated to its auditors.
    bool isNotifyEnabled(void) const;
    /// Sets all properties of this PropertyContainer to updated
    void touch();

    /// Returns true if the status of the PropertyContainer
    /// is set to MarkedForDelete, Deleted or DeletedFinal
    bool isDeleted() const;
    /// Returns true if the status is set to 'Deleted'
    bool isStatusDeleted() const;
    /// Returns true if the status is set to 'MarkedForDelete'
    bool isMarkedForDelete() const;
    /// Returns true if the status is set to 'MarkedForDeleteFinal'
    bool isMarkedForDeleteFinal() const;
    /// Returns true if the status is set to 'DeletedFinal'
    bool isDeletedFinal() const;
    /// Returns true if the status is set to 'New'
    bool isNew() const;
    /// Returns true if the status is set to 'Updated'
    bool isUpdated() const;
    /// Returns true if the status is set to 'Valid'
    bool isValid() const;
    /// Returns true if the status is set to 'Error'
    bool hasErrors() const;
    /// Adds arbitrary data for this key to the PropertyContainer (Used in SDK)
    void setData(const std::string& key, void* data);
    /// Returns data for this key from the PropertyContainer (Used in SDK)
    void* getData(const std::string& key, bool* ok = nullptr) const;
    /// Removes the data from the PropertyContainer (Used in SDK)
    void removeData(const std::string& key);
    /// Returns 'true' if all values in 'container' match the corresponding property in this PropertyContainer
    bool hasSameValuesAs(const PropertyContainer* container) const;
    /// Copies the property values from 'other' PropertyContainer to this PropertyContainer
    void setPropertyValues(const PropertyContainer* other);
    /// Returns the property value T with this name. If ok=true T holds a valid value.
    template <typename T>
    T getPropertyValueByName(const std::string& propertyName, bool* ok = 0) const
    {
        Core::Property* p = getPropertyByName(propertyName);
        if (p)
            return p->getVariant().getValue<T>(ok);
        else
            return Core::Variant().getValue<T>(ok);
    }

    /// Is called in enableNotify(true), at the end of this method the state of the container (object) has to be completely consistent
    /// (i.e. all properties that need to match other properties, match them) and _integrity should be set to true
    virtual void ensureIntegrity();
    /// Sets _integrity to true
    /// If you know for certain the state of the container (object) is completely consistent
    /// (i.e. all properties that need to match other properties, match them), make sure to always call this method after enableNotify(false) and do
    /// it before enableNotify(true) is called
    void integrityMaintained();
    /// Sets _integrity to false
    void integrityLost();
    /// Returns the value of _integrity
    bool checkIntegrity();


	/// Is called after a property in a PropertyContainers has been changed, it ignores notify-flag
    virtual bool onChangedDebug( Core::Property* p );

    virtual void checkAfterOnDeleted();
    

protected:
    virtual void onBeforeChangeProperty(const Property* /*prop*/) {}
    virtual void onChangedProperty(const Property* /*prop*/) {}
    
    /// Adds copy of all properties from other to this PropertyContainer
    void addPropertiesFrom(const Core::PropertyContainer* other);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API

public:
    /// Returns a map with the name of the property and its PropertyValue as a struct of the property type and the Core::Variant value.
    Core::PropertyValueMap getPropertyValueMap() const;
    /// Returns all keys and sub keys with their values of this container
    std::map<std::string, Core::Variant> getKeyValueMap() const;
    /// Sets the key in a property to value
    bool setPropertyFromKeyValue(const std::string& propertyName, const std::string& key, const Core::Variant& value);
    /// Returns all properties that were updated since the last recompute
    std::set<Core::Property*> getUpdatedProperties() const;
    /// Sets the status to 'Updated' if the old status was 'Valid'
    void setUpdated();
    void setUpdated(const Core::Property* p);
    /// Sets the status to 'Error'
    void setHasErrors();
    /// Sets the status to 'New'
    void setNew();
    /// Sets the status to 'Valid'
    void setValid();
    /// Sets the status to 'Delete'
    void setDeleted();
    /// Sets the status to 'MarkedForDelete'
    void setMarkedForDelete();
    /// Sets the status to 'MarkedForDeleteFinal'
    void setMarkedForDeleteFinal();
    /// Sets the status to 'DeleteFinal'
    void setDeleteFinal();
    /// Sets all links of this container to null.
    virtual void breakLinks();

    unsigned int getPropertyChangeStatus() const;
    unsigned int getLastPropertyChangeStatus() const;
    /// Sets the status of all properties to 'Valid'
    void setAllPropertiesValid();
    /// Copies the property values from a Core::PropertyValueMap to this PropertyContainer
    void setPropertyValues(const Core::PropertyValueMap& other);
    /// Returns the properties in the init order
    std::vector<Core::Property*> getPropertiesOrdered() const;

    virtual bool check_lx(const char* f, const char* n);

    /** @name DynamicProperty */
    //@{
    // HPK: Do not use DynamicProperty. This is for
    // testing transactions only.
    virtual Core::Property* addDynamicProperty(const char* type,
                                               const char* name = 0,
                                               const char* group = 0,
                                               const char* doc = 0,
                                               short attr = 0,
                                               bool ro = false,
                                               bool hidden = false);

#ifndef SWIG
    DynamicProperty::PropData getDynamicPropertyData(const Property* prop) const;
#endif

    virtual bool removeDynamicProperty(const char* name);
    virtual std::vector<std::string> getDynamicPropertyNames() const;
    virtual Core::Property* getDynamicPropertyByName(const char* name) const;
    //@}



    bool isRestored = false;

#ifdef USE_PROPERTYMAP

    /// Brings back the PropertyContainer to its last valid status
    bool rollBack();

    /// Saves the last valid property map, p.e. before a recompute to enable a rollback
    void saveLastValidPropertyMap();

    /// Returns the last valid PropertyValueMap
    const Core::PropertyValueMap& getLastValidPropertyMap() const;
#endif


protected:
    enum class Status
    {
        New = 1,
        Updated = 2,
        Valid = 3,
        MarkedForDelete = 4,
        MarkedForDeleteFinal,
        Deleted,
        DeletedFinal,
        Error
    };

    virtual void setStatus(Status status);
    Status getStatus() const;

    bool checkForAlreadyExistingProperty(Core::Property* property);

    /// Restores property from from reader in specified version.
    virtual void restoreProperty(Core::Property* property,
                                 const Base::String& name,
                                 Base::AbstractXMLReader& reader,
                                 Base::PersistenceVersion& version);

    
    void addChangedProperties(unsigned int propertiesflags);

private:

    unsigned int _changedProperties;
    unsigned int _lastChangedProperties;

    /// Copies the property values from a Core::PropertyValueMap to this PropertyContainer
    void _setPropertyValues(const Core::PropertyValueMap& pmap, bool isInit = false);
    /// Copies the property values from another Core::PropertyContainer to this PropertyContainer
    void _setPropertyValues(const Core::PropertyContainer* other, bool isInit = false);
    void getPropertyMapSetNotify(bool v);

    std::unordered_map<std::string, Core::Property*> _userPropertyMap;
#ifdef USE_PROPERTYMAP
    std::unordered_map<std::string, PropertyValue> _lastValidPropertyMap;
#endif
    std::unordered_map<std::string, void*> _data;
    Status _status = Status::New;
    bool _notify = true;

    /// When false the ensureIntegrity() method is called by enableNotify(true) which has been called either for the container or property contained
    /// in it False if any unauthorized changes may have happened -> is set to false every time enablenotify(false) is called either for the container
    /// or property contained in it
    bool _integrity = true;
#endif
};



class LX_CORE_EXPORT PostInitClass
{
public:
    PostInitClass(Core::PropertyContainer* p) : container(p){};
    ~PostInitClass();
    Core::PropertyContainer* container;
};

}  // namespace Core
