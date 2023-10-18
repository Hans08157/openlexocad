#pragma once 

#include <Core/Property.h>
#include <sstream>

namespace Core
{
class LX_CORE_EXPORT PropertyFile : public Core::Property
{
    TYPESYSTEM_HEADER();

public:

    void setValue(const Base::String& filepath);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Base::String& getValue() const;

    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Base::String _filepath;
    std::stringstream _memstream;
};



DECLARE_PROPERTY_FACTORY(PropertyFile_Factory, Core::PropertyFile);


}  // namespace Core