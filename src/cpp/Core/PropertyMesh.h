#pragma once

#include <Geom/IndexedMesh.h>
#include <Core/Property.h>



namespace Core
{
class LX_CORE_EXPORT PropertyMesh : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::IndexedMesh& mesh);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::IndexedMesh& getValue() const;


    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::IndexedMesh _value;
};



DECLARE_PROPERTY_FACTORY(PropertyMesh_Factory, Core::PropertyMesh);


}  // namespace Core