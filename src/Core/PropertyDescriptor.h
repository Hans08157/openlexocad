#pragma once

#include <Core/GeometryLimit.h>
#include <Core/PropertyBoolean.h>

namespace Core
{
/* @brief Saves and restore the characteristics of a Property
 */
class LX_CORE_EXPORT PropertyDescriptor : public Core::DocObject
{
    using inherited = Core::DocObject;

    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    enum Type
    {
        UNDEFINED,
        INTEGER,
        DOUBLE,
        BOOL,
        STRING,
        ENUM,
        BUTTON,
        COLOR,
        POINT,
        OBJECT,
        GROUP,
        LXATTRIBUTE,
        LXFORMULA,
    };

    enum struct LxzType : int
    {
        NotLxz = 0,
        Lxz_eBKP = 101,
        Lxz_4D = 102,
        Lxz_NPK = 103,
    };

    enum struct UserPropertiesLxPrefixMode : int
    {
        Mix = 0,
        Show = 1,
        Hide = 2,
    };

    PropertyText parameterName;
    PropertyTextOpt defaultDisplayName;
    PropertyTextOpt defaultDisplayNameEn;
    PropertyTextOpt defaultDisplayNameFr;
    PropertyTextOpt defaultDisplayNameIt;

    PropertyBoolean isVisible;
    PropertyBoolean isEditable;
    PropertyInteger translationId;
    PropertyInteger index;
    PropertyInteger indexDecimalPart;
    PropertyText guid;
    PropertyTextOpt ifcPropertyName;

    PropertyText entryType;
    PropertyText unit;
    PropertyTextList details;
    PropertyBoolean negative;
    PropertyBoolean forPropertySetInfo;  // all properties for PropertySetInfo should have unique name
    PropertyBoolean forceLxProperty;     // property is "lx user property" even if it does not start with "lx_"
    PropertyBoolean isMaterialProperty;
    PropertyInteger isLuccProperty;  // 0 is not lucc property, 1 is lucc property, 2 is unmodified lucc property from csv file
    PropertyInteger lxzType;
    PropertyInteger lccCompany;
    PropertyBoolean isUserLxz;
    PropertyBoolean isLccUserCatalog;
    PropertyBoolean extended;
    PropertyBoolean allowEditIfc;
    PropertyText npkChapter;

    PropertyText formulaArg1;
    PropertyText formulaOp1;
    PropertyText formulaArg2;
    PropertyText formulaOp2;
    PropertyText formulaArg3;

    Core::PropertyReal durationTimePerQuantity;
    Core::PropertyReal durationTimePerDay;
    Core::PropertyReal durationFactor;

    PropertyText linkedParameterName;

    PropertyDescriptor();
    virtual ~PropertyDescriptor();

    bool mustBeSaved() const override;
    void setMustbeSaved(bool aValue);
    virtual Type getType() const = 0;

    Base::String getDisplayName() const;

    bool hasFormula() const;
    Base::String getFormula() const;

    int getAvailableLmeIndex(int aMin = 1) const;
    static int getAvailableLccIndex(Core::CoreDocument* doc, int aLccCompany);

    void copyValuesFrom(const Core::PropertyDescriptor* other);
    virtual bool isEqualForMerging(const Core::PropertyDescriptor* other, bool ignoreEnumEntries = false);

    void setGeometryLimit(Core::GeometryLimit* gl);
    virtual Core::GeometryLimit* getGeometryLimit(const Base::String& propertyValue = L"") const;  // in enum limit depends on property value

    // for App::PropertySetInfo
    bool isLxzProperty() const;
    Base::String getEntryType() const;                        // returns only existing type
    static Base::String getEntryType(const Base::String& s);  // fix for import
    static const std::vector<std::pair<Base::String, int>>& getEntryTypes() { return _entryTypes; }

    static Core::PropertyDescriptor* getByParameterName(Core::CoreDocument* doc, const Base::String& name);
    static Core::PropertyDescriptor* getByCompanyIndexDecimalIndex(Core::CoreDocument* doc, int aCompany, int aIndex, int aDecimalIndex);
    static Core::PropertyDescriptor* getByCompanyChapterIndex(Core::CoreDocument* doc, int aCompany, const Base::String& aChapter, int aIndex);

    virtual size_t computeHash(bool strictComparison = false);

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;

    /// Restores property from from reader in specified version.
    void restoreProperty(Core::Property* property,
                         const Base::String& name,
                         Base::AbstractXMLReader& reader,
                         Base::PersistenceVersion& version) override;

private:
    PropertyBoolean mustbeSaved_;
    Core::PropertyLink<Core::GeometryLimit*> geometryLimit;

    static std::vector<std::pair<Base::String, int>> _entryTypes;  // entryType, translation id //for App::PropertySetInfo
};

DECLARE_PROPERTY_TEMPLATES(Core::PropertyDescriptor, LX_CORE_EXPORT);
}  // namespace Core