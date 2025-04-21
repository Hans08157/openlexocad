#pragma once 

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyMultiLineText : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Base::String& text);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const Base::String& getValue() const;
    Core::Variant getVariant() const override;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    Base::String _text;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyMultiLineTextOpt, Core::PropertyMultiLineText)

DECLARE_PROPERTY_FACTORY(PropertyMultiLineText_Factory, Core::PropertyMultiLineText);

}  // namespace Core
