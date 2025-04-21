#pragma once

#include <OpenLxApp/DistributionSystem/DistributionElement.h>

FORWARD_DECL(App, DistributionFlowElement)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT DistributionFlowElement : public DistributionElement
{
    PROXY_HEADER(DistributionFlowElement, App::DistributionFlowElement, IFCDISTRIBUTIONFLOWELEMENT)

public:
    ~DistributionFlowElement() override = default;

protected:
    DistributionFlowElement() {}
};
}
