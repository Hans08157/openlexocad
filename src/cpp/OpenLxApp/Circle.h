#pragma once

#include <OpenLxApp/Conic.h>



FORWARD_DECL(Part, Circle)

namespace OpenLxApp
{
/*!
 * @brief A circle is defined by a radius and the location and orientation of the circle.
 * (Definition from ISO/CD 16739:2011)
 *
 ** @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccircle.htm" target="_blank">Documentation from IFC4: IfcCircle</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Circle : public Conic
{
    PROXY_HEADER(Circle, Part::Circle, IFCCIRCLE)

    DECL_PROPERTY(Circle, Radius, double)

public:
    ~Circle(void);

private:
    Circle(void) {}
};
}  // namespace OpenLxApp
