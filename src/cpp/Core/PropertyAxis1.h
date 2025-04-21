#pragma once

#include <Core/Property.h>
namespace Base { class AbstractWriter; }
namespace Base { class AbstractXMLReader; }
namespace Core { class CoreDocument; }

namespace Core
{
class LX_CORE_EXPORT PropertyAxis1 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyAxis1(void);

    void setValue(const Geom::Ax1& ax1);
    bool setValueFromVariant(const Core::Variant& value);    

    void setLocation(const Geom::Pnt& loc);
    void setDirection(const Geom::Dir& dir);

    void copyValue(Core::Property* p);

    const Geom::Ax1& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Ax1 _ax1;
};

class LX_CORE_EXPORT PropertyAxis2D : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyAxis2D(void);

    void setValue(const Geom::Ax2d& ax);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Ax2d& getValue() const;
    Core::Variant getVariant(void) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Ax2d _ax;
};


DECLARE_PROPERTY_FACTORY(PropertyAxis1_Factory, Core::PropertyAxis1);
DECLARE_PROPERTY_FACTORY(PropertyAxis2D_Factory, PropertyAxis2D);

}  // namespace Core
