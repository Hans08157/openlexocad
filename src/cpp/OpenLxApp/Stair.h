#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Stair)

namespace OpenLxApp
{
/**
 * @brief A stair is a vertical passageway allowing occupants to walk (step) from
 * one floor level to another floor level at a different elevation.
 * It may include a landing as an intermediate floor slab.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcstair.htm" target="_blank">Documentation from IFC4: IfcStair</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Stair : public Element
{
    PROXY_HEADER(Stair, App::Stair, IFCSTAIR)

public:
    enum class StairTypeEnum
    {
        STRAIGHT_RUN_STAIR,
        TWO_STRAIGHT_RUN_STAIR,
        QUARTER_WINDING_STAIR,
        QUARTER_TURN_STAIR,
        HALF_WINDING_STAIR,
        HALF_TURN_STAIR,
        TWO_QUARTER_WINDING_STAIR,
        TWO_QUARTER_TURN_STAIR,
        THREE_QUARTER_WINDING_STAIR,
        THREE_QUARTER_TURN_STAIR,
        SPIRAL_STAIR,
        DOUBLE_RETURN_STAIR,
        CURVED_RUN_STAIR,
        TWO_CURVED_RUN_STAIR,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(StairTypeEnum aType);
    StairTypeEnum getPredefinedType() const;

    virtual ~Stair(void);


protected:
    Stair() {}
};

}  // namespace OpenLxApp