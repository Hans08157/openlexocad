#pragma once

#include <OpenLxApp/DistributionSystem/DistributionFlowElement.h>

FORWARD_DECL(App, FlowSegment)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT FlowSegment : public DistributionFlowElement
{
    PROXY_HEADER(FlowSegment, App::FlowSegment, IFCFLOWSEGMENT)

public:
    ~FlowSegment() override = default;

protected:
    FlowSegment() {}
};
}
