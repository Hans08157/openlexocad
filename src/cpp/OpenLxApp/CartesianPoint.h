#pragma once

#include <Geom/Pnt.h>
#include <OpenLxApp/Geometry.h>

FORWARD_DECL(Part, CartesianPoint)

namespace OpenLxApp
{
/*!
 * @brief A point defined by its coordinates in a two or three dimensional rectangular Cartesian coordinate system,
 * or in a two dimensional parameter space. The entity is defined in a two or three dimensional space.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccartesianpoint.htm" target="_blank">Documentation from IFC4:
 * IfcCartesianPoint</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT CartesianPoint : public Geometry
{
    PROXY_HEADER(CartesianPoint, Part::CartesianPoint, IFCCARTESIANPOINT)
    DECL_PROPERTY(CartesianPoint, Point, Geom::Pnt)

public:
    ~CartesianPoint(void);

private:
    CartesianPoint(void) {}
};
}  // namespace OpenLxApp
