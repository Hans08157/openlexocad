#pragma once 

#include <Core/Property.h>


namespace Core
{
/*@brief
 * A  PropertyProxy serves as a placeholder for another property (usually in another class).
 * It is used to mimic the Properties update mechanism even if the class it is used in does
 * not have a property of this king.
 * P.e. it can be used in an Element to do as if it would have a PropertyShape. This way
 * the updating of shapes can be more easily handled in App.Element.
 */

class LX_CORE_EXPORT PropertyProxy : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    inline void setValue(bool b);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    bool getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    bool _nValue = false;
};

DECLARE_PROPERTY_FACTORY(PropertyProxy_Factory, Core::PropertyProxy);

}  // namespace Core
