#pragma once

#include <OpenLxApp/Element.h>

FORWARD_DECL(App, CivilElement)

namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT CivilElement : public Element
{
PROXY_HEADER(CivilElement, App::CivilElement, IFCCIVILELEMENT)

public:
    virtual ~CivilElement() = default;

protected:
    CivilElement() = default;
};
}
