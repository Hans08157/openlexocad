#pragma once
#include <OpenLxApp/Slab.h>

#include <memory>

FORWARD_DECL(App, SlabElementedCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The SlabElementedCase defines a slab with certain constraints for the provision of its components.
 * The SlabElementedCase handles all cases of slabs, that are decomposed into parts:
 * - having components being assigned to the SlabElementedCase using the RelAggregates relationship accessible by the inverse relationship
 * IsDecomposedBy.
 * - applying the constraint that the parts within the decomposition shall be of type ElementAssembly, Beam, Member, Plate, BuildingElementPart or
 * BuildingElementProxy.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcslabelementedcase.htm" target="_blank">Documentation from IFC4:
 * IfcSlabElementedCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT SlabElementedCase : public Slab
{
    PROXY_HEADER(SlabElementedCase, App::SlabElementedCase, IFCSLABELEMENTEDCASE)

public:
    virtual ~SlabElementedCase(void);

protected:
    SlabElementedCase() {}
};

}  // namespace OpenLxApp