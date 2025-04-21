#pragma once

#include <Geom/Pnt.h>
#include <OpenLxApp/Geometry.h>
#include <vector>



FORWARD_DECL(Part, FacetedBrep)

namespace OpenLxApp
{
/*!
 * @section introsec Introduction
 *
 * @brief A faceted brep is a simple form of boundary representation model
 * in which all faces are planar and all edges are straight lines.
 * A faceted B-rep has to meet the same topological constraints as the manifold solid Brep.
 * (Definition from ISO/CD 16739:2011)
 *
 *
 *
 * A faceted brep can be used to create a polyhedron. Polyhedra are 3D objects only composed by planar faces.
 * Each face again has to be limited by straight edges.
 * An edge is - in this case - defined as a straight line between two points (respectively, vertices).
 *
 * Creating a faceted brep via this hirachical (or topological) approach is totally valid.
 * To do so, you have to:
 * <ol>
 *  <li> Define your set of @ref Geom::Pnt.</li>
 *  <li> Form a @ref Topo::Edge each of two different @ref Geom::Pnt (Have a look at @ref Topo::EdgeTool). </li>
 *  <li> Combine differend @ref Topo::Edge to a set of @ref Topo::Wire in a connected order (Have a look at @ref Topo::WireTool) </li>
 *  <li> Create @ref Topo::Face each of one outer @ref Topo::Wire and multiple (including zero) inner @ref Topo::Wire (Have a look at @ref
 * Topo::FaceTool). </li> <li> Merge the different @ref Topo::Face into a @ref Topo::Shape (Have a look at @ref Topo::ShapeTool). </li> <li> If this
 * @ref Topo::Shape is a polyhedron (in the mathematical sense), you can use @ref setShape to make it become a faceted brep. </li>
 * </ol>
 * <br/>
 * Another way to create a faceted brep is to use the @ref setPoints and @ref setModel functions. <br/>
 * The approach is different here.
 * <ol>
 *  <li> Set up a list of @ref Geom::Pnt and pass them to the faceted brep via @ref setPoints </li>
 *  <li> Set up a list of indices, pointing into this pointist and pass them to the faceted brep via @ref setModel </li>
 * </ol>
 * These indices have to follow a specific format and order:<br/><br/>
 * <b>The format:</b><br/>
 * Each index refers to a point in the pointlist. A sequence of indices represents a wire. Since faces are allowed to have voids
 * (as long as the resulting shape is still a polyhedron), one face can be made of several wires. To indicate the end of a wire, the index -2 is used.
 * To indicate the end of a face, the index -1 is used. If your face is only constructed by a single wire,
 * you still have to use the -2 to indicate the end of the wire, before indicating the end of the face (by a -1).<br/>
 * <br/>
 * <b>The order:</b><br/>
 * The order of the indices is used to determine, which side of it is the "outside" and which one is the "inside".<br/>
 * Looking at the face from the outside, the indices representing the outer boundary of the face, have to follow a <b>counter clockwise</b> order.
 * To cut voids into a face, the indices of this void-wire have to follow a <b>clockwise</b> order (again, looking from the outside of the face onto
 * it).<br/> The following image shows a face with a void from the "outside". The red arrows are indicating the winding (respectively order):
 * @image html images/FacetedBrep/FacetedBrep_winding_of_face_with_void.png "The winding of a face with a void." width=60%
 *
 *
 *
 * @section examples Examples
 *
 * The following example shows, how you can create a simple box with a side length of 10 as a faceted brep.
 * It is created by setting a list of points and indices (as described in the second approach).
 *
 * @include examples/facetedBrep_0.py
 * <center><b>The result:</b><br/></center>
 * @image html images/FacetedBrep/FacetedBrep_box.png "A simple box, created as faceted brep." width=60%
 *
 *
 *
 * This example extends the previous one, by carving a void into the top and bottom face. Again, the winding is important here.
 * To cut out the voids, the inner points have to be accessed in <b>clockwise</b> order,
 * where the outer bounds of each face have to be accessed in <b>counterclockwise</b> order.
 * To make the object still be a polyhderon, additional faces have to be added inbetween the voids. The result is a box with a squared tunnel.
 *
 * @include examples/facetedBrep_1.py
 * <center><b>The result:</b><br/></center>
 * @image html images/FacetedBrep/FacetedBrep_box_with_tunnel.png "A simple box with a tunnel, created as faceted brep." width=60%
 *
 *
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcfacetedbrep.htm" target="_blank">Documentation from IFC4:
 * IfcFacetedBrep</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT FacetedBrep : public Geometry
{
    PROXY_HEADER(FacetedBrep, Part::FacetedBrep, IFCFACETEDBREP)

    DECL_PROPERTY(FacetedBrep, Model, std::vector<int>)
    DECL_PROPERTY(FacetedBrep, Points, std::vector<Geom::Pnt>)

public:
    ~FacetedBrep(void);
    bool setShape(pShape aShape);

private:
    FacetedBrep(void) {}
};

}  // namespace OpenLxApp
