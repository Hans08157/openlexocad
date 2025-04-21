#pragma once


#include <Base/Color.h>
#include <functional>
#include <Geom/Bnd_box.h>
#include <Geom/Precision.h>
#include <Topo/Clash.h>
#include <Topo/GeometricInformation.h>
#include <Topo/ShapeTessellationQuality.h>
#include <Topo/ToolOutcome.h>
#include <Topo/Types.h>


namespace Base { struct Double; }
namespace Base { struct Int; }
namespace Core { class DocObject; }
namespace Geom { class Ax2; }
namespace Geom { class Dir; }
namespace Geom { class GTrsf; }
namespace Geom { class Pln; }
namespace Geom { class Vec; }


class TopoDS_Shape;
class ENTITY;
class BODY;
class CA_Ray;

namespace Base
{
class GlobalAttachment;
class AbstractWriter;
}  // namespace Base

namespace Acis
{
class AcisHelper;
class AcisBrepGeometryAdaptor;
class PolyToAcisConverter;
}  // namespace Acis

namespace Mesh
{
class OmfMeshTool;
}

namespace Mesher
{
class EdgeData;
class ShapeTesselator;
class ShapeTesselator_OCC;
class EdgeData_OCC;
}  // namespace Mesher

namespace MesherAcis
{
class ShapeTesselator_Acis;
class TriangleData_Acis;
class EdgeData_Acis;
class facet_body_thread_worker;
}  // namespace MesherAcis

namespace Core
{
class CoreDocument;
}

namespace App
{
class SubElement;
class Element;
}  // namespace App

class CA_Detail;
class CA_Snap;

typedef std::vector<Geom::Pnt> PNTS;

