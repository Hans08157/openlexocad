#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Ramp)

namespace OpenLxApp
{
/**
 * @brief A ramp is a vertical passageway which provides a human circulation link between one
 * floor level and another floor level at a different elevation.
 * It may include a landing as an intermediate floor slab. A ramp normally does not include steps.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcramp.htm" target="_blank">Documentation from IFC4: IfcRamp</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Ramp : public Element
{
    PROXY_HEADER(Ramp, App::Ramp, IFCRAMP)

public:
    enum class RampTypeEnum
    {
        STRAIGHT_RUN_RAMP,
        TWO_STRAIGHT_RUN_RAMP,
        QUARTER_TURN_RAMP,
        TWO_QUARTER_TURN_RAMP,
        HALF_TURN_RAMP,
        SPIRAL_RAMP,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(RampTypeEnum aType);
    RampTypeEnum getPredefinedType() const;

    virtual ~Ramp(void);


protected:
    Ramp() {}
};

}  // namespace OpenLxApp