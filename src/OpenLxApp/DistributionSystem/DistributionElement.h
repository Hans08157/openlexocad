#pragma once

#include <OpenLxApp/Element.h>

FORWARD_DECL(App, DistributionElement)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT DistributionElement : public Element
{
    PROXY_HEADER(DistributionElement, App::DistributionElement, IFCDISTRIBUTIONELEMENT)

public:
    ~DistributionElement() override = default;

protected:
    DistributionElement() {}
};
}