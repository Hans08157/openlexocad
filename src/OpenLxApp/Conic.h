#pragma once

#include <Geom/Ax2.h>
#include <OpenLxApp/Curve.h>


FORWARD_DECL(Part, Conic)

namespace OpenLxApp
{
/*!
 * @brief A conic is a planar curve which could be produced by intersecting
 * a plane with a cone. A conic is defined in terms of its intrinsic geometric
 * properties rather than being described in terms of other geometry.
 * A conic class always has a placement coordinate system defined by a two or three dimensional placement.
 * The parametric representation is defined in terms of this placement coordinate system.
 * (Definition from ISO/CD 16739:2011)
 *
 ** @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcconic.htm" target="_blank">Documentation from IFC4: IfcConic</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */
class LX_OPENLXAPP_EXPORT Conic : public Curve
{
    PROXY_HEADER_ABSTRACT(Conic, Part::Conic, IFCCONIC)

    DECL_PROPERTY(Conic, Position, Geom::Ax2)

public:
    virtual ~Conic(void);

protected:
    Conic(void) {}
};

}  // namespace OpenLxApp