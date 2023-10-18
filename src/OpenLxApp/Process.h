#pragma once

#include <OpenLxApp/Object.h>

FORWARD_DECL(App, Process)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT Process : public Object
{
PROXY_HEADER(Process, App::Process, IFCTASK)

public:
    virtual ~Process() = default;

protected:
    Process() = default;
};
}
