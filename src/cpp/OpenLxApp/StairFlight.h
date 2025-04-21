#pragma once

#include <OpenLxApp/Element.h>
#include <memory>

FORWARD_DECL(App, StairFlight)

namespace OpenLxApp
{
/**
 * @brief A stair flight is an assembly of building components in a single "run" of stair steps (not interrupted by a landing).
 * The stair steps and any stringers are included in the stair flight. A winder is also regarded a part of a stair flight.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcstairflight.htm" target="_blank">Documentation from IFC4:
 * IfcStairFlight</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT StairFlight : public Element
{
    PROXY_HEADER(StairFlight, App::StairFlight, IFCSTAIRFLIGHT)

public:
    enum class StairFlightTypeEnum
    {
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(StairFlightTypeEnum aType);
    StairFlightTypeEnum getPredefinedType() const;


    virtual ~StairFlight(void);


protected:
    StairFlight() {}
};

}  // namespace OpenLxApp