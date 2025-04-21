#pragma once

#include <Core/PropertyDescriptor.h>


namespace Core
{
/* @brief Saves and restore the characteristics of a LxFormula
 */
class LX_CORE_EXPORT PropertyLxFormulaDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    using inherited = Core::PropertyDescriptor;
    friend class PropertyLxFormulaDescriptor_Factory;

    Core::PropertyText formula;
    Core::PropertyRealList numsInFormula;
    Core::PropertyBackLinkSet<Core::PropertyDescriptor*> propsInFormula;

    PropertyLxFormulaDescriptor();

    Type getType() const override;

    bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false) override;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyLxFormulaDescriptor_Factory, PropertyLxFormulaDescriptor);
}  // namespace Core