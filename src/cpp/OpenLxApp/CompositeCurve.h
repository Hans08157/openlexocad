#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/CompositeCurveSegment.h>

#include <vector>



FORWARD_DECL(Part, CompositeCurve)

namespace OpenLxApp
{
/*!
 * @brief A composite curve (IfcCompositeCurve) is a collection of curves joined end-to-end.
 * The individual segments of the curve are themselves defined as composite curve segments.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccompositecurve.htm" target="_blank">Documentation from IFC4:
 * IfcCompositeCurve</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT CompositeCurve : public BoundedCurve
{
    PROXY_HEADER(CompositeCurve, Part::CompositeCurve, IFCCOMPOSITECURVE)

    DECL_PROPERTY(CompositeCurve, Allow3dCurve, bool)

public:
    ~CompositeCurve(void);

    void addSegment(std::shared_ptr<CompositeCurveSegment> segment);
    std::vector<std::shared_ptr<CompositeCurveSegment>> getSegments() const;

private:
    CompositeCurve(void) {}
};
}  // namespace OpenLxApp
