#pragma once

#include <Core/PropertyDescriptor.h>


namespace Core
{
/* @brief Saves and restore the characteristics of a LxAttribute
 */
class LX_CORE_EXPORT PropertyLxAttributeDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyLxAttributeDescriptor_Factory;

    PropertyLxAttributeDescriptor();
    Type getType() const override;

private:
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyLxAttributeDescriptor_Factory, PropertyLxAttributeDescriptor);
}  // namespace Core