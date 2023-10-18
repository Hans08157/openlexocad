#pragma once 

#include <Core/PropertyDescriptor.h>


namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyString
 */
class LX_CORE_EXPORT PropertyStringDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyStringDescriptor_Factory;

    PropertyStringDescriptor();

    PropertyText defaultValue;
    PropertyText fixedCode;

    Type getType() const override;

private:
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyStringDescriptor_Factory, PropertyStringDescriptor);
}  // namespace Core