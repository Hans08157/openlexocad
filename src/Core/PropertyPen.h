#pragma once 

#include <Core/Property.h>
#include <QPen>

namespace Core
{
class LX_CORE_EXPORT PropertyPen : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const QPen& pen);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const QPen& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    QPen _pen;
};

DECLARE_PROPERTY_FACTORY(PropertyPen_Factory, Core::PropertyPen);


}  // namespace Core
