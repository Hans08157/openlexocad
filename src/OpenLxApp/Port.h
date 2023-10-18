#pragma once

#include <OpenLxApp/Element.h>

FORWARD_DECL(App, Port)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT Port : public Element
{
    PROXY_HEADER(Port, App::Port, IFCPORT)

public:
    ~Port() override = default;

protected:
    Port() {}
};
}