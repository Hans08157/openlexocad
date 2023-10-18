#pragma once

#include <Core/PropertyDescriptor.h>


namespace Core
{
/* @brief Saves and restores the visual layout of a PropertyButton
 */
class LX_CORE_EXPORT PropertyButtonDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyButtonDescriptor_Factory;

    PropertyButtonDescriptor();

    Type getType() const override;

private:
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyButtonDescriptor_Factory, PropertyButtonDescriptor);
}  // namespace Core