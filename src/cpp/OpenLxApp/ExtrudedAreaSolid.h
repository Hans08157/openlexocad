#pragma once

#include <Geom/Ax2.h>
#include <Geom/Dir.h>
#include <OpenLxApp/CurveBoundedPlane.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/ProfileDef.h>


FORWARD_DECL(Part, ExtrudedAreaSolid)

namespace OpenLxApp
{
/*!
 * @brief The extruded area solid is defined by sweeping a bounded planar surface.
 * The direction of the extrusion is given by the setExtrudedDirection() method
 * and the length of the extrusion is given by the setDepth() method.
 * If the planar area has inner boundaries, i.e. holes defined, then those holes
 * shall be swept into holes of the solid.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcextrudedareasolid.htm" target="_blank">Documentation from IFC4:
 * IfcExtrudedAreaSolid</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT ExtrudedAreaSolid : public Geometry
{
    PROXY_HEADER(ExtrudedAreaSolid, Part::ExtrudedAreaSolid, IFCEXTRUDEDAREASOLID)

    DECL_PROPERTY(ExtrudedAreaSolid, Position, Geom::Ax2)
    DECL_PROPERTY(ExtrudedAreaSolid, ExtrudedDirection, Geom::Dir)
    DECL_PROPERTY(ExtrudedAreaSolid, Depth, double)

public:
    ~ExtrudedAreaSolid(void);

    void setSweptArea(std::shared_ptr<ProfileDef> area);
    std::shared_ptr<ProfileDef> getSweptArea() const;

private:
    ExtrudedAreaSolid(void) {}
};
}  // namespace OpenLxApp
