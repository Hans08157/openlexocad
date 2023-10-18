#pragma once 

#include <Core/PropertyDescriptor.h>

namespace Core
{
/* @brief Saves and restore the characteristics of a group of properties
 */
class LX_CORE_EXPORT PropertyGroupDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyGroupDescriptor_Factory;
    Core::PropertyLinkList children;

    PropertyGroupDescriptor();

    virtual Type getType() const override;

    bool isRoot() const;

    size_t computeHash(bool strictComparison = false) override;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap ) override;
};

DECLARE_PROPERTY_TEMPLATES(Core::PropertyGroupDescriptor, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(PropertyGroupDescriptor_Factory, PropertyGroupDescriptor);
}  // namespace Core