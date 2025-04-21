#pragma once 

#include <Core/Property.h>

namespace Core
{
struct SearchValue
{
    QString name;
    QString value;
};

class LX_CORE_EXPORT PropertySearchSettings : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<std::vector<SearchValue>>& setting);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const std::vector<std::vector<SearchValue>>& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<std::vector<SearchValue>> _settings;
};

class LX_CORE_EXPORT PropertySearchSettingsVector : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<std::vector<std::vector<SearchValue>>>& setting);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const std::vector<std::vector<std::vector<SearchValue>>>& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<std::vector<std::vector<SearchValue>>> _settings;
};

DECLARE_PROPERTY_FACTORY(PropertySearchSettings_Factory, Core::PropertySearchSettings);
DECLARE_PROPERTY_FACTORY(PropertySearchSettingsVector_Factory, Core::PropertySearchSettingsVector);



}  // namespace Core
