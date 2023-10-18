#pragma once
#pragma warning(disable : 4100)
#pragma warning(disable : 4005)


#include <Base/Dir.h>
#include <Base/Dir2d.h>
#include <core_defines2.h>

#include <vector>

#include "Core/Property.h"
#include "Core/Variant.h"

#pragma warning(default : 4100)
#pragma warning(default : 4005)

namespace Core
{
class CORE_EXPORT PropertyDirection : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyDirection(void);
    virtual ~PropertyDirection(void);

    void setValue(const Base::Dir& dir);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Base::Dir& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(CA_AbstractWriter& writer);

    /// Throws CA_FileException
    virtual void restore(CA_AbstractXMLReader& reader, int version);

protected:
    Base::Dir _dir;
};

class CORE_EXPORT PropertyDirection2d : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyDirection2d(void);
    virtual ~PropertyDirection2d(void);

    void setValue(const Base::Dir2d& dir);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Base::Dir2d& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(CA_AbstractWriter& writer);

    /// Throws CA_FileException
    virtual void restore(CA_AbstractXMLReader& reader, int version);

protected:
    Base::Dir2d _dir;
};

DECLARE_PROPERTY_FACTORY(PropertyDirection_Factory, Core::PropertyDirection);
DECLARE_PROPERTY_FACTORY(PropertyDirection2d_Factory, Core::PropertyDirection2d);



}  // namespace Core
