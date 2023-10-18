#pragma once 

#include <Core/Property.h>

class TopoDS_Face;

namespace Core
{
class LX_CORE_EXPORT PropertyFace : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(const TopoDS_Face& face) = 0;
    virtual bool setValueFromVariant(const Core::Variant& value) = 0;

    virtual void copyValue(Core::Property* p) = 0;

    virtual const TopoDS_Face& getValue() const = 0;
    virtual Core::Variant getVariant(void) const = 0;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) = 0;
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) = 0;
    virtual bool isEqual(const Property*) const;

protected:
};

}  // namespace Core
