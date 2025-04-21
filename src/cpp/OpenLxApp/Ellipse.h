#pragma once

#include <OpenLxApp/Conic.h>


FORWARD_DECL(Part, Ellipse)

namespace OpenLxApp
{
/*!
 * @brief An IfcEllipse is a curve consisting of a set of points
 * whose distances to two fixed points add to the same constant.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcellipse.htm" target="_blank">Documentation from IFC4: IfcEllipse</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Ellipse : public Conic
{
    PROXY_HEADER(Ellipse, Part::Ellipse, IFCELLIPSE)

    DECL_PROPERTY(Ellipse, SemiAxis1, double)
    DECL_PROPERTY(Ellipse, SemiAxis2, double)

public:
    ~Ellipse(void);

private:
    Ellipse(void) {}
};

}  // namespace OpenLxApp