namespace Topo
{
class Cdwk_SAT_Attributes;
class PathExtrusionFixVerticalOptions;
class ShapeInfo;
class SimplifyOptions;
class SkinningOptions;
class SweepingOptions;
class ThreadPool;
class VisibleEdge;
class RayHit;
typedef std::vector<RayHit> RayHitVector;
/**
 * @brief Tools for creating, manipulating and querying Shapes.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT ShapeTool
{
public:
    ShapeTool(void);
    virtual ~ShapeTool(void);

    friend class Mesher::EdgeData;
    friend class Mesher::EdgeData_OCC;
    friend class Mesher::ShapeTesselator;
    friend class Mesher::ShapeTesselator_OCC;
    friend class MesherAcis::ShapeTesselator_Acis;
    friend class MesherAcis::TriangleData_Acis;
    friend class MesherAcis::EdgeData_Acis;
    friend class MesherAcis::facet_body_thread_worker;
    friend class Mesh::OmfMeshTool;
    friend class Acis::AcisHelper;
    friend class Acis::AcisBrepGeometryAdaptor;
    friend class Acis::PolyToAcisConverter;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    enum class BuildingElementHintEnum
    {
        NO_HINT,
        BEAM_HINT,
        COLUMN_HINT,
        DOOR_HINT,
        MEMBER_HINT,
        PLATE_HINT,
        SLAB_HINT,
        WALL_HINT,
        WINDOW_HINT
    };

    /// Makes a shape from a single vertex
    static pShape makeShape(pVertex vertex);
    /// Makes a shape from a single edge
    static pShape makeShape(pEdge edge);
    /// Makes a shape from a single wire
    static pShape makeShape(pWire wire, double precision = Geom::Precision::linear_Resolution());
    /// Makes a shape from a single face
    static pShape makeShape(pFace face);
    /// Makes a shape from BrepData
    static pShape makeShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    /// Makes a shape from Acis BODY
    static pShape makeShape(BODY* aBody);
    /// Makes a shape from BrepData
    static pShape makeLazyFacetedBrepShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    /// Makes a mesh-shape from IndexedData
    static pShape makeInventorMeshShape(pIndexedMesh);
    /// Makes a mesh-shape from BrepData
    static pShape makeInventorMeshShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    /// Makes a mesh-shape from BrepData
    static pShape makeOMFMeshShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    /// Makes a indexed-Mesh from BrepData
    static pIndexedMesh makeIndexedMesh(pConstBrepData data, std::vector<PNTS>& defectPolygons, bool createEdges = false);
    /// Makes a indexed-Mesh from shape
    static pIndexedMesh makeIndexedMesh(pConstShape input, bool createEdges = false);
    /// Make Acis-Shape
    static pShape makeAcisShape(pShape input);
    /// Create BrepData
    static bool createBrepData(pConstShape input, pBrepData data);
    /// Makes a shape from BrepData
    static void makeShapeAsync(pConstBrepData data, std::function<void(pShape newShape, std::vector<PNTS> defectPolygons)> onShapeMadeCB);
    /// Makes a shape from BrepData
    static pShape makeShape(const std::vector<int>& model, const std::vector<Geom::Pnt>& vertices, std::vector<PNTS>& defectPolygons);
    /// Makes a shape from BrepData
    static pShape makeShape(const std::vector<Base::Int>& model, const std::vector<Geom::Pnt>& vertices, std::vector<PNTS>& defectPolygons);
    /// Makes a shape from BrepData
    static void makeShapeAsync(const std::vector<int>& model,
                               const std::vector<Geom::Pnt>& vertices,
                               std::function<void(pShape newShape, std::vector<PNTS> defectPolygons)> onShapeMadeCB);
    /// Makes shapes from BrepData in parallel
    static bool makeShapes_parallel(const std::vector<pConstBrepData>& breps, std::map<pConstBrepData, pShape>& shapes);

    /// Makes an open or closed shape from a vector of pFaces. The faces are stitched or sewn together within given tolerance if possible. If stitch
    /// returns more than one body, this method returns compound shape from all resulted bodies.
    static pShape makeShape(const std::vector<pFace>& faces, double precision = Geom::Precision::linear_Resolution());
    /// Makes a shape from a vector of pFaces. The faces are not stitched together and may be unconnected.
    static pShape makeFaceSet(const std::vector<pFace>& faces);
    /// Makes a shape from BrepData. The faces are not stitched together and may be unconnected. No faces with voids are allowed!!!
    static pShape makeFaceSet(pConstBrepData data);
    /// Makes a compound or combined shape from a vector of pShapes. The shapes are copied. The copies are not merged/united or tested for
    /// intersections. They may be unconnected.
    static pShape makeCompound(const std::vector<pConstShape>& shapes);
    /// Makes a shape from a curve. If the curve is bounded startParam and endParam can be omitted.
    static pShape makeShape(Core::DocObject* curve, double startParam = 0, double endParam = 0);

    /// Returns the number of lumps in the shape
    static int getLumpsCount(pConstTopologicalItem item);
    /// Returns the number of faces in the shape
    static int getFaceCount(pConstTopologicalItem item);
    /// Returns the number of wires in the shape
    static int getWireCount(pConstTopologicalItem item);
    /// Returns the number of edges in the shape
    static int getEdgeCount(pConstTopologicalItem item);
    /// Returns the number of vertices in the shape
    static int getVertexCount(pConstTopologicalItem item);
    /// Returns number of polygons in a shape
    static int getPolygonCount(pConstTopologicalItem item, Topo::ShapeTessellationQuality quality);

    /// Returns the face at index 'idx'. Returns nullptr if index is out of bounds.
    static pConstFace getFaceByIndex(pConstTopologicalItem item, int idx);
    /// Returns the wire at index 'idx'. Returns nullptr if index is out of bounds.
    static pConstWire getWireByIndex(pConstTopologicalItem item, int idx);
    /// Returns the edge at index 'idx'. Returns nullptr if index is out of bounds.
    static pConstEdge getEdgeByIndex(pConstTopologicalItem item, int idx);
    /// Returns the vertex at index 'idx'. Returns nullptr if index is out of bounds.
    static pConstVertex getVertexByIndex(pConstTopologicalItem item, int idx);

    /// Returns the index of the shell in this shape. Returns -1 if shell is not part of this shape
    static int getIndexFromShell(pConstTopologicalItem item, pConstShell shell);
    /// Returns the index of the face in this shape. Returns -1 if face is not part of this shape
    static int getIndexFromFace(pConstTopologicalItem item, pConstFace face);

    /// Returns the indexes of the faces in this shape. Returns -1 if face is not part of this shape
    static std::vector<int> getIndexesFromFaces(pConstTopologicalItem item, const std::vector<pConstFace> faces);

    /// Returns the index of the wire in this shape. Returns -1 if wire is not part of this shape
    static int getIndexFromWire(pConstTopologicalItem item, pConstWire wire);
    /// Returns the index of the edge in this shape. Returns -1 if edge is not part of this shape
    static int getIndexFromEdge(pConstTopologicalItem item, pConstEdge edge);
    /// TODO -> This method is wrong since one gp_Pnt can correspond to more than one index
    static int getIndexFromVertex(pConstTopologicalItem item, const Geom::Pnt& v);
    /// Return the index of vertex 'vtx'. Returns -1 if vertex is not part of this shape
    static int getIndexFromVertex(pConstTopologicalItem item, pConstVertex vtx);

    /// Returns the shells of the shape
    static std::vector<pConstShell> getShells(pConstTopologicalItem item);
    /// Returns the faces of the shape
    static std::vector<pConstFace> getFaces(pConstTopologicalItem item);
    /// Returns the faces of the shape as Copy
    static std::vector<pFace> getFacesAsCopy(pConstTopologicalItem item);
    /// Returns the wires of the shape
    static std::vector<pConstWire> getWires(pConstTopologicalItem item);
    /// Returns the edges of the shape
    static std::vector<pConstEdge> getEdges(pConstTopologicalItem item);
    /// Returns the visible edges of the shape
    static std::vector<VisibleEdge> getEdges_visible(std::vector<pConstShape> shapes,
                                                     const Geom::Pnt& cam_position,
                                                     const Geom::Pnt& cam_target,
                                                     bool cam_perspective = true);
    /// Returns the vertices of the shape
    static std::vector<pConstVertex> getVertices(pConstTopologicalItem item);
    /// Returns the indices of all faces that contain the vertex of index 'vertexIdx'
    static std::vector<int> getAdjacentFaceIndicesFromVertexIndex(pConstTopologicalItem item, int vertexIdx);
    /// Returns all adjacent faces of an edge in a shape
    static std::vector<pConstFace> getAdjacentFacesFromEdge(pConstTopologicalItem item, pConstEdge edge);
    /// Returns edge indices of the face with index 'faceIndex'
    static std::vector<int> getEdgeIndicesFromFace(pConstTopologicalItem item, int faceIndex);
    /// Returns sorted vertex indices of the wire with index 'wireIdx'
    static std::vector<int> getVertexIndicesFromWire(pConstTopologicalItem item, int wireIdx);
    /// Returns wire indices of the face with index 'faceIdx'
    static std::vector<int> getWireIndicesFromFace(pConstTopologicalItem item, int faceIdx);
    /// Returns the vertices of a shape as a vector of points
    static void getVerticesAsPoints(pConstTopologicalItem item, std::vector<Geom::Pnt>& vertices);
    /// Returns the bounding box of the shape
    static Geom::Bnd_Box getBoundingBox(pConstTopologicalItem item);
    /// Returns the transform of the shape
    static Geom::Trsf getTransform(pConstShape shape);
    /// Calculates the local axes for the shape that 'fit the best'. The longest linear edge is taken as the length axis and the biggest face area's
    /// normal vector is taken as the width direction.
    static bool calculateLocalAxes(pConstShape shape, Geom::Ax2& localAxes);
    ///
    static bool calculateDetail(pConstShape shape, CA_Detail& detail, const CA_Snap& snap);
    /// Casts a shape to a solid. Returns nullptr if cast is not possible
    static pSolid cast2Solid(pShape shape);
    /// Casts a shape to a compound. Returns nullptr if cast is not possible
    static pCompound cast2Compound(pShape shape);
    /// Casts a shape to a mesh. Returns nullptr if cast is not possible
    static pMesh cast2Mesh(pShape shape);
    /// Casts a shape to a solid. Returns nullptr if cast is not possible
    static pConstSolid cast2ConstSolid(pConstShape shape);
    /// Casts a shape to a compound. Returns nullptr if cast is not possible
    static pConstCompound cast2ConstCompound(pConstShape shape);
    /// Casts a shape to a mesh. Returns nullptr if cast is not possible
    static pConstMesh cast2ConstMesh(pConstShape shape);
    /// Returns the volume of a shape. Returns 0 if shape has no volume
    static double getVolume(pConstTopologicalItem item);
    /// Computes the center of gravity of a shape. Returns false in case of error
    static bool getCentroid(pConstShape shape, Geom::Pnt& centroid);
    ///
    static void setNeedMassUpdate(pConstShape shape, bool on);
    /// Update the transformation of the shape and its bounding box
    static void updateShapeTransform(pConstShape shape, const Geom::Trsf& transform);
    /// Writes a shape to ostream
    static bool write(pConstShape shape, std::ostream& writer);
    /// Writes a shape to ostream
    static bool write(pConstShape shape, Base::AbstractWriter& writer);
    /// Writes the shape in the give format
    static bool write(const std::string& format, pConstShape shape, const Base::String& fileName);
    /// Writes the shapes in the give format
    static bool write(const std::string& format, std::vector<pConstShape> shapes, const Base::String& fileName);
    /// Writes the shapes in an ACIS binary or text file. ACIS Attributes should be attached to the shape before exporting them. If 'major_version ==
    /// -1' it takes the latest version.
    static bool writeAcisFile(std::vector<pConstShape> shapes,
                              const Base::String& fileName,
                              bool isText,
                              int major_version = -1,
                              int minor_version = -1,
                              double scale = 1.);
    /// Append the shapes in an ACIS binary or text file. ACIS Attributes should be attached to the shape before exporting them. If 'major_version ==
    /// -1' it takes the latest version.
    static bool appendAcisFile(std::vector<pConstShape> shapes,
                               const Base::String& fileName,
                               bool isText,
                               int major_version = -1,
                               int minor_version = -1,
                               double scale = 1.);
    /// Checks if shape can be written in given format
    static bool canWriteAs(const std::string& format, pConstShape shape);
    /// Returns the save format
    static std::string getWriteFormat(pConstShape shape);
    /// Reads a shape from istream in given format
    static pShape read(const std::string& format, std::istream& reader);
    /// Reads shape in given format from data
    static pShape read(const std::string& format, const std::string& data, float version);
    /// Reads shape from fileName in given format
    /*DEPRECATED("Pass fileName as Base::String.") */ static pShape read(const std::string& format, const std::string& fileName);
    /// Reads shape from fileName in given format
    static pShape read(const std::string& format, const Base::String& fileName);

