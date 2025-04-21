#pragma once

#include <Core/GeometryLimit.h>

namespace Core
{
/**
 *User-defined geometry limits for PropertyDecriptor.
 */
class LX_CORE_EXPORT GeometryLimitUser : public Core::GeometryLimit
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
    using inherited = Core::GeometryLimit;

public:
    friend class GeometryLimitUser_Factory;

    PropertyText customText;

    QString getKeyText(bool first = true) const override;

protected:
    GeometryLimitUser();
    virtual ~GeometryLimitUser();

    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;
};

DECLARE_PROPERTY_TEMPLATES(Core::GeometryLimitUser, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(Core::GeometryLimitUser_Factory, Core::GeometryLimitUser)
}  // namespace Core
