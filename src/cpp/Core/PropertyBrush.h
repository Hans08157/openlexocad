#pragma once

#include <Core/Property.h>

class QBrush;

namespace Core
{
class LX_CORE_EXPORT PropertyBrush : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyBrush();
    ~PropertyBrush();

    void setValue(const QBrush& brush);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const QBrush& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::unique_ptr<QBrush> _pimpl;
};

DECLARE_PROPERTY_FACTORY(PropertyBrush_Factory, Core::PropertyBrush);


}  // namespace Core
