#pragma once
#include <OpenLxApp/Plate.h>

#include <memory>

FORWARD_DECL(App, PlateStandardCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The standard plate, PlateStandardCase, defines a plate with certain constraints for the
 * provision of material usage, parameters and with certain constraints for the geometric representation.
 * The PlateStandardCase handles all cases of plates, that:
 * - have a reference to the MaterialLayerSetUsage defining the material layers of the plate with thicknesses
 *  - are based on an extrusion of a planar surface as defined by the plate profile
 *  - have a constant thickness along the extrusion direction
 *  - are consistent in using the correct material layer set offset to the base planar surface in regard to the shape representation
 *  - are extruded perpendicular to the plane surface
 *
 * The definitions of plate openings and niches are the same as given at the supertype Plate.
 * The same agreements to the special types of plates, as defined in the PredefinedType attribute apply as well.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcplatestandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcPlateStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT PlateStandardCase : public Plate
{
    PROXY_HEADER(PlateStandardCase, App::PlateStandardCase, IFCPLATESTANDARDCASE)

public:
    virtual ~PlateStandardCase(void);

protected:
    PlateStandardCase() {}
};

}  // namespace OpenLxApp