#pragma once

#include <OpenLxApp/Port.h>

FORWARD_DECL(App, DistributionPort)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT DistributionPort : public Port
{
    PROXY_HEADER(DistributionPort, App::DistributionPort, IFCDISTRIBUTIONPORT)

public:
    enum class FlowDirectionEnum
    {
        SOURCE,
        SINK,
        SOURCEANDSINK,
        NOTDEFINED
    };
	
    void setFlowDirection(FlowDirectionEnum aType);
    FlowDirectionEnum getFlowDirection() const;

    enum class DistributionPortTypeEnum
    {
        CABLE,
        CABLECARRIER,
        DUCT,
        PIPE,
        USERDEFINED,
        NOTDEFINED
    };
	
    void setPredefinedType(DistributionPortTypeEnum aType);
    DistributionPortTypeEnum getPredefinedType() const;

    ~DistributionPort() override = default;

protected:
    DistributionPort() {}
};
}
