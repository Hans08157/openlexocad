#pragma once

#include <OpenLxApp/DocObject.h>

FORWARD_DECL(App, Layer)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT Layer : public DocObject
{
    PROXY_HEADER(Layer, App::Layer, IFC_ENTITY_UNDEFINED)

public:
    friend class Document;

    ~Layer() override = default;

protected:
    Layer() = default;
};
}
