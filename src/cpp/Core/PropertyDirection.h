#pragma once

#include <Core/Property.h>


namespace Core
{
class LX_CORE_EXPORT PropertyDirection : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Dir& dir);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Dir& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Dir _dir;
};

class LX_CORE_EXPORT PropertyDirection2d : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Dir2d& dir);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Dir2d& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Dir2d _dir;
};

DECLARE_PROPERTY_FACTORY(PropertyDirection_Factory, Core::PropertyDirection);
DECLARE_PROPERTY_FACTORY(PropertyDirection2d_Factory, Core::PropertyDirection2d);



}  // namespace Core
