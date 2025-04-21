#pragma once

#include <Core/Property.h>

class QFont;

namespace Core
{
class LX_CORE_EXPORT PropertyFont : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyFont(void);
    PropertyFont(const PropertyFont& o);
    ~PropertyFont();
    PropertyFont& operator=(const PropertyFont& o);

    void setValue(const QFont& font);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const QFont& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::unique_ptr<QFont> _M_impl;
};


DECLARE_PROPERTY_FACTORY(PropertyFont_Factory, Core::PropertyFont);


}  // namespace Core