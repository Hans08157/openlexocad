#pragma once

#include <OpenLxApp/BuildingElementProxy.h>

#include <memory>

FORWARD_DECL(App, BuildingElementProxy)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT PythonElement : public BuildingElementProxy
{
    PROXY_HEADER(PythonElement, App::BuildingElementProxy, IFCPYTHONELEMENT)

    virtual ~PythonElement() = default;

protected:
    PythonElement() = default;
};
}