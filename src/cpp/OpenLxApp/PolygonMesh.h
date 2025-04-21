
#include <Geom/Pnt.h>
#include <OpenLxApp/Geometry.h>
#include <Topo/Shape.h>

#include <vector>

FORWARD_DECL(Mesh, PolygonMesh)

namespace OpenLxApp
{
/*!
 * @brief A Polygon Mesh from triangles and quadrangles.
 *
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT PolygonMesh : public Geometry
{
    PROXY_HEADER(PolygonMesh, Mesh::PolygonMesh, IFCPOLYGONMESH)

    DECL_PROPERTY(PolygonMesh, Polygons, std::vector<int>)
    DECL_PROPERTY(PolygonMesh, Points, std::vector<Geom::Pnt>)
public:
    ~PolygonMesh(void);
    void setMesh(pMesh aMesh);
    pConstMesh getMesh() const;

private:
    PolygonMesh(void) {}
};
}  // namespace OpenLxApp