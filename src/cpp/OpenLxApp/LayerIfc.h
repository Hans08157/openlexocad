#pragma once

#include <App/LayerIfc.h>
#include <OpenLxApp/Layer.h>

FORWARD_DECL(App, LayerIfc)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT LayerIfc : public Layer
{
    PROXY_HEADER(LayerIfc, App::LayerIFC, IFC_ENTITY_UNDEFINED)

public:
    ~LayerIfc() override = default;

protected:
    LayerIfc() = default;
};
}
