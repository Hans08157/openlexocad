#pragma once

#include <OpenLxApp/Geometry.h>

#include <vector>



FORWARD_DECL(Part, FaceBasedSurfaceModel)

namespace OpenLxApp
{
/*!
 * @brief A face based surface model is described by a set of connected face sets of dimensionality 2.
 * The connected face sets shall not intersect except at edges and vertices, except that a face in
 * one connected face set may overlap a face in another connected face set, provided the face boundaries are identical.
 * There shall be at least one connected face set. (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcfacebasedsurfacemodel.htm" target="_blank">Documentation from IFC4:
 * IfcFaceBasedSurfaceModel</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT FaceBasedSurfaceModel : public Geometry
{
    PROXY_HEADER(FaceBasedSurfaceModel, Part::FaceBasedSurfaceModel, IFCFACEBASEDSURFACEMODEL)

    DECL_PROPERTY(FaceBasedSurfaceModel, FbsmFaces, std::vector<pBrepData>)

public:
    ~FaceBasedSurfaceModel(void);

private:
    FaceBasedSurfaceModel(void) {}
};
}  // namespace OpenLxApp
