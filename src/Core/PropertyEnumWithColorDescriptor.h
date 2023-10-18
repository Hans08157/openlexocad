#pragma once

#include <Core/ColorSetForPED.h>
#include <Core/PropertyEnumDescriptor.h>

namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyEnum with additional color information
 */
class LX_CORE_EXPORT PropertyEnumWithColorDescriptor : public Core::PropertyEnumDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyEnumWithColorDescriptor_Factory;
    using inherited = Core::PropertyEnumDescriptor;

    Core::PropertyLink<Core::ColorSetForPED*> colorSetForPED;

    size_t addEntry(const Base::String& aValue, int aTranslationId, const Base::String& code = Base::String()) override;
    size_t addEntry(const Base::String& aValue, const CustomTranslation& ct, const Base::String& code = Base::String()) override;
    size_t addEntry(const Base::String& aValue, int aTranslationId, const Base::Color& color, const Base::String& code = Base::String());
    size_t addEntry(const Base::String& aValue, const CustomTranslation& ct, const Base::Color& color, const Base::String& code = Base::String());
    bool removeEntry(size_t aIndex) override;
    void setEmpty() override;
    void copyEntriesFrom(PropertyEnumDescriptor* other) override;

    bool getEntry(size_t aIndex, std::tuple<Base::String, int, Base::Color>& aEntry) const;
    bool getEntry(size_t aIndex, std::tuple<Base::String, int, Base::Color, CustomTranslation, Base::String>& aEntry) const;
    std::vector<std::tuple<Base::String, int, Base::Color>> getEntriesWithColor() const;
    std::vector<std::tuple<Base::String, int, Base::Color, CustomTranslation, Base::String>> getEntriesWithColorCTAndCode() const;
    Base::Color getColor(size_t aIndex) const;

    PropertyEnumWithColorDescriptor();
protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;

private:
    PropertyIndexList
        colors;  // Contains colors in #AARRGGBB format. Color of value 0 (aplha is 0 too) corresponds to invalid color (no color is set).
};

DECLARE_PROPERTY_TEMPLATES(Core::PropertyEnumWithColorDescriptor, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(PropertyEnumWithColorDescriptor_Factory, PropertyEnumWithColorDescriptor);
}  // namespace Core