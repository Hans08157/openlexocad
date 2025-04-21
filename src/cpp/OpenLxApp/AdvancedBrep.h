#pragma once

#include <OpenLxApp/Geometry.h>



FORWARD_DECL(Part, AdvancedBrep)

namespace OpenLxApp
{
/*!
 * @section introsec Introduction
 *
 * @brief An advanced B-rep is a boundary representation model in which all faces, edges and vertices are explicitly represented.
 * It is a solid with explicit topology and elementary or free-form geometry. The faces of the B-rep are of type IfcAdvancedFace.
 * An advanced B-rep has to meet the same topological constraints as the manifold solid B-rep.
 * (Definition from ISO/CD 16739:2011)
 *
 *
 *
 * An AdvancedBrep is the generalized form of a @ref FacetedBrep "FacetedBrep".
 * Where the @ref FacetedBrep "FacetedBrep" has to be a polyhedron - in a mathematical sense - the AdvancedBrep "only" has to be a manifold.
 * This means, it still has to be a closed body, but its faces and edges don't have to be planar or straight anymore.
 *
 * In contrast to the @ref FacetedBrep "FacetedBrep", you can't define an AdvancedBrep via @ref FacetedBrep::setPoints "setPoints()"
 * and @ref FacetedBrep::setModel "setModel" methods. To create an AdvancedBrep, you have to define its faces and merge them into a shape, which then
 * forms the AdvancedBrep via the @ref setShape method (similar to the first approach described in @ref FacetedBrep "FacetedBrep").
 *
 *
 *
 *
 * @section example Example
 *
 * The following example will create a cylinder by creating each of the outer faces separately and then merging them into an advanced brep.
 * @include examples/advancedBrep.py
 * <center><b>The result:</b><br/></center>
 * @image html images/AdvancedBrep/AdvancedBrep.png "An AdvancedBrep." width=60%
 *
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcadvancedbrep.htm" target="_blank">Documentation from IFC4:
 * IfcAdvancedBrep</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT AdvancedBrep : public Geometry
{
    PROXY_HEADER(AdvancedBrep, Part::AdvancedBrep, IFCADVANCEDBREP)

public:
    ~AdvancedBrep(void);
    bool setShape(pShape aShape);

private:
    AdvancedBrep(void) {}
};

}  // namespace OpenLxApp
