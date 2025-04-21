#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/Conic.h>
#include <OpenLxApp/Line.h>



FORWARD_DECL(Part, BezierCurve)

namespace OpenLxApp
{
/*!
 * @brief This is a special type of curve which can be represented as
 * a type of B-spline curve in which the knots are evenly spaced and
 * have high multiplicities. Suitable default values for the knots and
 * knot multiplicities are derived in this case.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC2x3/TC1/html/ifcgeometryresource/lexical/ifcbeziercurve.htm" target="_blank">Documentation
 * from IFC2x3: IfcBezierCurve</a>
 */

class LX_OPENLXAPP_EXPORT BezierCurve : public BoundedCurve
{
    PROXY_HEADER(BezierCurve, Part::BezierCurve, IFC_ENTITY_UNDEFINED)


    DECL_PROPERTY(BezierCurve, ClosedCurve, bool)
    DECL_PROPERTY(BezierCurve, ControlPointsList, std::vector<Geom::Pnt>)
    DECL_PROPERTY(BezierCurve, Degree, int)
    DECL_PROPERTY(BezierCurve, SelfIntersect, bool)

public:
    ~BezierCurve(void);

private:
    BezierCurve(void) {}
};
}  // namespace OpenLxApp