    /** @name Boolean Operations */
    //@{
    static bool intersectBBoxes(pConstShape shape1, pConstShape shape2);
    static pShape cut(pConstShape base, pConstShape tool, bool* ok = 0);
    static pShape cut(pConstShape base, const std::vector<pConstShape> tools, bool* ok = 0);
    static pShape fuse(pConstShape base, pConstShape tool, bool* ok = 0);
    static pShape common(pConstShape base, pConstShape tool, bool* ok = 0);
    static pShape section(pConstShape base, pConstShape tool, bool* ok = 0);
    static pShape s_cut(pConstShape base, pConstShape tool);
    static pShape s_common(pConstShape base, pConstShape tool);
    static pShape cutWithPlane(pConstShape aBlank, const Geom::Pln& aPlane, bool* ok = 0);
    static pShape splitByPlane(pConstShape aBlank, const Geom::Pln& aPlane, bool* ok = 0);
    //@}

    /// Creates a copy of the shape and transforms the copy
    static pShape transformed(pConstShape base, const Geom::Trsf& t);
    /// Convenience method: Creates a copy of the shape and moves the copy
    static pShape moved(pConstShape base, const Geom::XYZ& move);
    /// Creates a copy of the shape and scales the copy. The scale can be non-uniform.
    static pShape scaled(pConstShape base, const Geom::XYZ& scale);
    ///
    /// Checks if the shape is Null
    static bool isNull(pConstShape shape);

