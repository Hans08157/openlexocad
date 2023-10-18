#pragma once

#include <Geom/Ax2.h>
#include <OpenLxApp/Geometry.h>

FORWARD_DECL(Part, Cone)

namespace OpenLxApp
{
/*!
 * @brief The RightCircularRightCircularCone is a Construction Solid Geometry (CSG) 3D primitive.
 * It is a solid with a circular base and a point called apex as the top.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrightcircularcone.htm" target="_blank">Documentation from IFC4:
 * IfcRightCircularCone</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT RightCircularCone : public Geometry
{
    PROXY_HEADER(RightCircularCone, Part::Cone, IFCRIGHTCIRCULARCYLINDER)

    DECL_PROPERTY(RightCircularCone, Position, Geom::Ax2)
    DECL_PROPERTY(RightCircularCone, BottomRadius, double)
    DECL_PROPERTY(RightCircularCone, Height, double)


public:
    ~RightCircularCone(void);


private:
    RightCircularCone(void) {}
};
}  // namespace OpenLxApp
