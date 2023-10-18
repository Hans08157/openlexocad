#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Door)

namespace OpenLxApp
{
/**
 * @brief The door is a building element that is predominately used to provide controlled access for people and goods.
 * It includes constructions with hinged, pivoted, sliding, and additionally revolving and folding operations.
 * A door consists of a lining and one or several panels.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcdoor.htm" target="_blank">Documentation from IFC4: IfcDoor</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Door : public Element
{
    PROXY_HEADER(Door, App::Door, IFCDOOR)

public:
    enum class DoorTypeEnum
    {
        DOOR,
        GATE,
        TRAPDOOR,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(DoorTypeEnum aType);
    DoorTypeEnum getPredefinedType() const;

    virtual ~Door(void);

protected:
    Door() {}
};

}  // namespace OpenLxApp