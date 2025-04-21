#pragma once

#include <Core/PropertyPoint.h>
#include <OpenLxApp/BoundedCurve.h>


FORWARD_DECL(Part, Polyline)

namespace OpenLxApp
{
/*!
 * @brief The Polyline is a bounded curve with only linear segments
 * defined by a list of Cartesian points. If the first and the last Cartesian
 * point in the list are identical, then the polyline is a closed curve,
 * otherwise it is an open curve.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcpolyline.htm" target="_blank">Documentation from IFC4: IfcPolyline</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Polyline : public BoundedCurve
{
    PROXY_HEADER(Polyline, Part::Polyline, IFCPOLYLINE)

    DECL_PROPERTY(Polyline, Points, std::vector<Geom::Pnt>)

public:
    ~Polyline(void);

private:
    Polyline(void) {}
};
}  // namespace OpenLxApp
