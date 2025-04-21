#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyCompoundPlaneAngle : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::CompoundPlaneAngle& value);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::CompoundPlaneAngle& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::CompoundPlaneAngle _value;
};



DECLARE_PROPERTY_FACTORY(PropertyCompoundPlaneAngle_Factory, Core::PropertyCompoundPlaneAngle);
DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyCompoundPlaneAngleOpt, Core::PropertyCompoundPlaneAngle);



}  // namespace Core
