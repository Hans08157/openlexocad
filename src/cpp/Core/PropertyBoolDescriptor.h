#pragma once

#include <Core/PropertyDescriptor.h>


namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyBool
 */
class LX_CORE_EXPORT PropertyBoolDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    using inherited = Core::PropertyDescriptor;
    friend class PropertyBoolDescriptor_Factory;

    enum class Style
    {
        DEFAULT = 0,
        LOCKBUTTON = 1,
        // CHECKBOX = 2,
    };

    PropertyBoolDescriptor();

    Type getType() const override;
    Style getStyle() const;
    void setStyle(PropertyBoolDescriptor::Style aStyle);

    bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false) override;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;

private:
    PropertyInteger style;
};

DECLARE_OBJECT_FACTORY_NOIFC(PropertyBoolDescriptor_Factory, PropertyBoolDescriptor);
}  // namespace Core