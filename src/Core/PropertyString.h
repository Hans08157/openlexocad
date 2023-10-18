#pragma once 

#include <Core/Property.h>

namespace Core
{

class LX_CORE_EXPORT PropertyString : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    bool setValue(const Base::String& text);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const Base::String& getValue() const;
    Core::Variant getVariant() const override;

    bool isEmpty() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    Base::String _text;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyStringOpt, Core::PropertyString);
DECLARE_PROPERTY_FACTORY(PropertyString_Factory, Core::PropertyString);



}  // namespace Core
