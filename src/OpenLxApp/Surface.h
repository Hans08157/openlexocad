#pragma once

#include <OpenLxApp/Geometry.h>



FORWARD_DECL(Part, Surface)

namespace OpenLxApp
{
/*!
 * @brief A surface can be envisioned as a set of connected points in 3-dimensional space
 * which is always locally 2-dimensional, but need not be a manifold.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcsurface.htm" target="_blank">Documentation from IFC4: IfcSurface</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Surface : public Geometry
{
    PROXY_HEADER_ABSTRACT(Surface, Part::Surface, IFCSURFACE)

public:
    virtual ~Surface(void);

protected:
    Surface() {}
};
}  // namespace OpenLxApp
