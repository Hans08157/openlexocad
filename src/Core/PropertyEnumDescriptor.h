#pragma once

#include <Core/PropertyDescriptor.h>
#include <Core/PropertyLinkMap.h>

namespace Core
{
/* @brief Saves and restores the characteristics of a PropertyEnum
 */
class LX_CORE_EXPORT PropertyEnumDescriptor : public Core::PropertyDescriptor
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PropertyEnumDescriptor_Factory;
    using inherited = Core::PropertyDescriptor;

    struct CustomTranslation
    {
        Base::String en;
        Base::String fr;
        Base::String it;

        bool operator==(const CustomTranslation& other) const { return en == other.en && fr == other.fr && it == other.it; }
        bool allEmpty() const { return en.empty() && fr.empty() && it.empty(); }
    };

    PropertyBoolean fix;  // fix has only one entry
    PropertyInteger defaultValueIndex;

    // "geom. limit" that determines the value
    PropertyText automaticValueUnit;
    PropertyText automaticValueDetail;
    PropertyReal automaticValueFactor;
    PropertyRealList automaticValueLimits;

    virtual size_t addEntry(const Base::String& aValue, int aTranslationId, const Base::String& code = Base::String());
    virtual size_t addEntry(const Base::String& aValue, const CustomTranslation& ct, const Base::String& code = Base::String());
    bool getEntry(size_t aIndex, std::pair<Base::String, int>& aEntry) const;
    bool getEntry(size_t aIndex, std::pair<Base::String, int>& aEntry, CustomTranslation& ct) const;
    bool getEntry(size_t aIndex, std::tuple<Base::String, int, CustomTranslation, Base::String>& aEntry) const;
    bool getTranslatedEntry(size_t aIndex, Base::String& aValueTr) const;
    virtual bool removeEntry(size_t aIndex);
    std::vector<std::pair<Base::String, int>> getEntries() const;
    std::vector<std::tuple<Base::String, int, CustomTranslation>> getEntriesWithCT() const;
    std::vector<std::tuple<Base::String, int, CustomTranslation, Base::String>> getEntriesWithCTAndCode() const;
    std::vector<Base::String> getTranslatedEntries() const;
    virtual void setEmpty();
    virtual void copyEntriesFrom(PropertyEnumDescriptor* other);
    /// Returns true/index of the value in enums, false if it is not found.
    bool getIndex(const Base::String& aValue, size_t& aIndex) const;
    Base::String getCode(size_t aIndex) const;
    /// Returns true for the properties from Lcc data with 'o' code
    bool isNPKOpenPosition(size_t aIndex) const;
    /// Sets enums and codes for the user-defined entries.
    void setUserDefinedEntries(const std::vector<std::tuple<Base::String, Base::String>>& entries);
    /// Returns enums and codes for the user-defined entries.
    std::vector<std::tuple<Base::String, Base::String>> getUserDefinedEntries() const;

    PropertyEnumDescriptor();

    Type getType() const override;
    bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false) override;
    size_t getSize() const;

    size_t computeHash(bool strictComparison) override;
    long getEnumsTransactionNumber() const { return enums.getTransactionNumber(); }

    Core::GeometryLimit* getGeometryLimit(const Base::String& propertyValue = L"") const override;

    bool hasEnumGeometryLimits() const;
    void setEnumGeometryLimits(const std::map<int, DocObject*>& egls);
    const std::map<int, DocObject*>& getEnumGeometryLimits() const;

    bool hasEnumGeometryLimit(Core::GeometryLimit* gl, int& idx) const;
    void addEnumGeometryLimit(int idx, Core::GeometryLimit* gl);
    bool removeEnumGeometryLimit(Core::GeometryLimit* gl);

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;
    void restoreProperty(Core::Property* property,
                         const Base::String& name,
                         Base::AbstractXMLReader& reader,
                         Base::PersistenceVersion& version) override;

private:
    PropertyTextList enums;
    PropertyIndexList translationIds;
    PropertyTextListOpt enumsEn;
    PropertyTextListOpt enumsFr;
    PropertyTextListOpt enumsIt;
    PropertyTextListOpt codes;                // "code" (text) for each enum value
    PropertyTextList userDefinedEnums;        // remember which entries are user-defined
    PropertyLinkMap<int> enumGeometryLimits;  // limit for each enum value, key is index of enum
};

DECLARE_PROPERTY_TEMPLATES(Core::PropertyEnumDescriptor, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(PropertyEnumDescriptor_Factory, PropertyEnumDescriptor);
}  // namespace Core