#pragma once

#include <OpenLxApp/Slab.h>

#include <memory>

FORWARD_DECL(App, Slab)

namespace OpenLxApp
{
/**
 * @brief The standard slab, SlabStandardCase, defines a slab with certain constraints
 * for the provision of material usage, parameters and with certain constraints for the geometric representation.
 * The SlabStandardCase handles all cases of slabs, that:
 * - have a reference to the MaterialLayerSetUsage defining the material layers of the slab with thicknesses
 * - are based on an extrusion of a planar surface as defined by the slab profile
 * - have a constant thickness along the extrusion direction
 * - are consistent in using the correct material layer set offset to the base planar surface in regard to the shape representation
 * - are extruded either perpendicular or slanted to the plane surface
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcslabstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcSlabStandardCase</a>
 *
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT SlabStandardCase : public Slab
{
    PROXY_HEADER(SlabStandardCase, App::Slab, IFCSLABSTANDARDCASE)

public:
    virtual ~SlabStandardCase(void);
    virtual bool setGeometry(std::shared_ptr<Geometry> geo) override;

protected:
    SlabStandardCase() {}
};

}  // namespace OpenLxApp