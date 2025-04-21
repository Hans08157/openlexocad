#pragma once

#include <Base/Color.h>
#include <Base/Message.h>
#include <Core/PropertyUser.h>
#include <Core/Variant.h>
#include <Geom/Pnt.h>

#include <memory>
#include <string>
#include <vector>

namespace Core
{
class DocObject;
class PropertyScriptParam;
class PropertyDescriptor;
}  // namespace Core

namespace OpenLxApp
{
class DocObject;
class Document;
class ProductImpl;

class LX_OPENLXAPP_EXPORT Property
{
public:
    enum Visible
    {
        NOT_VISIBLE = 0,
        VISIBLE = 1
    };

    enum Editable
    {
        NOT_EDITABLE = 0,
        EDITABLE = 1
    };

    Core::Variant getVariant() const;
    std::string getName() const;

    bool isVisible() const;
    void setVisible(bool on);
    bool isEditable() const;
    void setEditable(bool on);

    Base::String getDisplayName() const;
    void setTranslationId(int aId);
    int getTranslationId() const;

    virtual ~Property() = default;

    /// Internal
    void __setPropertyUser__(Core::PropertyUser* aProperty);

protected:
    Property();

    bool isDocEditing() const;

    template <typename T>
    void _setValue(const T& aValue)
    {
        assert(_prop);
        
        if (isDocEditing())
        {
            _prop->setValue(Core::Variant(aValue));
        }
        else
        {
            Base::Message().showMessageBoxError(
                "Not in 'Edit Mode'",
                "You cannot set the value of a property \nif you are not in 'Edit mode'. \nCall 'Document.beginEditing()' before.");
            // throw std::logic_error("You cannot set the value of a property if you are not in 'Edit mode'. Call 'Document.beginEditing()' before.");
        }
    }

    std::shared_ptr<Document> _getDocument(Core::Property* aProp) const;
    Core::PropertyDescriptor* _getPropertyDescriptor() const;
    Core::PropertyUser* _prop = nullptr;
};

class LX_OPENLXAPP_EXPORT PropertyInteger : public Property
{
public:
    PropertyInteger();
    virtual ~PropertyInteger() {}

    int getValue() const;
    void setValue(int aValue);

    void setMinValue(int aValue);
    void setMaxValue(int aValue);
    void setSteps(int aValue);

    int getMinValue() const;
    int getMaxValue() const;
    int getSteps() const;
};

struct LX_OPENLXAPP_EXPORT PropertyEnumEntry
{
    Base::String mName;
    int mTranslationId = -1;
};

class LX_OPENLXAPP_EXPORT PropertyEnum : public PropertyInteger
{
public:
    PropertyEnum();
    virtual ~PropertyEnum() {}

    size_t addEntry(const Base::String& aValue, int aTranslationId = -1);
    bool getEntry(size_t aIndex, std::pair<Base::String, int>& aEntry);
    bool getEntry(size_t aIndex, PropertyEnumEntry& aEntry);
    bool removeEntry(size_t aIndex);
    void setEmpty();

    std::vector<PropertyEnumEntry> getPredefinedValues() const;
};

class LX_OPENLXAPP_EXPORT PropertyDouble : public Property
{
public:
    PropertyDouble();
    virtual ~PropertyDouble() {}
    double getValue() const;
    void setValue(double aValue);

    void setMinValue(double aValue);
    void setMaxValue(double aValue);
    void setSteps(double aValue);

    double getMinValue() const;
    double getMaxValue() const;
    double getSteps() const;
};

class LX_OPENLXAPP_EXPORT PropertyBool : public Property
{
public:
    enum Style
    {
        DEFAULT = 0,
        LOCKBUTTON = 1,
        // CHECKBOX = 2,
    };

    PropertyBool();
    virtual ~PropertyBool() {}
    bool getValue() const;
    void setValue(bool aValue);

    Style getStyle() const;
    void setStyle(Style aStyle);
};

class LX_OPENLXAPP_EXPORT PropertyString : public Property
{
public:
    PropertyString();
    virtual ~PropertyString() {}
    Base::String getValue() const;
    void setValue(const Base::String& aValue);
    void setValue(const std::string& aValue);
};

class LX_OPENLXAPP_EXPORT PropertyButton : public Property
{
public:
    PropertyButton();
    virtual ~PropertyButton() {}
};

class LX_OPENLXAPP_EXPORT PropertyColor : public Property
{
public:
    PropertyColor();
    virtual ~PropertyColor() {}
    Base::Color getValue() const;
    void setValue(const Base::Color& aValue);
};

class LX_OPENLXAPP_EXPORT PropertyPoint : public Property
{
public:
    PropertyPoint();
    virtual ~PropertyPoint() {}
    Geom::Pnt getValue() const;
    void setValue(const Geom::Pnt& aValue);
};

class LX_OPENLXAPP_EXPORT PropertyPointVector : public Property
{
public:
    PropertyPointVector();
    virtual ~PropertyPointVector() {}
    std::vector<Geom::Pnt> getValue() const;
    void setValue(const std::vector<Geom::Pnt>& aValue);
};

class LX_OPENLXAPP_EXPORT PropertyObject : public Property
{
public:
    PropertyObject();
    virtual ~PropertyObject() {}
    std::shared_ptr<OpenLxApp::DocObject> getValue() const;
    void setValue(std::shared_ptr<OpenLxApp::DocObject> aValue);
};

class LX_OPENLXAPP_EXPORT PropertyObjectVector : public Property
{
public:
    PropertyObjectVector();
    virtual ~PropertyObjectVector() {}
    std::vector<std::shared_ptr<OpenLxApp::DocObject>> getValue() const;
    void setValue(const std::vector<std::shared_ptr<OpenLxApp::DocObject>>& aValue);
};

/* @brief: A property defined by the Lexocad user.
 */
class LX_OPENLXAPP_EXPORT PropertyUser : public Property
{
public:
    PropertyUser();
    virtual ~PropertyUser() {}
    Core::Variant getValue() const;
    void setValue(const Core::Variant& aValue);
};
}  // namespace OpenLxApp

#define EXT_ADD_PROPERTY(_prop_, _value_) \
    { \
        Core::PropertyUser* p = new Core::PropertyUser(); \
        p->setValue(Core::Variant(_value_)); \
        _coreObj->addProperty(p, #_prop_); \
        _prop_.puser = p; \
    }