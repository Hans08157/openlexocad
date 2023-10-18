#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/BoundedSurface.h>
#include <OpenLxApp/Plane.h>

#include <memory>
#include <vector>



FORWARD_DECL(Part, CurveBoundedSurface)

namespace OpenLxApp
{
/*!
 * @brief The curve bounded surface is a parametric surface with curved boundaries
 * defined by one or more boundary curves. The bounded surface is defined to be the portion
 * of the basis surface in the direction of N x T from any point on the boundary, where N
 * is the surface normal and T the boundary curve tangent vector at this point.
 * The region so defined shall be arcwise connected. (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccurveboundedplane.htm" target="_blank">Documentation from IFC4:
 * IfcCurveBoundedPlane</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT CurveBoundedPlane : public BoundedSurface
{
    PROXY_HEADER(CurveBoundedPlane, Part::CurveBoundedSurface, IFCCURVEBOUNDEDPLANE)

public:
    ~CurveBoundedPlane(void);

    void setBasisSurface(std::shared_ptr<Plane> surface);
    void setOuterBoundary(std::shared_ptr<BoundedCurve> outerBound);
    void setInnerBoundaries(const std::vector<std::shared_ptr<BoundedCurve>>& innerBounds);

    std::shared_ptr<ElementarySurface> getBasisSurface() const;
    std::shared_ptr<BoundedCurve> getOuterBoundary() const;
    std::vector<std::shared_ptr<BoundedCurve>> getInnerBoundaries() const;


private:
    CurveBoundedPlane(void) {}
};
}  // namespace OpenLxApp
