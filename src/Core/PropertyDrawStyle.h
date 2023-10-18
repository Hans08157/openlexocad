#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyDrawStyle : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::DrawStyle& ds);
    bool setValueFromVariant(const Core::Variant& value);
    virtual bool setKeyValue(const std::string& name, const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::DrawStyle& getValue() const;
    Core::Variant getVariant(void) const;

    /// Returns all keys  and their values of this property
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Draw::DrawStyle _drawstyle;
};

DECLARE_PROPERTY_FACTORY(PropertyDrawStyle_Factory, Core::PropertyDrawStyle);

//////////////////////////////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyArrowheads : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::Arrowheads& value);
    bool setValueFromVariant(const Core::Variant& value);
    virtual bool setKeyValue(const std::string& name, const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::Arrowheads& getValue() const;
    Core::Variant getVariant(void) const;
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Draw::Arrowheads _arrowHeads;
};

DECLARE_PROPERTY_FACTORY(PropertyArrowheads_Factory, Core::PropertyArrowheads);
}  // namespace Core