#pragma once

#include <OpenLxApp/Curve.h>


FORWARD_DECL(Part, BoundedCurve)

namespace OpenLxApp
{
/*!
 * @brief A bounded curve is a curve of finite arc length with identifiable end points.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcboundedcurve.htm" target="_blank">Documentation from IFC4:
 * IfcBoundedCurve</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT BoundedCurve : public Curve
{
    PROXY_HEADER_ABSTRACT(BoundedCurve, Part::BoundedCurve, IFCBOUNDEDCURVE)

public:
    bool getStartPoint(Geom::Pnt& p) const;
    bool getEndPoint(Geom::Pnt& p) const;

    virtual ~BoundedCurve();

protected:
    BoundedCurve() {}
};

}  // namespace OpenLxApp
