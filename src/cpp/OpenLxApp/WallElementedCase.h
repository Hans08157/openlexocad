#pragma once
#include <OpenLxApp/Wall.h>

#include <memory>

FORWARD_DECL(App, WallElementedCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The WallElementedCase defines a wall with certain constraints for the provision of its components.
 * The WallElementedCase handles all cases of walls, that are decomposed into parts:
 * - having components being assigned to the WallElementedCase using the RelAggregates relationship accessible by the inverse relationship
 * IsDecomposedBy.
 *
 * Parts within the decomposition are usually be of type:
 *  - BuildingElementPart for wall layer, insulation layers and similar
 *  - Member for studs, posts and similar elements,
 *  - ElementAssembly for other aggregates, or
 *  - BuildingElementProxy.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcwallelementedcase.htm" target="_blank">Documentation from IFC4:
 * IfcWallElementedCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT WallElementedCase : public Wall
{
    PROXY_HEADER(WallElementedCase, App::WallElementedCase, IFCWALLELEMENTEDCASE)

public:
    virtual ~WallElementedCase(void);

protected:
    WallElementedCase() {}
};

}  // namespace OpenLxApp