#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/Geometry.h>

FORWARD_DECL(Part, CompositeCurveSegment)

namespace OpenLxApp
{
/*!
 * @brief A composite curve segment is a bounded curve together with transition
 * information which is used to construct a composite curve.
 * (Definition from ISO/CD 16739:2011)
 * Note: Transition information is not implemented yet.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccompositecurvesegment.htm" target="_blank">Documentation from IFC4:
 * IfcCompositeCurveSegment</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT CompositeCurveSegment : public Geometry
{
    PROXY_HEADER(CompositeCurveSegment, Part::CompositeCurveSegment, IFCCOMPOSITECURVESEGMENT)

    DECL_PROPERTY(CompositeCurveSegment, SameSense, bool)
public:
    ~CompositeCurveSegment(void);

    void setParentCurve(std::shared_ptr<BoundedCurve> boundedCurve);
    std::shared_ptr<BoundedCurve> getParentCurve() const;

private:
    CompositeCurveSegment(void) {}
};
}  // namespace OpenLxApp
