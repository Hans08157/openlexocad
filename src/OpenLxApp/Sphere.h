#pragma once

#include <Geom/Ax2.h>
#include <OpenLxApp/Geometry.h>


FORWARD_DECL(Part, Sphere)

namespace OpenLxApp
{
/*!
 * @brief The Sphere is a Construction Solid Geometry (CSG) 3D primitive. It is a solid where all points at the surface have the same distance from
 * the center point. (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcsphere.htm" target="_blank">Documentation from IFC4: IfcSphere</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Sphere : public Geometry
{
    PROXY_HEADER(Sphere, Part::Sphere, IFCSPHERE)

    DECL_PROPERTY(Sphere, Position, Geom::Ax2)
    DECL_PROPERTY(Sphere, Radius, double)


public:
    ~Sphere(void);


private:
    Sphere(void) {}
};
}  // namespace OpenLxApp