    /// Checks if the shape is valid. Check level can be between 10 (fast, but not profound) and 70 (slow and profound)
    static bool isValid(pConstShape shape, int checkLevel = 30);
    /// Checks if the shape is valid. Check level can be between 10 (fast, but not profound) and 70 (slow and profound)
    static bool isValid(pConstWire wire, int checkLevel = 30);
    /// Checks if the shape is valid. Check level can be between 10 (fast, but not profound) and 70 (slow and profound)
    static bool isValid(pConstFace face, int checkLevel = 30);
    /// Checks if the shape is valid. Check level can be between 10 (fast, but not profound) and 70 (slow and profound)
    static bool isValid(pConstVertex vertex, int checkLevel = 30);
    /// Checks if the shape is valid. Check level can be between 10 (fast, but not profound) and 70 (slow and profound)
    static bool isValid(pConstEdge edge, int checkLevel = 30);
    /// Checks if the shape is valid in cadwork3d. The checking level and type of checking are identical to the one in cadwork3d.
    static bool isValidInCadwork3d(pConstTopologicalItem shape);
    /// Checks if TopologicalItems are equal. Two items are equal if they have the same underlying pointer
    static bool isEqual(pConstTopologicalItem shape1, pConstTopologicalItem shape2);
    /// Returns geometric information about the item (like mass etc.)
    static Topo::GeometricInformation getGeometricInformation(pConstTopologicalItem item);
    /// Returns geometric information about the horizontal and vertical faces of the shape
    static void getAxesOrientedSurfaces(pConstShape shape, double& XYSurface, double& XZSurface, double& YZSurface);
    static void getVerticalAndHorizontalFaceAreas(pConstShape shape,
                                                  double& verticalFaceSurface,
                                                  std::vector<double>& verticalFaceSurfaces,
                                                  double& verticalLargestFaceSurface,
                                                  double& horizontalFaceSurface);
    /// Returns geometric information about the horizontal and vertical faces of the shape
    static void getVerticalAndHorizontalFaceAreas(pConstShape shape,
                                                  Base::Double& verticalFaceSurface,
                                                  std::vector<double>& verticalFaceSurfaces,
                                                  Base::Double& verticalLargestFaceSurface,
                                                  Base::Double& horizontalFaceSurface);
    /// Returns projected area from top. Equal to getVisibleProjectedAreaFrom(shape, Geom::Dir(0, 0, -1), areaFromTopMesh).
    static double getAreaFromTop(pConstShape shape, pMesh* areaFromTopMesh = nullptr);
    // Returns area of the largest face of the shape
    static double getLargestFaceArea(pConstShape shape);
    // Returns normal of the largest face of the shape
    static Geom::Dir getLargestFaceNormal(pConstShape shape);
    /// Makes a copy of the shape
    static pShape copy(pConstShape shape, bool deepCopy = true);
    /// Returns a test element - for testing only!
    static App::Element* makeDbgElementFromShape(Core::CoreDocument* doc, pConstShape shape, const Base::Color& color = Base::Color(204, 204, 204));
    /// Returns a test element - for testing only!
    static App::SubElement* makeDbgSubElementFromShape(Core::CoreDocument* doc,
                                                       pConstShape shape,
                                                       const Base::Color& color = Base::Color(204, 204, 204));
    /// Creates a mesh from the shape's triangulation. Returns nullptr if there is no triangulation. If the shape is a mesh returns a triangulated
    /// deep copy.
    static pMesh triangulationToMesh(pConstShape shape);
    /// Checks if the shape consists only of planar faces
    static bool isFaceted(pConstTopologicalItem shape);
    /// Checks if any of the faces in shape has voids
    static bool hasVoids(pConstTopologicalItem shape);
    /// Returns a new shape where all planar faces of 'shape' are merged
    static pShape mergePlanarFaces(pConstShape shape);
    ///	Converts an advanced BRep (with NURBS) into a faceted BRep
    static bool convertToPolygonalFaces(pConstShape shape, std::vector<pFace>& polyFaces, bool precise = false);
    /// Returns true if at least one of the shape's faces is NURBS face (see Topo::FaceTool::isNurbs())
    static bool hasNurbsFace(pConstShape shape);
    /// Checks if the shape has a triangulation ( = the shape is tessellated )
    static bool hasTriangulation(pConstShape shape);
    /// Returns vertex of the shape that is closest to the given point (if there are more vertices in the same distance returns the first one found)
    static pConstVertex getClosestVertexToPoint(pConstTopologicalItem item, const Geom::Pnt& p);
    /// Checks whether a shape consists of faces. In case of a compound the method will
    /// return true if ONE shape in the compound has a face. Also the flag
    /// 'allSubShapesHaveFaces' will be set depending on whether all of the sub-shapes
    /// have faces or not.
    static bool hasFaces(pConstShape shape, bool& allSubShapesHaveFaces);
    /// Reads in a SAT file and converts each ACIS BODY into a pShape.
    static std::vector<pShape> getShapesFromAcisFile(const Base::String& fileName, double scaleFactor = 1., std::function<int(int)> callback = 0);
    /// Read a Brep
    static pShape importBrep(Base::String filename);
    /// Extrudes a wire in the given extrudedDirection with the given depth. It returns nullptr on failure
    static pShape extrudedWire(pConstWire wire, const Geom::Dir& extrudedDirection, double depth, double precision);
    /// Thickens a shape consisting of sheets. If input shape is not a single sided sheet the function tries to convert it into one.
    static pShape thickenSheets(pConstShape shape, double thickness, bool doubleSided /* = false*/, Base::String& errorInfo);
    /// Returns a deformed shape, based on a base point and a transformation.
    static pShape deformed(pConstShape shape, const Geom::GTrsf& t, const Geom::Pnt& p);
    /// Returns a mirrored shape.
    static pShape mirrored(pConstShape shape, const Geom::Ax2& ax);
    /// Performs a clash of two shapes and reports if they touch one another
    static Topo::ToolOutcome clash(pConstShape shape1, pConstShape shape2, bool& hasClash);
    /// Perform a real clash of two shapes and report the way in which these shapes clash
    static Topo::ToolOutcome clashBodies(pConstShape shape1,
                                         pConstShape shape2,
                                         Topo::BodyClashType& clashType,
                                         Topo::ClashMode clashMode = Topo::ClashMode::CLASH_CLASSIFY_BODIES);
    static Topo::ToolOutcome createContactFaces(pConstShape aBaseShape, pConstShape aToolShape, std::vector<pConstFace>& aContactFaces);
    static Topo::ToolOutcome createContactFaces(const std::vector<pConstShape>& aBaseShapes,
                                                const std::vector<pConstShape>& aToolShapes,
                                                std::vector<pConstFace>& aContactFaces);

    /// Checks if the shape consists of one single wire and no faces. Returns the wire or nullptr
    static pConstWire isSingleWire(pConstShape shape);
    /// Checks if the shape consists of one single face. Returns the face or nullptr
    static pConstFace isSingleFace(pConstShape shape);
    /// Checks if the shape consists of one single wire with one edge and no faces. Returns the edge or nullptr
    static pConstEdge isSingleEdge(pConstShape shape);
    /// Checks if the shape consists of one wire with a single vertex but no edges or faces. Returns the vertex or nullptr
    static pConstVertex isSingleVertex(pConstShape shape);
    /// Checks if the shape is an open or closed shell
    static bool isShell(pConstShape shape);
    /// Checks if the shape is an open shell
    static bool isOpenShell(pConstShape shape);
    /// Checks if the shape is a closed shell
    static bool isClosedShell(pConstShape shape);
    /// Checks if the shape is a closed solid
    static bool isClosedSolid(pConstShape shape);
    /// Checks if the shape is a wire.
    static bool isWire(pConstShape shape);
    /// Checks if the shape consists of more than one sub-shape.
    static bool isCompound(pConstShape shape);
    /// Checks if the shape is a mesh.
    static bool isMesh(pConstShape shape);
    /// Checks if the shape is a vertex.
    static bool isVertex(pConstShape shape);
    /// Checks if shape is an ExtrudedAreaSolid and returns the parameters
    static bool isExtrudedAreaSolid(pConstShape aShape,
                                    Geom::Ax2& aPosition,
                                    double& aLength,
                                    pConstFace& aProfile,
                                    BuildingElementHintEnum aHint = BuildingElementHintEnum::NO_HINT);
    /// Checks if shape is a cylinder and returns the parameters
    static bool isCylinder(pConstShape shape, Geom::Ax2& position, double& length, double& radius);

