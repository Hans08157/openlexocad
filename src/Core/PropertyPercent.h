#pragma once 

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyPercent : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(int i);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    int getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    int _nValue = 0;
};

DECLARE_PROPERTY_FACTORY(PropertyPercent_Factory, Core::PropertyPercent);

}  // namespace Core
