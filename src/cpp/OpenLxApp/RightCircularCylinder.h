#pragma once

#include <Geom/Ax2.h>
#include <OpenLxApp/Geometry.h>


FORWARD_DECL(Part, Cylinder)

namespace OpenLxApp
{
/*!
 * @brief A right circular cylinder is a CSG primitive in the
 * form of a solid cylinder of finite height. It is defined by
 * an axis point at the centre of one planar circular face, an axis,
 * height, and a radius. The faces are perpendicular to the axis and
 * are circular discs with the specified radius. The height is the
 * distance from the first circular face centre in the positive direction
 * of the axis to the second circular face centre.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrightcircularcylinder.htm" target="_blank">Documentation from IFC4:
 * IfcRightCircularCylinder</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */


class LX_OPENLXAPP_EXPORT RightCircularCylinder : public Geometry
{
    PROXY_HEADER(RightCircularCylinder, Part::Cylinder, IFCRIGHTCIRCULARCYLINDER)

    DECL_PROPERTY(RightCircularCylinder, Position, Geom::Ax2)
    DECL_PROPERTY(RightCircularCylinder, Radius, double)
    DECL_PROPERTY(RightCircularCylinder, Height, double)


public:
    ~RightCircularCylinder(void);


private:
    RightCircularCylinder(void) {}
};
}  // namespace OpenLxApp
