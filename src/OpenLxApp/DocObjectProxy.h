#pragma once

#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Globals.h>


namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT DocObjectProxy : public DocObject
{
    PROXY_HEADER_ABSTRACT(DocObjectProxy, Core::DocObject, IFC_ENTITY_UNDEFINED)

public:
    ~DocObjectProxy(void);

protected:
    DocObjectProxy() {}
};
}  // namespace OpenLxApp