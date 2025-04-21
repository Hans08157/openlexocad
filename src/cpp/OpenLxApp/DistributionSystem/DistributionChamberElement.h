#pragma once

#include <OpenLxApp/DistributionSystem/DistributionFlowElement.h>

FORWARD_DECL(App, DistributionChamberElement)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT DistributionChamberElement : public DistributionFlowElement
{
    PROXY_HEADER(DistributionChamberElement, App::DistributionChamberElement, IFCDISTRIBUTIONCHAMBERELEMENT)

public:
    ~DistributionChamberElement() override = default;

    enum class DistributionChamberElementTypeEnum
    {
        FORMEDDUCT,
        INSPECTIONCHAMBER,
        INSPECTIONPIT,
        MANHOLE,
        METERCHAMBER,
        SUMP,
        TRENCH,
        VALVECHAMBER,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(DistributionChamberElementTypeEnum aType);
    DistributionChamberElementTypeEnum getPredefinedType() const;

protected:
    DistributionChamberElement() {}
};
}
