#pragma once 

#include <Core/Property.h>


namespace Core
{
/* @brief A defined type of simple type logical.
 * Logical datatype can have values TRUE, FALSE or UNKNOWN.
 */

// TODO: add 'UNKNOWN' value
class LX_CORE_EXPORT PropertyBoolean : public Core::Property
{
    TYPESYSTEM_HEADER();

public:

    inline void setValue(bool b);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    bool getValue() const;
    Core::Variant getVariant() const override;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    Core::Property* copy(void) const override;
    void paste(const Core::Property& from) override;

protected:
    bool _nValue = false;
};

DECLARE_PROPERTY_FACTORY(PropertyLogical_Factory, Core::PropertyBoolean);

}  // namespace Core
