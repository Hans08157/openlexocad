#pragma once 

#include <Core/PropertyDescriptor.h>

namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyInteger
 */
class LX_CORE_EXPORT PropertyIntegerDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    using inherited = Core::PropertyDescriptor;
    friend class PropertyIntegerDescriptor_Factory;

    PropertyInteger minValue;
    PropertyInteger maxValue;
    PropertyInteger steps;
    PropertyEnum quantity;

    PropertyIntegerDescriptor();

    Type getType() const override;

    bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false) override;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyIntegerDescriptor_Factory, PropertyIntegerDescriptor);
}  // namespace Core