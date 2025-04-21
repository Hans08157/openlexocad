#pragma once

#include <Core/Property.h>


namespace Core
{
/*!
 * @brief Core::PropertyUser is a class that can hold properties defined
 * by the user. Its value member is a Core::Variant and can hold
 * arbitrary information.
 */

class LX_CORE_EXPORT PropertyUser : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    bool setValue(const Core::Variant& value);
    const Core::Variant& getValue() const;

    bool setTextValue(const Base::String& text);
    Base::String getTextValue(bool* ok = 0);

    Core::Variant getVariant() const override;
    bool setValueFromVariant(const Core::Variant& value) override { return setValue(value); }
    void copyValue(Core::Property* p) override;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    Core::Variant _value;
};

DECLARE_PROPERTY_FACTORY(PropertyUser_Factory, Core::PropertyUser);

class LX_CORE_EXPORT PropertyIfc : public Core::PropertyUser
{
    TYPESYSTEM_HEADER();
};

DECLARE_PROPERTY_FACTORY(PropertyIfc_Factory, Core::PropertyIfc);

}  // namespace Core
