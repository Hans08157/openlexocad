#pragma once

#include <Draw/OglMaterial.h>
#include <Geom/Pln.h>
#include <Topo/Types.h>


/*
@brief MeshTool
[1] Boundary edges are edges shared by only one face.
*/

namespace Core
{
class CoreDocument;
class Variant;
}
namespace Draw
{
class SurfaceStyle;
}

namespace App
{
class Element;
}

namespace Geom
{
class Pnt2d;
}


namespace Topo
{
struct LX_TOPO_EXPORT LineItem
{
    std::vector<Geom::Pnt> points;
    Draw::OglMaterial material;
};

/**
 * @brief Tools for creating, manipulating and querying Meshes.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT MeshTool
{
public:
    MeshTool(void);
    virtual ~MeshTool(void);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Makes a copy of the mesh
    static pMesh copy(pConstMesh mesh, bool deepCopy = false);
    /// Checks if the mesh is closed ( = it has no boundary edges[1] ).
    static bool isClosed(pConstMesh mesh);
    /// Checks if the mesh is planar ( =  all its points lay on the same plane ).
    static bool isPlanar(pConstMesh mesh);
    /// Creates a mesh from the shape's triangulation. Tessellates the shape if necessary. Returns nullptr if there is no triangulation. If the shape
    /// is a mesh returns a triangulated deep copy.
    static pMesh triangulationToMesh(pConstShape shape);
    /// Creates a mesh from the shape's triangulation. Tessellates the shape if necessary. Returns nullptr if there is no triangulation. If the shape
    /// is a mesh returns a triangulated deep copy.
    static pMesh triangulationToMesh(pConstShape shape, bool highQuality, std::vector<int>* newToOldFaceIdxMap = 0);
    /// Converts a mesh to a BREP shape (shell or solid)
    static pShape convertMesh2Shape(pConstMesh mesh, std::vector<std::vector<Geom::Pnt>>& defectPolygons);
    ///
    static pShape convertMesh2Solid(pConstMesh aMesh, bool prefer_stiching, bool onlyClosedSolid, bool mergePlanarFaces);
    /// Converts a mesh to a Polyhedral (Acis)
    static pShape convertMesh2Polyhedral(pConstMesh mesh, std::vector<std::vector<Geom::Pnt>>& defectPolygons);
    /// Converts a mesh to a BREP shape (shell or solid)
    static pShape convertMesh2Brep_by_Face_Stiching(pConstMesh mesh, std::vector<std::vector<Geom::Pnt>>& defectPolygons);
    /// Converts a mesh to an open or closed shell
    static pShape convertMesh2Shell(pConstMesh mesh, std::vector<std::vector<Geom::Pnt>>& defectPolygons);
    /// Makes a mesh from BrepData
    static pMesh makeMeshFromBrepData(pConstBrepData data);
    /// Makes a mesh from Nodes and Texture-Coordinates
    static pMesh makeMesh(const std::vector<Geom::Pnt>& nodes,
                          const std::vector<int>& model,
                          const std::vector<Geom::Pnt2d>& textureCoords,
                          const std::vector<int>& textureCoordIndices,
                          const std::vector<Geom::Pnt>& normals);
    /// Makes a mesh from Nodes
    static pMesh makeMesh(const std::vector<Geom::Pnt>& nodes, const std::vector<int>& model);

    /// Makes a mesh from Nodes and normals
    static pMesh makeMesh(const std::vector<Geom::Pnt>& nodes, const std::vector<int>& model, const std::vector<Geom::Pnt>& normals);
    /// Reads in a OMF file and converts each OMF into an App::Element
    static std::vector<App::Element*> getElementsFromOMFFile(Core::CoreDocument* doc,
                                                             const Base::String& fileName,
                                                             double scaleFactor = 1.,
                                                             bool terrain = false);

    static bool getMesh(pConstMesh mesh,
                        std::vector<Geom::Pnt>& nodes,
                        std::vector<int>& model,
                        std::vector<Draw::SurfaceStyle>& surfaceStyles,
                        std::vector<int>& faceIndices,
                        std::vector<int>& surfaceStyleIndices,
                        std::vector<Geom::Pnt2d>& textureCoords,
                        std::vector<int>& textureCoordIndices,
                        std::vector<Topo::LineItem>* lineItems = 0);

    static bool getCreaseAngle(pConstMesh mesh, float& angle);

    

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
               /// @cond INTERNAL

    /// Reads in a OMF file and converts each OMF into an App::Element
    static std::vector<App::Element*> getElementsFromOMFFile(Core::CoreDocument* doc,
                                                             const Base::String& fileName,
                                                             double scaleFactor,
                                                             bool terrain,
                                                             std::map<std::string, Core::Variant>* properties,
                                                             bool forceTerrainFrom2dr);

#ifndef SWIG
    /// Reads in a OMF file and converts each OMF into an App::Element
    static std::map<int, std::array<Core::Variant, 6>> getHorizontalPointsFromOMFFile(Core::CoreDocument* doc,
                                                                                      const Base::String& fileName,
                                                                                      std::map<std::string, Core::Variant>* properties,
                                                                                      const double& scaleFactor = 1.);
    static std::map<int, std::array<Core::Variant, 4>> getVerticalPointsFromOMFFile(Core::CoreDocument* doc,
                                                                                    const Base::String& fileName,
                                                                                    std::map<std::string, Core::Variant>* properties,
                                                                                    const double& scaleFactor = 1.);
#endif

    static void getModel(pConstMesh mesh, std::vector<int>& model);
    static void getPoints(pConstMesh mesh, std::vector<Geom::Pnt>& points);


    /// Sets the default MeshTool. For internal use only.
    static void __setDefaultMeshTool__(Topo::MeshTool* tool) { _defaultTool = tool; }
    /// Create OMF file with colors
    static bool writeOmfFile(const std::vector<App::Element*>& elems, const Base::String& fileName);

    static bool getInventorMeshColors(pConstMesh mesh, std::vector<Base::Color>& uniqueColors, std::vector<std::string>* colorNames = 0);

    static pMesh makePlateFast(const std::vector<Geom::Pnt>& points,
                               const std::vector<int>& model,
                               const Geom::Dir& extrudeDir,
                               double thickness,
                               bool askForHoles);  // for mesh without overhangs

    static bool triangulateClosedPolyline(const std::vector<Geom::Pnt> inputPolyLine, std::vector<Geom::Pnt>& nodes, std::vector<int>& model);
    static bool tryToCloseMesh(const pConstMesh& mesh,
                               pMesh& newMesh,
                               const std::vector<unsigned int>* mtlIds = nullptr,
                               std::vector<unsigned int>* newMtlIds = nullptr);

    /// faces are without holes
    static bool section(const pConstMesh& mesh, const Geom::Pln& pln, std::vector<pFace>& faces);
    /// Face from multiple triangles projected to plane of faceIndex face
    static pFace getCreaseAngleFace(const pConstMesh& mesh, double creaseAngle, int faceIndex);
    /// Get border lines and triangles of face defined by crease angle. Pointers can be nullptr if not needed.
    static bool getCreaseAngleFaceMesh(const pConstMesh& mesh,
                                       double creaseAngle,
                                       int faceIndex,
                                       std::vector<Geom::Pnt>* points,
                                       std::vector<int>* linesModel,
                                       std::vector<int>* trianglesModel,
                                       double* area,
                                       std::vector<int>* usedPointsByFace);
    static bool computeCreaseEdges(const pConstMesh& mesh, double creaseAngle, std::vector<std::pair<Geom::Pnt, Geom::Pnt>>& creaseEdges);

protected:
#endif

private:
    virtual pMesh _copy(pConstMesh shape, bool deepCopy);
    virtual bool _isClosed(pConstMesh mesh);
    virtual pMesh _triangulationToMesh(pConstShape shape);
    virtual pMesh _triangulationToMesh(pConstShape shape, bool highQuality, std::vector<int>* newToOldFaceIdxMap);
    static Topo::MeshTool* _defaultTool;

    virtual void _getModel(pConstMesh mesh, std::vector<int>& model);
    virtual void _getPoints(pConstMesh mesh, std::vector<Geom::Pnt>& points);
    virtual pMesh _makeMeshFromBrepData(pConstBrepData data);
    virtual std::vector<App::Element*> _getElementsFromOMFFile(Core::CoreDocument* doc,
                                                               const Base::String& fileName,
                                                               double scaleFactor,
                                                               bool terrain,
                                                               std::map<std::string, Core::Variant>* properties,
                                                               bool forceTerrainFrom2dr);
    virtual std::map<int, std::array<Core::Variant, 6>> _getHorizontalPointsFromOMFFile(Core::CoreDocument* doc,
                                                                                        const Base::String& fileName,
                                                                                        std::map<std::string, Core::Variant>* properties,
                                                                                        const double& scaleFactor);
    virtual std::map<int, std::array<Core::Variant, 4>> _getVerticalPointsFromOMFFile(Core::CoreDocument* doc,
                                                                                      const Base::String& fileName,
                                                                                      std::map<std::string, Core::Variant>* properties,
                                                                                      const double& scaleFactor);
    virtual bool _writeOmfFile(const std::vector<App::Element*>& elems, const Base::String& fileName);
    virtual bool _getInventorMeshColors(pConstMesh mesh, std::vector<Base::Color>& uniqueColors, std::vector<std::string>* colorNames);
    virtual pMesh _makeMesh(const std::vector<Geom::Pnt>& nodes,
                            const std::vector<int>& model,
                            const std::vector<Geom::Pnt2d>& textureCoords,
                            const std::vector<int>& textureCoordIndices,
                            const std::vector<Geom::Pnt>& normals);
    virtual pMesh _makeMesh(const std::vector<Geom::Pnt>& nodes, const std::vector<int>& model);
    virtual pMesh _makeMesh(const std::vector<Geom::Pnt>& nodes, const std::vector<int>& model, const std::vector<Geom::Pnt>& normals);

    virtual bool _getMesh(pConstMesh mesh,
                          std::vector<Geom::Pnt>& nodes,
                          std::vector<int>& model,
                          std::vector<Draw::SurfaceStyle>& surfaceStyles,
                          std::vector<int>& faceIndices,
                          std::vector<int>& surfaceStyleIndices,
                          std::vector<Geom::Pnt2d>& textureCoords,
                          std::vector<int>& textureCoordIndices,
                          std::vector<Topo::LineItem>* lineItems = 0);

    virtual bool _getCreaseAngle(pConstMesh mesh, float& angle);

    virtual pMesh _makePlateFast(const std::vector<Geom::Pnt>& points,
                                 const std::vector<int>& model,
                                 const Geom::Dir& extrudeDir,
                                 double thickness,
                                 bool askForHoles);

    virtual bool _triangulateClosedPolyline( const std::vector<Geom::Pnt> inputPolyLine, std::vector<Geom::Pnt>& nodes, std::vector<int>& model );
    virtual bool _tryToCloseMesh(const pConstMesh& mesh,
                                 pMesh& newMesh,
                                 const std::vector<unsigned int>* mtlIds,
                                 std::vector<unsigned int>* newMtlIds);
    virtual bool _section(const pConstMesh& mesh, const Geom::Pln& pln, std::vector<pFace>& faces);
    virtual pFace _getCreaseAngleFace(const pConstMesh& mesh, double creaseAngle, int faceIndex);
    virtual bool _getCreaseAngleFaceMesh(const pConstMesh& mesh,
                                         double creaseAngle,
                                         int faceIndex,
                                         std::vector<Geom::Pnt>* points,
                                         std::vector<int>* linesModel,
                                         std::vector<int>* trianglesModel,
                                         double* area,
                                         std::vector<int>* usedPointsByFace);
    virtual bool _computeCreaseEdges(const pConstMesh& mesh, double creaseAngle, std::vector<std::pair<Geom::Pnt, Geom::Pnt>>& creaseEdgesusedPointsByFace);

    /// @endcond
};

}  // namespace Topo
