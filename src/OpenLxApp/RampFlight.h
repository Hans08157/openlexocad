#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, RampFlight)

namespace OpenLxApp
{
/**
 * @brief A ramp comprises a single inclined segment, or several inclined segments that are connected by a horizontal segment, referred to as a
 * landing. A ramp flight is the single inclined segment and part of the ramp construction. In case of single flight ramps, the ramp flight and the
 * ramp are identical.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrampflight.htm" target="_blank">Documentation from IFC4:
 * IfcRampFlight</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT RampFlight : public Element
{
    PROXY_HEADER(RampFlight, App::RampFlight, IFCRAMPFLIGHT)

public:
    enum class RampFlightTypeEnum
    {
        STRAIGHT,
        SPIRAL,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(RampFlightTypeEnum aType);
    RampFlightTypeEnum getPredefinedType() const;

    virtual ~RampFlight(void);


protected:
    RampFlight() {}
};

}  // namespace OpenLxApp