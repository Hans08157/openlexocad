#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, CurtainWall)

namespace OpenLxApp
{
/**
 * @brief A curtain wall is an exterior wall of a building which is an assembly of components,
 * hung from the edge of the floor/roof structure rather than bearing on a floor.
 * Curtain wall is represented as a building element assembly and implemented as a subtype of BuildingElement that uses an RelAggregates relationship.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccurtainwall.htm" target="_blank">Documentation from IFC4:
 * IfcCurtainWall</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT CurtainWall : public Element
{
    PROXY_HEADER(CurtainWall, App::CurtainWall, IFCCURTAINWALL)

public:
    enum class CurtainWallTypeEnum
    {
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(CurtainWallTypeEnum aType);
    CurtainWallTypeEnum getPredefinedType() const;

    virtual ~CurtainWall(void);

protected:
    CurtainWall() {}
};

}  // namespace OpenLxApp