    /// Get Attribute from Shape
    static bool getAttributeInteger(pConstTopologicalItem shape, const Base::String& name, int& value);
    /// Set Attribute to Shape
    static bool setAttributeInteger(pConstTopologicalItem shape, const Base::String& name, int value);
    /// Remove Attribute from Shape
    static bool removeAttribute(pConstTopologicalItem shape, const Base::String& name);
    /// Get Attribute to Shape
    static bool getAttributeString(pConstTopologicalItem shape, const Base::String& name, Base::String&);
    /// Set Attribute to Shape
    static bool setAttributeString(pConstTopologicalItem shape, const Base::String& name, const Base::String&);
    /// Set Attribute to Shape, Don't copy attribute at Copy/Slip/Merge
    static bool setAttributeStringNonCopy(pConstTopologicalItem shape, const Base::String& name, const Base::String&);
    /// Get Attribute-Count
    static size_t getAttributeCount(pConstTopologicalItem shape);
    /// Sets the cadwork SAT attributes
    static bool setCdwkSATAttributes(pConstShape shape, const Topo::Cdwk_SAT_Attributes& att);
    /// Deletes the cadwork SAT attributes
    static void releaseCdwkSATAttributes(pConstShape shape);

    /// Removes all unnecessary faces, wires, edges of the shape
    static bool cleanupShape(pShape shape);

    static bool hasSliverFaces(pConstShape shape);
    static pShape removedSliverFaces(pConstShape shape, double aTolerance = -1);

    /// Intersects two shapes and imprints the intersection graph on BOTH shapes (if a closed loop of edges is created, a new face is made).
    static bool imprint(pShape base, pShape tool);

    /// Make a RayPick
    static Topo::ToolOutcome rayPick(const std::vector<pConstTopologicalItem>& targets, const CA_Ray& ray, Topo::RayHitVector& found);
    /// Removes the faceting ( the triangle/mesh data ) associated with this item.
    static void removeFaceting(pConstTopologicalItem item);
    /// Get RGB values associated with this shape. Useful if color is defined by an ACIS attribute when importing files.
    static bool getColorRGB(pConstShape shape, int& r, int& g, int& b);

    template <class _InputIterator, class _Function>
    static void do_parallel(_InputIterator first, _InputIterator last, _Function fn)
    {
        while (first != last)
        {
            fn(*first);
            ++first;
        }
    }

    static pShape skinning(Base::String& errorInfo,
                           const Topo::SkinningOptions& skinOptions,
                           const double& precision = Geom::Precision::linear_Resolution());
    static pShape sweeping(Base::String& errorInfo, const Topo::SweepingOptions& sweepOptions);

    static pShape pathExtrusionFixVertical(Base::String& errorInfo, PathExtrusionFixVerticalOptions& options);

