#pragma once

#include <Geom/Dir.h>
#include <Geom/Pnt.h>
#include <OpenLxApp/Curve.h>



FORWARD_DECL(Part, Line)

namespace OpenLxApp
{
/*!
 * @brief A line is an unbounded curve with constant tangent direction.
 * A line is defined by a point and a direction. The positive direction
 * of the line is in the direction of the Dir vector.
 * (Definition from ISO/CD 16739:2011)
 *
 ** @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcline.htm" target="_blank">Documentation from IFC4: IfcLine</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Line : public Curve
{
    PROXY_HEADER(Line, Part::Line, IFCLINE)

    DECL_PROPERTY(Line, Point, Geom::Pnt)
    DECL_PROPERTY(Line, Direction, Geom::Dir)

public:
    ~Line(void);

private:
    Line(void) {}
};
}  // namespace OpenLxApp
