#pragma once

#include <OpenLxApp/Process.h>

FORWARD_DECL(App, Task)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT Task : public Process
{
PROXY_HEADER(Task, App::Task, IFCTASK)

public:
    virtual ~Task() = default;

protected:
    Task() = default;
};
}
