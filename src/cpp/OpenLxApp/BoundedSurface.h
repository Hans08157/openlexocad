#pragma once

#include <OpenLxApp/Surface.h>



FORWARD_DECL(Part, BoundedSurface)


namespace OpenLxApp
{
/*!
 * @brief A bounded surface is a surface of finite area with identifiable boundaries.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcboundedsurface.htm" target="_blank">Documentation from IFC4:
 * IfcBoundedSurface</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT BoundedSurface : public Surface
{
    PROXY_HEADER_ABSTRACT(BoundedSurface, Part::BoundedSurface, IFCBOUNDEDSURFACE)

public:
    virtual ~BoundedSurface();

protected:
    BoundedSurface() {}
};
}  // namespace OpenLxApp
