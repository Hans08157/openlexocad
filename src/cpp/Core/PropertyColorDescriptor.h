#pragma once

#include <Core/PropertyDescriptor.h>

namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyColor
 */
class LX_CORE_EXPORT PropertyColorDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyColorDescriptor_Factory;

    PropertyColorDescriptor();

    Type getType() const override;

private:
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyColorDescriptor_Factory, PropertyColorDescriptor);
}  // namespace Core