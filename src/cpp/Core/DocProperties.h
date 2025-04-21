#pragma once

#include <map>
#include <set>

namespace Core
{
class DocObject;

/**
 * This struct holds information about properties required to be displayed in PropertiesDialog.
 * Every DocObject is responsible to add info about itself if asked to do so (collectDocProperties()).
 */
struct LX_CORE_EXPORT DocProperties
{
    unsigned int elementsWithoutGeometry = 0;
    unsigned int multigeo = 0;
    unsigned int subElements = 0;
    unsigned int groups = 0;
    unsigned int spatialElements = 0;
    unsigned int auxiliaryElements = 0;

    unsigned int points = 0;
    unsigned int curves = 0;

    unsigned int surfaces = 0;
    unsigned int surfaces2d = 0;
    unsigned int surfaces3d = 0;

    unsigned int solids = 0;
    unsigned int facetedBrepSolids = 0;
    unsigned int extrusions = 0;
    unsigned int solidPlates = 0;
    unsigned int solidBars = 0;
    unsigned int wallStandards = 0;
    unsigned int walls = 0;
    unsigned int slabStandards = 0;

    unsigned int polygonMeshes = 0;
    unsigned int polygonMeshesSolids = 0;
    unsigned int polygonMeshesSurfaces = 0;
    unsigned int polygonMeshesLinear = 0;
    unsigned int polygonMeshesPlate = 0;
    unsigned int polygonMeshesLinearPlate = 0;

    unsigned int texts = 0;

    unsigned int ivBlocks = 0;
    unsigned int inventorImports = 0;
    std::set<Core::DocObject*> inventorImportIvObjects;
    unsigned int ifcBlocks = 0;
    std::set<Core::DocObject*> ifcBlockIvObjects;

    unsigned int dimensions = 0;

    std::map<Core::DocObject*, int> materialUsageCache;
    unsigned int materialsUsed = 0;
    unsigned int materialsNotUsed = 0;
    unsigned int materialsLcc = 0;

    unsigned int componentsUsed = 0;
    unsigned int componentsNotUsed = 0;
    unsigned int componentsLcc = 0;

    unsigned int propertySetsUsed = 0;
    unsigned int propertySetsNotUsed = 0;
    unsigned int propertySetsEmpty = 0;
    unsigned int propertySetsLcc = 0;

    unsigned int others = 0;
};

}  // namespace Core
