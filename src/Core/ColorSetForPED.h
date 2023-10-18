#pragma once

#include <Core/DocObject.h>
#include <Core/PropertyBackLink.h>
#include <Core/PropertyBoolean.h>
#include <Core/PropertyInteger.h>
#include <Core/PropertyLink.h>
#include <Core/PropertyText.h>
#include <Core/PropertyTextList.h>

namespace Core
{
/* @brief Defines ColorSetForPED is used for overriding and sharing values and colors in PropertyEnumDescriptor and PropertyEnumWithColorDescriptor
 */
class LX_CORE_EXPORT ColorSetForPED : public Core::DocObject
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class ColorSetForPED_Factory;
    using inherited = Core::DocObject;

    PropertyTextOpt defaultDisplayName;
    PropertyInteger index;
    PropertyInteger indexDecimalPart;
    PropertyBoolean fix;  // fix has only one entry

    size_t addEntry(const Base::String& aValue, const Base::Color& color);
    bool removeEntry(size_t aIndex);
    void setEmpty();

    bool getEntry(size_t aIndex, Base::String& aEntry) const;
    bool getEntry(size_t aIndex, std::pair<Base::String, Base::Color>& aEntry) const;
    /// Returns true/index of the value in enums, false if it is not found.
    bool getIndex(const Base::String& aValue, size_t& aIndex) const;
    bool getIndexAndEntry(const Base::String& aValue, int& aIndex, Base::String& aEntry, bool onlyStrictEquality = true) const;
    std::vector<Base::String> getEntries() const;
    std::vector<std::pair<Base::String, Base::Color>> getEntriesWithColor() const;
    Base::Color getColor(size_t aIndex) const;
    size_t getSize() const;

    bool mustBeSaved() const override;

    static Core::ColorSetForPED* getByIndex(Core::CoreDocument* cdoc, int aIndex, int aIndexDecimalPart);

protected:
    ColorSetForPED();
    virtual ~ColorSetForPED();

    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;

private:
    PropertyTextList enums;
    PropertyIndexList
        colors;  // Contains colors in #AARRGGBB format. Color of value 0 (alpha is 0 too) corresponds to invalid color (no color is set).
};

DECLARE_PROPERTY_TEMPLATES(Core::ColorSetForPED, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(Core::ColorSetForPED_Factory, Core::ColorSetForPED)
}  // namespace Core