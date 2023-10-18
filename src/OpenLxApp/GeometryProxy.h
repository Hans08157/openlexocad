#pragma once

#include <OpenLxApp/Geometry.h>


namespace OpenLxApp
{
/*!
 * @brief A GeometryProxy can hold any type of Geometry.
 * It must be instantiated with a specific type.
 *
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT GeometryProxy : public Geometry
{
    PROXY_HEADER_ABSTRACT(GeometryProxy, App::Geometry, IFC_ENTITY_UNDEFINED)

public:
    ~GeometryProxy(void);

private:
    GeometryProxy() {}
};

}  // namespace OpenLxApp
