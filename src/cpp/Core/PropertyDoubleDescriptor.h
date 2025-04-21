#pragma once

#include <Core/PropertyDescriptor.h>

namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyDouble
 */
class LX_CORE_EXPORT PropertyDoubleDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    using inherited = Core::PropertyDescriptor;
    friend class PropertyDoubleDescriptor_Factory;

    PropertyLength minValue;
    PropertyLength maxValue;
    PropertyLength steps;
    PropertyEnum quantity;

    PropertyDoubleDescriptor();
    Type getType() const override;

    bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false) override;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyDoubleDescriptor_Factory, PropertyDoubleDescriptor);
}  // namespace Core