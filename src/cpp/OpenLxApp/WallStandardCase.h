#pragma once

#include <OpenLxApp/Wall.h>

#include <memory>

FORWARD_DECL(App, WallStandardCase)

namespace OpenLxApp
{
/**
 * @brief TThe WallStandardCase defines a wall with certain constraints for the provision of
 * parameters and with certain constraints for the geometric representation.
 * The WallStandardCase handles all cases of walls, that are extruded vertically:
 * - along the positive z axis of the wall object coordinate system, and
 * - along the positive z axis of the global (world) coordinate system
 *
 * and have a single thickness along the path for each wall layer, i.e.:
 * - parallel sides for straight walls
 * - co-centric sides for curved walls.
 *
 * and have either:
 * - a straight line axis (straight wall), or
 * - a circular arc axis (round wall).
 *
 * and shall not have
 * - aggregated components, that is, parts aggregated to a wall by RelAggregates
 * - shape representation for 'Body' not being an extrusion, or clipped extrusion
 *
 * The following parameter have to be provided:
 * - Wall height, taken from the depth of extrusion, provided by the geometric representation.
 * - Wall thickness, taken from the material layer set usage, attached to the wall
 * - Wall offset from axis, taken from the material layer set usage, attached to the wall
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcwallstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcWallStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT WallStandardCase : public Wall
{
    PROXY_HEADER(WallStandardCase, App::WallStandardCase, IFCWALLSTANDARDCASE)

public:
    virtual ~WallStandardCase(void);
    virtual bool setGeometry(std::shared_ptr<Geometry> geo) override;

protected:
    WallStandardCase() {}
};

}  // namespace OpenLxApp