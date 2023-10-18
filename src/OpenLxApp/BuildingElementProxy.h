#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, BuildingElementProxy)

namespace OpenLxApp
{
/**
 * @brief The BuildingElementProxy is a proxy definition that provides the same functionality as subtypes of BuildingElement,
 * but without having a predefined meaning of the special type of building element, it represents.
 * Proxies can also be used as spatial place holders or provisions, that are later replaced by special types of elements.
 * One use of the proxy object is a provision for voids, i.e. where a particular volume of space is requested by an
 * engineering function that might later be accepted or rejected. If accepted it is transformed into a void within a building element,
 * like a wall opening, or a slab opening. The provision for voids is exchanged as an BuildingElementProxy with the
 * PredefinedType = ProvisionForVoid. Such proxy shall have a swept solid geometry, where the profile of the swept solid
 * lies on/near the surface of the referred building element and the extrusion depths is equal to or
 * bigger then (in case of round or otherwise irregular element shape) the thickness of the building element. The appropriate property set should be
 * attached. In addition to the provision for voids, the building element proxy can also represent a provision for space, often the necessary space
 * allocation for mechanical equipment that will be determined in a later design phase. The provision for space is exchanged as an
 * IfcBuildingElementProxy with the PredefinedType = ProvisionForSpace.
 *
 * Other usages of BuildingElementProxy include:
 * - The BuildingElementProxy can be used to exchange special types of building elements for which the current specification does not yet provide a
 * semantic definition.
 * - The BuildingElementProxy can also be used to represent building elements for which the participating applications can not provide a semantic
 * definition.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcbuildingelementproxy.htm" target="_blank">Documentation from IFC4:
 * IfcBuildingElementProxy</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT BuildingElementProxy : public Element
{
    PROXY_HEADER(BuildingElementProxy, App::BuildingElementProxy, IFCBUILDINGELEMENTPROXY)

public:
    enum class BuildingElementProxyTypeEnum
    {
        COMPLEX,
        ELEMENT,
        PARTIAL,
        PROVISIONFORVOID,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(BuildingElementProxyTypeEnum aType);
    BuildingElementProxyTypeEnum getPredefinedType() const;

    virtual ~BuildingElementProxy(void);


protected:
    BuildingElementProxy() {}
};

}  // namespace OpenLxApp