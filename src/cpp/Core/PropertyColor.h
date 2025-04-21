#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyColor : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Base::Color& c);
    void setValue(int r, int g, int b);
    bool setValueFromVariant(const Core::Variant& value);

    /// Possible values: "r" (int) , "g" (int) , "b" (int)
    virtual bool setKeyValue(const std::string& name, const Core::Variant& value);
    /// Returns all keys  and their values of this property
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;

    void copyValue(Core::Property* p);

    const Base::Color& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Base::Color _cValue{0, 0, 0};
};

class LX_CORE_EXPORT PropertyColorList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<Base::MColor>& clist);
    void setValue(const std::vector<Base::Color>& clist);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addColor(const Base::MColor& c);
    void setEmpty();
    bool isEmpty() const;

    const std::vector<Base::MColor>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_colorList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<Base::MColor> _colorList;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyColorOpt, Core::PropertyColor);
DECLARE_PROPERTY_FACTORY(PropertyColor_Factory, Core::PropertyColor);
DECLARE_PROPERTY_FACTORY(PropertyColorOpt_Factory, Core::PropertyColorOpt);
DECLARE_PROPERTY_FACTORY(PropertyColorList_Factory, Core::PropertyColorList);

}  // namespace Core
