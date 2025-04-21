#pragma once

#include <Core/PropertyAxis2.h>
#include <Geom/Ax2.h>
#include <OpenLxApp/Geometry.h>


FORWARD_DECL(Part, Box)

namespace OpenLxApp
{
/*!
 *
 * @brief A box is a solid rectangular parallelepiped,
 * defined with a location and placement coordinate system.
 * The box is specified by the positive lengths x, y, and z
 * along the axes of the placement coordinate system, and has
 * one vertex at the origin of the placement coordinate system.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/schema/ifcgeometricmodelresource/lexical/ifcblock.htm"
 * target="_blank">Documentation from IFC4: IfcBlock</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Block : public Geometry
{
    PROXY_HEADER(Block, Part::Box, IFCBLOCK)

    DECL_PROPERTY(Block, XLength, double)
    DECL_PROPERTY(Block, YLength, double)
    DECL_PROPERTY(Block, ZLength, double)
    DECL_PROPERTY(Block, Position, Geom::Ax2)

    // Deprecated:
    DECL_PROPERTY(Block, Length, double)  // Deprecated. Use XLength instead.
    DECL_PROPERTY(Block, Width, double)   // Deprecated. Use YLength instead.
    DECL_PROPERTY(Block, Height, double)  // Deprecated. Use ZLength instead.



public:
    ~Block();

private:
    Block() {}
};

}  // namespace OpenLxApp
