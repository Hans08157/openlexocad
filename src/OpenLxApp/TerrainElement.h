#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, GeographicElement)

namespace OpenLxApp
{
/**
 * @brief An GeographicElement is a generalization of all elements within a geographical landscape.
 * It includes occurrences of typical geographical elements, often referred to as features, such as trees or terrain.
 * Common type information behind several occurrences of IfcGeographicElement is provided by the IfcGeographicElementType.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcgeographicelement.htm" target="_blank">Documentation from IFC4:
 * IfcGeographicElement</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT TerrainElement : public Element
{
    PROXY_HEADER(TerrainElement, App::GeographicElement, IFCTERRAINELEMENT)

public:
    virtual ~TerrainElement(void);


protected:
    TerrainElement() {}
};

}  // namespace OpenLxApp