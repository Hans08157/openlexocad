#pragma once

#include <OpenLxApp/Geometry.h>

#include <vector>



FORWARD_DECL(Part, ShellBasedSurfaceModel)

namespace OpenLxApp
{
/*!
 * @brief An IfcShellBasedSurfaceModel represents the shape by a set of open or closed shells.
 * The connected faces within the shell have a dimensionality 2 and are placed in a coordinate space of dimensionality 3.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcshellbasedsurfacemodel.htm" target="_blank">Documentation from IFC4:
 * IfcFaceBasedSurfaceModel</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT ShellBasedSurfaceModel : public Geometry
{
    PROXY_HEADER(ShellBasedSurfaceModel, Part::ShellBasedSurfaceModel, IFCSHELLBASEDSURFACEMODEL)

    DECL_PROPERTY(ShellBasedSurfaceModel, SbsmBoundary, std::vector<pBrepData>)

public:
    ~ShellBasedSurfaceModel(void);

private:
    ShellBasedSurfaceModel(void) {}
};
}  // namespace OpenLxApp
