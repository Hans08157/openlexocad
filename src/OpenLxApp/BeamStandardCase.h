#pragma once
#include <OpenLxApp/Beam.h>
#include <memory>

FORWARD_DECL(App, BeamStandardCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The standard beam, BeamStandardCase, defines a beam with certain constraints for the
 * provision of material usage, parameters and with certain constraints for the geometric representation.
 * The BeamStandardCase handles all cases of beams, that:
 * - have a reference to the MaterialProfileSetUsage defining the material profile association of the beam with the cardinal point of its insertion
 * relative to the local placement.
 * - are consistent in using the correct cardinal point offset of the profile as compared to the 'Axis' and 'Body' shape representation
 * - are based on a sweep of a planar profile, or set of profiles, as defined by the MaterialProfileSet
 * - have an 'Axis' shape representation with constraints provided below in the geometry use definition
 * - have a 'Body' shape representation with constraints provided below in the geometry use definition
 *   - are extruded perpendicular to the profile definition plane
 *   - have a start profile, or set of profiles, that is swept
 *   - the sweeping operation can be linear extrusion, circular rotation, or a sweep along a directrix
 *   - the start profile, or set of profiles can be swept unchanged, or might be changed uniformly by a taper definition
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcbeamstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcBeamStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT BeamStandardCase : public Beam
{
    PROXY_HEADER(BeamStandardCase, App::BeamStandardCase, IFCBEAMSTANDARDCASE)

public:
    virtual ~BeamStandardCase(void);


protected:
    BeamStandardCase() {}
};

}  // namespace OpenLxApp