    /// Returns the global resolution absolute.
    static double getModelingTolerance();
    static Topo::ThreadPool* getThreadPool();
    static void transformShape2LocalSpaceOfElement(App::Element* elem, pShape shape);
    static bool hasPolyHedral();
    static bool getModelFromPolyHedral(pShape shape, std::vector<int>& model, std::vector<Geom::Pnt>& vertices);
    static pShape makePolyHedral(const std::vector<int>& model,
                                 const std::vector<Geom::Pnt>& vertices,
                                 bool checkShape,
                                 std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    static bool is_polyhedral_body(BODY const* iBody);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API

    static std::vector<Geom::Pnt> getIntersectionPoints(pConstShape shape, const std::vector<pConstShape> shapes);
    static std::vector<Geom::Pnt> getAllIntersectionPoints(const std::vector<pConstShape> shapes);
    static void getAllIntersectionPointsIn2DMode(const std::vector<pConstShape>& shapes,
                                                 const Geom::Pnt& pnt,
                                                 const double& distance,
                                                 std::vector<Geom::Pnt>& intersectionPoints);
    static void getAllIntersectionPointsWithLineIn2DMode(const std::vector<pConstShape>& shapes,
                                                         const Geom::Pnt& linePnt1,
                                                         const Geom::Pnt& linePnt2,
                                                         std::vector<Geom::Pnt>& intersectionPoints);
    // convenience method
    static void getAllIntersectionPointsWithLineIn2DMode(pConstShape shape,
                                                         const Geom::Pnt& linePnt1,
                                                         const Geom::Pnt& linePnt2,
                                                         std::vector<Geom::Pnt>& intersectionPoints);

    static pShape createShell(pConstShape shape);
    static pShape createSheet(pConstShape shape, bool doubleSided);
    static std::vector<pShape> splitLumps(pConstShape shape);
    /// Makes an open or closed shapes from a vector of pFaces. The faces are stitched or sewn together within given tolerance if possible.
    static bool makeShapes(const std::vector<pFace>& faces, std::vector<pShape>& shapes, double precision = Geom::Precision::linear_Resolution());

    /// create a Element
    static Topo::ToolOutcome createElementFromShape(Core::CoreDocument* doc,
                                                    pConstShape shape,
                                                    App::Element*& newElement,
                                                    bool auxiliary = false,
                                                    App::Element* sample = nullptr);
    static size_t getShapeCount();
    static void shapeCountInc();
    static void shapeCountDec();
    /// Returns the sizes of the bounding box of the shape
    static bool getBoundingBoxSizes(pConstTopologicalItem item, Geom::XYZ& sizes);  //
    static pShape simplifyShape(pConstShape shape, const SimplifyOptions& opts);
    static pShape offsetShape(pConstShape shape, double offset);
    static void debugShape(pConstShape shape, int checkLevel, ShapeInfo& info);
    static bool isManifold(pConstShape shape);
    static bool restoreGlobalAttachment(Base::GlobalAttachment* gAtta, std::istream*, uint64_t streamsize, const Base::String& entryName);
    static int getFaceIndexByPointOnFace(pConstTopologicalItem shape, const Geom::Pnt& p);
    static std::vector<int> getFaceIndexesByPointOnFace(pConstTopologicalItem shape, const Geom::Pnt& p);

    static void getFacesByMaxNormalToVectorAngle(pConstShape aShape,
                                                 std::map<int, Geom::Vec> aDirectionsToSortBy,
                                                 std::map<int, std::vector<pConstFace> >& aFacesListMap,
                                                 float aMaxAngleRad = 0.75);
    /// Gets the TopoDS_Shape of 'shape'. Returns 'true' on success, 'false' if shape has no TopoDS_Shape or the TopoDS_Shape is Null.
    static bool getTopoDS_Shape(pConstTopologicalItem shape, TopoDS_Shape& topoShape);

    static bool getEntityAttribute_Int(ENTITY* ent, int& v);
    static bool setEntityAttribute_Int(ENTITY* ent, int v);
    static double getSurfaceArea(pConstTopologicalItem item);
    /// Area of faces, which are visible from given orthogonal camera direction.
    static double getVisibleAreaFrom(pConstShape shape, const Geom::Dir& cameraDir, pMesh* resultMesh = nullptr);
    /// Area of faces, which are visible from given orthogonal camera direction, projected to camera plane.
    static double getVisibleProjectedAreaFrom(pConstShape shape, const Geom::Dir& cameraDir, pMesh* resultMesh = nullptr);

    static bool hasOnlyLineWires(pConstShape shape);

    /// @cond INTERNAL
    /// Sets the OCC ShapeTool. For internal use only.
    static void __setOCCShapeTool__(Topo::ShapeTool* tool) { _occTool = tool; }
    /// Sets the ACIS ShapeTool. For internal use only.
    static void __setAcisShapeTool__(Topo::ShapeTool* tool) { _acisTool = tool; }
    /// Sets the default ShapeTool. For internal use only.
    static void __setDefaultShapeTool__(Topo::ShapeTool* tool) { _defaultTool = tool; }
    /// Sets Inventor shape tool. For internal use only.
    static void __setInventorShapeTool__(Topo::ShapeTool* tool) { _inventorTool = tool; }
    /// Sets OMF shape tool. For internal use only.
    static void __setOMFShapeTool__(Topo::ShapeTool* tool) { _omfTool = tool; }
    /// Sets acis mesh shape tool. For internal use only.
    static void __setAcisMeshShapeTool__(Topo::ShapeTool* tool) { _acisMeshShapeTool = tool; }
    /// This is a helper function for refactoring. Only for internal use.
    static pConstShape getFirstShape_Helper(App::Element* elem);



protected:
    /// Gets the Acis ENTITY of 'shape'. Returns NULL on failure
    static ENTITY* getAcisEntity(pConstTopologicalItem item);

    virtual pShape _makeShape(pVertex vertex);
    virtual pShape _makeShape(pEdge edge);
    virtual pShape _makeShape(pWire wire, double precision);
    virtual pShape _makeShape(pFace face);
    virtual pShape _makeShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    virtual pShape _makeShape(BODY* aBody);
    virtual pShape _makeLazyFacetedBrepShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    virtual pShape _makeInventorMeshShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    virtual pShape _makeInventorMeshShape(pIndexedMesh p);
    virtual pIndexedMesh _makeIndexedMesh(pConstBrepData data, std::vector<PNTS>& defectPolygons, bool createEdges = false);
    virtual pIndexedMesh _makeIndexedMesh(pConstShape input, bool createEdges = false);
    virtual pShape _makeOMFMeshShape(pConstBrepData data, std::vector<PNTS>& defectPolygons);
    virtual pShape _makeAcisShape(pShape input);
    virtual bool _createBrepData(pConstShape input, pBrepData data);
    virtual pShape _makeShape(const std::vector<pFace>& faces, double tolerance);
    virtual bool _makeShapes(const std::vector<pFace>& faces, std::vector<pShape>& shapes, double precision);
    virtual pShape _makeShape(const std::vector<int>& model,
                              const std::vector<Geom::Pnt>& vertices,
                              std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    virtual bool _makeShapes_parallel(const std::vector<pConstBrepData>& breps, std::map<pConstBrepData, pShape>& shapes);
    virtual pShape _makeFaceSet(const std::vector<pFace>& faces);
    virtual pShape _makeFaceSet(pConstBrepData data);
    virtual pShape _makeCompound(const std::vector<pConstShape>& shapes);
    virtual int _getFaceCount(pConstTopologicalItem item);
    virtual int _getWireCount(pConstTopologicalItem item);
    virtual int _getEdgeCount(pConstTopologicalItem item);
    virtual int _getVertexCount(pConstTopologicalItem item);
    virtual int _getLumpsCount(pConstTopologicalItem item);
    virtual int _getPolygonCount(pConstTopologicalItem item, Topo::ShapeTessellationQuality quality);
    virtual pShape _makeShape(Core::DocObject* curve, double startParam, double endParam);

    virtual pConstFace _getFaceByIndex(pConstTopologicalItem item, int idx);
    virtual pConstWire _getWireByIndex(pConstTopologicalItem item, int idx);
    virtual pConstEdge _getEdgeByIndex(pConstTopologicalItem item, int idx);
    virtual pConstVertex _getVertexByIndex(pConstTopologicalItem item, int idx);

    virtual std::vector<pConstFace> _getFaces(pConstTopologicalItem item);
    virtual std::vector<pConstWire> _getWires(pConstTopologicalItem item);
    virtual std::vector<pConstEdge> _getEdges(pConstTopologicalItem item);
    virtual std::vector<pConstEdge> _getAllEdges(pConstTopologicalItem item);
    virtual std::vector<pConstVertex> _getVertices(pConstTopologicalItem item);


    virtual int _getIndexFromFace(pConstTopologicalItem item, pConstFace face);
    virtual std::vector<int> _getIndexesFromFaces(pConstTopologicalItem item, const std::vector<pConstFace> faces);
    virtual int _getIndexFromWire(pConstTopologicalItem item, pConstWire wire);
    virtual int _getIndexFromEdge(pConstTopologicalItem item, pConstEdge edge);
    virtual int _getIndexFromVertex(pConstTopologicalItem item, const Geom::Pnt& v);
    virtual int _getIndexFromVertex(pConstTopologicalItem item, pConstVertex vtx);

    virtual std::vector<int> _getAdjacentFaceIndicesFromVertexIndex(pConstTopologicalItem item, int vertexIdx);
    virtual std::vector<pConstFace> _getAdjacentFacesFromEdge(pConstTopologicalItem item, pConstEdge edge);
    virtual void _getVerticesAsPoints(pConstTopologicalItem item, std::vector<Geom::Pnt>& vertices);
    virtual Geom::Bnd_Box _getBoundingBox(pConstTopologicalItem item);

    virtual Geom::Trsf _getTransform(pConstShape shape);
    virtual bool _calculateDetail(pConstShape shape, CA_Detail& detail, const CA_Snap& snap);

    virtual pSolid _cast2Solid(pShape shape);
    virtual pCompound _cast2Compound(pShape shape);
    virtual pMesh _cast2Mesh(pShape shape);
    virtual pConstSolid _cast2ConstSolid(pConstShape shape);
    virtual pConstCompound _cast2ConstCompound(pConstShape shape);
    virtual pConstMesh _cast2ConstMesh(pConstShape shape);

    virtual double _getVolume(pConstTopologicalItem item);
    virtual double _getSurfaceArea(pConstTopologicalItem item);
    virtual bool _getCentroid(pConstShape shape, Geom::Pnt& centroid);
    virtual void _setNeedMassUpdate(pConstShape shape, bool on);
    virtual void _updateShapeTransform(pConstShape shape, const Geom::Trsf& transform);
    virtual bool _write(pConstShape shape, std::ostream& writer);
    virtual bool _write(pConstShape shape, Base::AbstractWriter& writer);

    virtual std::string _getWriteFormat(pConstShape shape);

    virtual bool _write(const std::string& format, pConstShape shape, const Base::String& fileName);
    virtual bool _write(const std::string& format, std::vector<pConstShape> shapes, const Base::String& fileName);
    virtual bool _writeAcisFile(std::vector<pConstShape> shapes,
                                const Base::String& fileName,
                                bool isText,
                                int major_version,
                                int minor_version,
                                double scale);
    virtual bool _appendAcisFile(std::vector<pConstShape> shapes,
                                 const Base::String& fileName,
                                 bool isText,
                                 int major_version,
                                 int minor_version,
                                 double scale);
    virtual bool _canWriteAs(const std::string& format, pConstShape shape);
    virtual bool _intersectBBoxes(pConstShape shape1, pConstShape shape2);

    virtual pShape _cut(pConstShape base, pConstShape tool, bool* ok);
    virtual pShape _cut(pConstShape base, const std::vector<pConstShape> tools, bool* ok);
    virtual pShape _fuse(pConstShape base, pConstShape tool, bool* ok);
    virtual bool _imprint(pShape base, pShape tool);
    virtual pShape _common(pConstShape base, pConstShape tool, bool* ok);
    virtual pShape _section(pConstShape base, pConstShape tool, bool* ok);
    virtual pShape _s_cut(pConstShape base, pConstShape tool);
    virtual pShape _s_common(pConstShape base, pConstShape tool);
    virtual pShape _cutWithPlane(pConstShape aBlank, const Geom::Pln& aPlane, bool* ok = 0);
    virtual pShape _splitByPlane(pConstShape aBlank, const Geom::Pln& aPlane, bool* ok = 0);

    virtual pShape _transformed(pConstShape base, const Geom::Trsf& t);
    virtual pShape _moved(pConstShape base, const Geom::XYZ& xyz);
    virtual pShape _scaled(pConstShape base, const Geom::XYZ& scale);
    virtual bool _isValid(pConstShape shape, int checkLevel);
    virtual bool _isValid(pConstFace face, int checkLevel);
    virtual bool _isValid(pConstWire wire, int checkLevel);
    virtual bool _isValid(pConstVertex vertex, int checkLevel);
    virtual bool _isValid(pConstEdge edge, int checkLevel);
    virtual bool _isValid(pShape shape, int checkLevel);
    virtual bool _isValid(pFace face, int checkLevel);
    virtual bool _isValid(pWire wire, int checkLevel);
    virtual bool _isValid(pVertex vertex, int checkLevel);
    virtual bool _isValid(pEdge edge, int checkLevel);
    virtual bool _isValidInCadwork3d(pConstTopologicalItem shape);
    virtual bool _isEqual(pConstTopologicalItem item1, pConstTopologicalItem item2);
    virtual bool _cleanupShape(pShape shape);

    virtual Topo::GeometricInformation _getGeometricInformation(pConstTopologicalItem shape);
    virtual void _getAxesOrientedSurfaces(pConstShape shape, double& XYSurface, double& XZSurface, double& YZSurface);
    virtual void _getVerticalAndHorizontalFaceAreas(pConstShape shape,
                                                    double& verticalFaceSurface,
                                                    std::vector<double>& verticalFaceSurfaces,
                                                    double& verticalLargestFaceSurface,
                                                    double& horizontalFaceSurface);
    virtual double _getVisibleAreaFrom(pConstShape shape, const Geom::Dir& cameraDir, pMesh* resultMesh);
    virtual double _getVisibleProjectedAreaFrom(pConstShape shape, const Geom::Dir& cameraDir, pMesh* resultMesh);
    virtual pShape _copy(pConstShape shape, bool deepCopy);
    virtual App::Element* _makeDbgElementFromShape(Core::CoreDocument* doc, pConstShape shape, const Base::Color& color);
    virtual App::SubElement* _makeDbgSubElementFromShape(Core::CoreDocument* doc, pConstShape shape, const Base::Color& color);
    virtual bool _getTopoDS_Shape(pConstTopologicalItem shape, TopoDS_Shape& topoShape);
    virtual bool _isFaceted(pConstTopologicalItem shape);
    virtual bool _hasVoids(pConstTopologicalItem shape);
    virtual pShape _mergePlanarFaces(pConstShape shape);
    virtual bool _convertToPolygonalFaces(pConstShape shape, std::vector<pFace>& polyFaces, bool precise = false);

    virtual pShape _extrudedWire(pConstWire wire, const Geom::Dir& extrudedDirection, double depth, double precision);
    virtual std::vector<Geom::Pnt> _getIntersectionPoints(pConstShape shape, const std::vector<pConstShape> shapes);
    virtual std::vector<Geom::Pnt> _getAllIntersectionPoints(const std::vector<pConstShape> shapes);
    virtual bool _hasTriangulation(pConstShape shape);
    virtual pShape _createShell(pConstShape shape);
    virtual pShape _createSheet(pConstShape shape, bool doubleSided);

    virtual std::vector<pShape> _splitLumps(pConstShape shape);

    virtual bool _hasFaces(pConstShape shape, bool& allSubShapesHaveFaces);
    virtual bool _isNull(pConstShape shape);
    virtual pShape _deformed(pConstShape shape, const Geom::GTrsf& t, const Geom::Pnt& p);
    virtual std::vector<pShape> _getShapesFromAcisFile(const Base::String& fileName, double scaleFactor = 1., std::function<int(int)> callback = 0);
    virtual pShape _importBrep(const Base::String& filename);
    virtual pShape _mirrored(pConstShape shape, const Geom::Ax2& ax);
    virtual Topo::ToolOutcome _clash(pConstShape shape1, pConstShape shape2, bool& hasClash);
    virtual Topo::ToolOutcome _clashBodies(pConstShape shape1,
                                           pConstShape shape2,
                                           Topo::BodyClashType& clashType,
                                           Topo::ClashMode clashMode = Topo::ClashMode::CLASH_CLASSIFY_BODIES);
    virtual std::vector<VisibleEdge> _getEdges_visible(std::vector<pConstShape> shapes,
                                                       const Geom::Pnt& cam_position,
                                                       const Geom::Pnt& cam_target,
                                                       bool cam_perspective = true);
    virtual Topo::ToolOutcome _createElementFromShape(Core::CoreDocument* doc,
                                                      pConstShape shape,
                                                      App::Element*& newElement,
                                                      bool auxiliary = false,
                                                      App::Element* sample = nullptr);
    virtual bool _getAttributeInteger(pConstTopologicalItem shape, const Base::String& name, int& value);
    virtual bool _setAttributeInteger(pConstTopologicalItem shape, const Base::String& name, int value);
    virtual bool _removeAttribute(pConstTopologicalItem shape, const Base::String& name);
    virtual Topo::ToolOutcome _rayPick(const std::vector<pConstTopologicalItem>& targets, const CA_Ray& ray, Topo::RayHitVector& found);
    virtual void _removeFaceting(pConstTopologicalItem item);
    virtual bool _getColorRGB(pConstShape shape, int& r, int& g, int& b);
    virtual pShape _simplifyShape(pConstShape shape, const SimplifyOptions& opts);
    virtual pShape _offsetShape(pConstShape shape, double offset);
    virtual pShape _thickenSheets(pConstShape shape, double thickness, bool doubleSided, Base::String& errorInfo);

    virtual pShape _skinning(Base::String& errorInfo, const Topo::SkinningOptions&, const double&)
    {
        errorInfo = L"Not implemented";
        return nullptr;
    }
    virtual pShape _sweeping(Base::String& errorInfo, const Topo::SweepingOptions&)
    {
        errorInfo = L"Not implemented";
        return nullptr;
    }

    virtual double _getModelingTolerance();
    virtual void _debugShape(pConstShape shape, int checkLevel, Topo::ShapeInfo& info);
    virtual bool _isManifold(pConstShape shape);
    virtual bool _restoreGlobalAttachment(Base::GlobalAttachment* gAtta, std::istream*, uint64_t streamsize, const Base::String& entryName);

    virtual bool _getAttributeString(pConstTopologicalItem shape, const Base::String& name, Base::String&);
    virtual bool _setAttributeString(pConstTopologicalItem shape, const Base::String& name, const Base::String&);
    // Don't copy attribute at Copy/Slip/Merge
    virtual bool _setAttributeStringNonCopy(pConstTopologicalItem shape, const Base::String& name, const Base::String&);
    virtual size_t _getAttributeCount(pConstTopologicalItem shape);
    virtual int _getFaceIndexByPointOnFace(pConstTopologicalItem shape, const Geom::Pnt& p);
    virtual std::vector<int> _getFaceIndexesByPointOnFace(pConstTopologicalItem shape, const Geom::Pnt& p);

    virtual Topo::ThreadPool* _getThreadPool();
    virtual bool _setCdwkSATAttributes(pConstShape shape, const Topo::Cdwk_SAT_Attributes& att);
    virtual void _releaseCdwkSATAttributes(pConstShape shape) {}
    virtual void _transformShape2LocalSpaceOfElement(App::Element* elem, pShape shape);
    virtual pShape _removedSliverFaces(pConstShape aShape, double aTolerance);
    virtual bool _hasSliverFaces(pConstShape shape);

    virtual bool _hasPolyHedral();
    virtual bool _getModelFromPolyHedral(pShape shape, std::vector<int>& model, std::vector<Geom::Pnt>& vertices);
    virtual pShape _makePolyHedral(const std::vector<int>& model,
                                   const std::vector<Geom::Pnt>& vertices,
                                   bool checkShape,
                                   std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    virtual bool _is_polyhedral_body(BODY const* iBody);

    virtual bool _getEntityAttribute_Int(ENTITY* ent, int& v);
    virtual bool _setEntityAttribute_Int(ENTITY* ent, int v);



#endif
private:
    static bool _hasSameShapeTool(pConstTopologicalItem shape1, pConstTopologicalItem shape2);
    static Topo::ShapeTool* getShapeTool(pConstTopologicalItem item);

    static Topo::ShapeTool* _acisTool;
    static Topo::ShapeTool* _occTool;
    static Topo::ShapeTool* _defaultTool;
    static Topo::ShapeTool* _inventorTool;
    static Topo::ShapeTool* _omfTool;
    static Topo::ShapeTool* _acisMeshShapeTool;

    static size_t _shapeCount;
    /// @endcond
};
}  // namespace Topo