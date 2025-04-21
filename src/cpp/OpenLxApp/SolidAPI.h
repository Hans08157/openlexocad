#pragma once

#include <OpenLxApp/AdvancedBrep.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/ExtrudedAreaSolid.h>
#include <OpenLxApp/FacetedBrep.h>
#include <Topo/ShapeTool.h>

#include <memory>

/** @defgroup OPENLX_SOLID_API Solid API
 */

namespace OpenLxApp
{
LX_OPENLXAPP_EXPORT std::shared_ptr<ExtrudedAreaSolid> createExtrudedAreaSolid(
    std::shared_ptr<Document> aDoc,
    pConstShape aShape,
    Topo::ShapeTool::BuildingElementHintEnum aHint = Topo::ShapeTool::BuildingElementHintEnum::NO_HINT);
LX_OPENLXAPP_EXPORT std::shared_ptr<FacetedBrep> createFacetedBrep(std::shared_ptr<Document> aDoc, pConstShape aShape);
LX_OPENLXAPP_EXPORT std::shared_ptr<AdvancedBrep> createAdvancedBrep(std::shared_ptr<Document> aDoc, pConstShape aShape);


}  // namespace OpenLxApp