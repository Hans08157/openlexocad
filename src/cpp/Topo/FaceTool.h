#pragma once

#include <Geom/Precision.h>
#include <Topo/ToolOutcome.h>
#include <Topo/Types.h>
#include <vector>


class FACE;
class TopoDS_Face;

namespace Mesher
{
class ShapeTesselator;
class ShapeTesselator_OCC;
class TriangleData;
class TriangleData_OCC;
}  // namespace Mesher

namespace MesherAcis
{
class ShapeTesselator_Acis;
class TriangleData_Acis;
}  // namespace MesherAcis


namespace Part
{
class SnapPointTool;
}
namespace Geom
{
class Pnt;
class Dir;
class Ax2;
class Circ;
class Pln;
class Trsf;
class Bnd_Box;
class Pnt2d;
enum class SurfaceType;
}

namespace App
{
class SurfaceStyleAssignment;
}  // namespace App

namespace Topo
{
struct SpecialFaceInfo;
enum class FaceClashType;
    /**
 * @brief Tools for creating, manipulating and querying Faces.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT FaceTool
{
public:
    FaceTool(void);
    virtual ~FaceTool(void);

    friend class Mesher::ShapeTesselator;
    friend class Mesher::ShapeTesselator_OCC;
    friend class MesherAcis::ShapeTesselator_Acis;
    friend class Mesher::TriangleData;
    friend class Mesher::TriangleData_OCC;
    friend class MesherAcis::TriangleData_Acis;
    friend class Part::SnapPointTool;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Copies a face
    static pFace copy(pConstFace face);
    /// Makes a face from a wire. The wire describes the outer boundary of the face
    static pFace makeFace(pWire outer, double precision = Geom::Precision::linear_Resolution());
    /// Makes a face from three points
    static pFace makeFace(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& p3);
    /// Makes a face from four points
    static pFace makeFace(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& p3, const Geom::Pnt& p4);
    /// Makes a cylindrical face
    static pFace makeCylindricalFace(const Geom::Circ& aCircle, double aParam1, double aParam2, double aHeight);
    /// Makes a planar face from an outer wire describing the outer boundary and inner wires describing the holes in the face. The wires must not
    /// overlap. Inner and outer wires must have opposite orientations.
    static pFace makePlanarFace(pWire outerWire, const std::vector<pWire>& innerWires, double precision = Geom::Precision::linear_Resolution());
    /// Makes a planar face from the given wires. Each closed region on each wire is covered and all of the covered regions are united.
    static pFace makePlanarFaceWithoutVoids(const std::vector<pWire>& wires, double precision = Geom::Precision::linear_Resolution());
    /// Makes planar faces from BrepData
    static std::vector<pFace> makePlanarFaces(pConstBrepData data);
    /// Makes a face from an outer wire describing the outer boundary and inner wires describing the holes in the face. The wires must not overlap.
    /// Inner and outer wires must have opposite orientations.
    static pFace makeFace(pWire outerWire, const std::vector<pWire>& innerWires, double precision = Geom::Precision::linear_Resolution());
    /// Makes a polygonal face from a vector of points
    static pFace makePolygon(const std::vector<Geom::Pnt>& points);
    /// Checks if p is a valid point on face within the given tolerance.
    static bool isValidPointForFace(const Geom::Pnt& p, pConstFace face, double precision = Geom::Precision::linear_Resolution());
    /// Returns a copy of 'face' transformed by 'transform'
    static pFace transformed(pConstFace face, const Geom::Trsf& transform);
    /// Returns the surface type of the underlying geometry of the face
    static bool getGeomSurfaceType(pConstFace face, Geom::SurfaceType& type);
    /// Returns the surface type of the underlying geometry of the face
    static bool getGeomSurfaceType(FACE* face, Geom::SurfaceType& type);
    /// Returns the area of the face
    static double getArea(pConstFace face);
    /// Returns the outer boundary of the face
    static pConstWire getOuterBoundary(pConstFace face);
    /// Returns the inner boundaries of the face
    static std::vector<pConstWire> getInnerBoundaries(pConstFace face);
    /// Makes a connected face set from a model description and a vector of points. Returns an empty shell on failure
    static pShape makeConnectedFaceSet(const std::vector<int>& model, const std::vector<Geom::Pnt>& vertices);
    /// Returns true if surface type is BEZIERSURFACE or BSPLINESURFACE
    static bool isNurbs(pConstFace face);
    /// Extrudes a planar face in the given extrudedDirection with the given depth. It returns nullptr on failure
    static pShape extrudePlanarFace(pConstFace face, const Geom::Dir& extrudedDirection, double depth);    
    /// Extrudes a face in the given extrudedDirection with the given depth. It returns nullptr on failure
    static pShape extrudedFace(pConstFace face, const Geom::Dir& extrudedDirection, double depth);    
    /// Moves a face in the given extrudedDirection with the given depth. It returns nullptr on failure, see acis sweepMore()
    static pShape tweakFaceToPlane(pConstFace face, const Geom::Dir& extrudedDirection, double depth);
    /// Extends the input list of edges from the given face by offsetting those along the surfaces by the given distance. The face must belong to a
    /// shape. It must be the only face in the shape.
    static bool extendFace(pFace face, const std::vector<pConstEdge>& edges, double offset);
    /// Get parameters of circular face
    static bool getCircularSurfaceParams(pConstFace face, Geom::Circ& circle);
    /// Get parameters of cylinder face
    static bool getCylinderSurfaceParams(pConstFace face, Geom::Ax2& position, double& radius);
    /// Get parameters of cylinder face
    static bool getCylinderSurfaceParams(FACE* face, Geom::Ax2& position, double& radius);
    /// Get parameters of cone face
    static bool getConeSurfaceParams(pConstFace face, Geom::Ax2& position, double& angle, double& radius);
    /// Get parameters of cone face
    static bool getConeSurfaceParams(FACE* face, Geom::Ax2& position, double& angle, double& radius);
    /// Returns centre of mass (centre of gravity) of the face
    static Geom::Pnt getCentre(pConstFace face);
    /// Projects point 'p' on 'face'. Returns the nearest solution point.
    static bool projectPointOnFace(const Geom::Pnt& p, pConstFace face, Geom::Pnt& nearest);
    /// Projects point 'p' on 'face'. Returns the parameter 'u' and 'v' at that point. Only the nearest solution is returned.
    static bool projectPointOnFace(const Geom::Pnt& p, pConstFace face, double& u, double& v);
    /// Returns true if the face is self-intersecting
    static bool isSelfIntersecting(pConstFace face);
    /// Return the points of the outer boundary
    static void getOuterBoundaryPoints(pConstFace face, std::vector<Geom::Pnt>& pnts);
    /// Return the points of the outer boundary
    static void getOuterBoundaryPointsFast(pConstFace face, std::vector<Geom::Pnt>& pnts);
    /// Computes the minimum distances and the closest positions between an entity and a point
    static bool getPointFaceDistance(const Geom::Pnt& p, pConstFace face, Geom::Pnt& nearest, double& distance);
    /// Contains Face
    static bool containsFace(pConstFace outerface, pConstFace innerFace);
    /// Special Info for Face, Cone, Cylinder
    static std::shared_ptr<Topo::SpecialFaceInfo> getSpecialFaceInfo(pConstFace face);
    /// Performs a clash of two faces and reports if they touch one another
    static Topo::ToolOutcome clash(pConstFace face1, pConstFace face2, bool& hasClash);
    /// Perform a real clash of two faces and report the way in which these shapes clash
    static Topo::ToolOutcome clashFaces(pConstFace face1, pConstFace face2, Topo::FaceClashType& clashType);
    /// Checks if a face is rectangular and returns its parameters.
    static bool isRectangular(pConstFace face, Geom::Ax2& position, double& width, double& height);

    /// Projects a face onto a plane (projection along given Direction). Returns the new projected face.
    static pFace projectFaceOnPlane(pConstFace face, const Geom::Dir& dir, const Geom::Pln& pln);

    static void getOuterBoundaryPointsFast(FACE*, std::vector<Geom::Pnt>& pnt);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
               /// @cond INTERNAL

    /// Sets the default FaceTool. For internal use only.
    static void __setDefaultFaceTool__(Topo::FaceTool* tool) { _defaultTool = tool; }
    static void __setAcisShapeTool__(Topo::FaceTool* tool) { _acisTool = tool; }
    static bool isPlanarFace(pConstFace face);
    /// Makes a face from a wire. The wire describes the outer boundary of the face. Orientation is taken from refNormal.
    static pFace makeFace(pWire outer, const Geom::Dir& refNormal, double precision = Geom::Precision::linear_Resolution());
    /// Makes a face from an outer wire describing the outer boundary and inner wires describing the holes in the face. The wires must not overlap.
    /// Inner and outer wires must have opposite orientations. Orientation is taken from refNormal.
    static pFace makeFace(pWire outerWire,
                          const std::vector<pWire>& innerWires,
                          const Geom::Dir& refNormal,
                          double precision = Geom::Precision::linear_Resolution());

protected:
    /// Gets the TopoDS_Face of 'face'. Returns 'true' on success, 'false' if shape has no TopoDS_Face or the TopoDS_Face is Null.
    static bool getTopoDS_Face(pConstFace face, TopoDS_Face& topoFace);

    virtual pFace _copy(pConstFace face);
    virtual pFace _makeFace(pWire outer, double precision, const Geom::Dir* refNormal);
    virtual pFace _makeFace(pWire outerWire, const std::vector<pWire>& innerWires, double precision, const Geom::Dir* refNormal);
    virtual pFace _makePolygon(const std::vector<Geom::Pnt>& points);
    virtual bool _isValidPointForFace(const Geom::Pnt& p, pConstFace face, double precision = Geom::Precision::linear_Resolution());
    virtual pFace _transformed(pConstFace face, const Geom::Trsf& transform);
    virtual bool _getGeomSurfaceType(pConstFace face, Geom::SurfaceType& type);
    virtual bool _getGeomSurfaceType(FACE* , Geom::SurfaceType& type);
    virtual double _getArea(pConstFace face);
    virtual bool _getTopoDS_Face(pConstFace face, TopoDS_Face& topoFace);
    virtual pConstWire _getOuterBoundary(pConstFace face);
    virtual std::vector<pConstWire> _getInnerBoundaries(pConstFace face);
    virtual pShape _makeConnectedFaceSet(const std::vector<int>& model, const std::vector<Geom::Pnt>& vertices);
    virtual pShape _extrudePlanarFace(pConstFace face, const Geom::Dir& extrudedDirection, double depth);
    virtual pShape _extrudedFace(pConstFace face, const Geom::Dir& extrudedDirection, double depth);
    virtual pShape _tweakFaceToPlane(pConstFace face, const Geom::Dir& extrudedDirection, double depth);
    virtual bool _extendFace(pFace face, const std::vector<pConstEdge>& edges, double offset);
    virtual bool _getCylinderSurfaceParams(FACE* face, Geom::Ax2& position, double& radius);
    virtual bool _getCylinderSurfaceParams(pConstFace face, Geom::Ax2& position, double& radius);
    virtual bool _getConeSurfaceParams(FACE*  face, Geom::Ax2& position, double& angle, double& radius);
    virtual bool _getConeSurfaceParams(pConstFace face, Geom::Ax2& position, double& angle, double& radius);
    virtual Geom::Pnt _getCentre(pConstFace face);
    virtual bool _projectPointOnFace(const Geom::Pnt& p, pConstFace face, Geom::Pnt& nearest);
    virtual bool _projectPointOnFace(const Geom::Pnt& p, pConstFace face, double& u, double& v);
    virtual bool _isSelfIntersecting(pConstFace face);
    virtual pFace _makePlanarFace(pWire outerWire, const std::vector<pWire>& innerWires, double precision);
    virtual pFace _makePlanarFaceWithoutVoids(const std::vector<pWire>& wires, double precision);
    virtual std::vector<pFace> _makePlanarFaces(pConstBrepData data);
    virtual void _getOuterBoundaryPoints(pConstFace face, std::vector<Geom::Pnt>& pnts);
    virtual void _getOuterBoundaryPointsFast(pConstFace face, std::vector<Geom::Pnt>& pnts);
    virtual void _getOuterBoundaryPointsFast(FACE*, std::vector<Geom::Pnt>& pnts);
    virtual bool _getPointFaceDistance(const Geom::Pnt& p, pConstFace face, Geom::Pnt& nearest, double& distance);
    virtual bool _containsFace(pConstFace outerface, pConstFace innerFace);
    virtual bool _createTextureCoordinates(pConstFace face,
                                           const Geom::Bnd_Box& bbox,
                                           const App::SurfaceStyleAssignment* ssa,
                                           std::vector<Geom::Pnt2d>& coord);
    virtual bool _isPlanarFace(pConstFace face);
    virtual Topo::ToolOutcome _clash(pConstFace face1, pConstFace face2, bool& hasClash);
    virtual Topo::ToolOutcome _clashFaces(pConstFace face1, pConstFace face2, Topo::FaceClashType& clashType);
    static Topo::FaceTool* _defaultTool;
    static Topo::FaceTool* _acisTool;
    /// @endcond

#endif
};


}  // namespace Topo
