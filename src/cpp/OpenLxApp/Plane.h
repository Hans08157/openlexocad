#pragma once

#include <Geom/Ax2.h>
#include <OpenLxApp/ElementarySurface.h>



FORWARD_DECL(Part, Plane)

namespace OpenLxApp
{
/*!
 * @brief A plane is an unbounded surface with a constant normal.
 * A plane is defined by a point on the plane and the normal direction to the plane.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcplane.htm" target="_blank">Documentation from IFC4: IfcPlane</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Plane : public ElementarySurface
{
    PROXY_HEADER(Plane, Part::Plane, IFCPLANE)

    DECL_PROPERTY(Plane, Position, Geom::Ax2)

public:
    ~Plane(void);



private:
    Plane(void) {}
};

}  // namespace OpenLxApp
