#pragma once

#include <Core/DocObject.h>
#include <Core/PropertyBackLink.h>
#include <Core/PropertyBoolean.h>
#include <Core/PropertyInteger.h>
#include <Core/PropertyLink.h>
#include <Core/PropertyReal.h>
#include <Core/PropertyText.h>
#include <Core/PropertyTextList.h>
#include <Core/PropertyTextMap.h>

namespace Core
{
/* @brief Defines geometry limits for PropertyDecriptor
 */
class LX_CORE_EXPORT GeometryLimit : public Core::DocObject
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
    using inherited = Core::DocObject;

public:
    friend class GeometryLimit_Factory;

    enum struct GeometryLimitType : int
    {
        Lxz_eBKP = 101,
        Lxz_4D = 102,
        Lxz_NPK = 103,
    };

    static const int intervalOutOfBounds = 1000;

    PropertyInteger geometryLimitType;
    PropertyInteger lccCompany;
    PropertyInteger index;
    PropertyInteger indexDecimalPart;
    PropertyText npkChapter;
    PropertyText name;
    PropertyText unit;
    PropertyText detail;
    PropertyReal factor;
    PropertyRealList limits;
    PropertyTextMap userDefinedLimits;
    PropertyTextList textLimits;
    PropertyTextList textLimitsFr;
    PropertyInteger defaultInterval;
    PropertyTextList codes;
    PropertyText name2;
    PropertyText unit2;
    PropertyText detail2;
    PropertyReal factor2;
    PropertyRealList limits2;
    PropertyTextMap userDefinedLimits2;
    PropertyTextList textLimits2;
    PropertyTextList textLimits2Fr;
    PropertyInteger defaultInterval2;
    PropertyTextList codes2;

    virtual QString getKeyText(bool first = true) const;

    QString getAsStringComplete() const;
    QString getAsString(bool first = true) const;
    QString getIntervalAsString(int i, bool first = true) const;

    int getNumberOfIntervals(bool first = true) const;

    int getInterval(double d, bool first = true) const;
    int getInterval(const Base::String& str, bool first = true) const;

    int getNPKPositionNumberForInterval(int i, bool first = true) const;
    QString getCodeForInterval(int i, bool first = true) const;

    bool isTextLimit(bool first = true) const;
    QString getTranslatedTextLimit(int i, bool first = true) const;
    QString getTranslatedTextLimit(const Base::String& str, bool first = true) const;

    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool mustBeSaved() const override;

protected:
    GeometryLimit();
    virtual ~GeometryLimit();

    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap) override;

    void restoreProperty(Core::Property* property,
                         const Base::String& aName,
                         Base::AbstractXMLReader& reader,
                         Base::PersistenceVersion& version) override;

private:
    QString getLimitsAsString(bool first = true) const;
    int getUserDefinedInterval(double d, bool first = true) const;
    bool getDoubleFromString(QString& str, double& value) const;
    bool getIntervalFromString(QString& str, double& value1, double& value2) const;

    bool _pre964 = false;  // used in restore() to finish conversion

    static inline double lastLimitIgnoreValue = 99;
};

DECLARE_PROPERTY_TEMPLATES(Core::GeometryLimit, LX_CORE_EXPORT);
DECLARE_OBJECT_FACTORY_NOIFC(Core::GeometryLimit_Factory, Core::GeometryLimit)
}  // namespace Core