
#include <Geom/GTrsf.h>
#include <OpenLxApp/Geometry.h>
#include <Topo/Shape.h>

FORWARD_DECL(Mesh, InventorImport)

namespace OpenLxApp
{
/*!
 * @brief A mesh imported from an OpenInventor (iv) file.
 *
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT InventorImport : public Geometry
{
    PROXY_HEADER(InventorImport, Mesh::InventorImport, IFC_ENTITY_UNDEFINED)

    DECL_PROPERTY(InventorImport, Transform, Geom::GTrsf)
public:
    ~InventorImport(void);
    void setMesh(pMesh aMesh);
    pConstMesh getMesh() const;

private:
    InventorImport(void) {}
};
}  // namespace OpenLxApp