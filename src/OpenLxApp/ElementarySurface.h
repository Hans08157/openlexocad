#pragma once

#include <OpenLxApp/Surface.h>



FORWARD_DECL(Part, ElementarySurface)

namespace OpenLxApp
{
/*!
 * @brief An elementary surface is a simple analytic surface with defined parametric representation.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcelementarysurface.htm" target="_blank">Documentation from IFC4:
 * IfcElementarySurface</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT ElementarySurface : public Surface
{
    PROXY_HEADER_ABSTRACT(ElementarySurface, Part::ElementarySurface, IFCELEMENTARYSURFACE)

public:
    virtual ~ElementarySurface(void);

protected:
    ElementarySurface(void) {}
};
}  // namespace OpenLxApp
