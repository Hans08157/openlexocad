#pragma once
#include <OpenLxApp/Door.h>

#include <memory>

FORWARD_DECL(App, DoorStandardCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The standard door, DoorStandardCase, defines a door with certain constraints for the provision of operation types,
 * opening directions, frame and lining parameters, and with certain constraints for the geometric representation.
 * The DoorStandardCase handles all cases of doors, that:
 * - are inserted into an opening, represented by OpeningElement, using the RelFillsElement relationship;
 * - have a local placement relative to this opening, and with the y-axis of the placement pointing into the opening direction;
 * - have a profile geometry, represented by ShapeRepresentation.RepresentationIdentifier="Profile" as a closed curve to which the door parameters
 * apply;
 * - have a reference to an DoorType to define the opening direction and the operation type (swinging, sliding, folding, etc.) of the door.
 *   The attribute OperationType shall be provided and not being UNDEFINED, and the attribute ParameterTakesPrecedence shall be "TRUE";
 * - have an DoorLiningProperties and DoorPanelProperties instances included in the set of HasPropertySets at DoorType.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcdoorstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcDoorStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT DoorStandardCase : public Door
{
    PROXY_HEADER(DoorStandardCase, App::DoorStandardCase, IFCDOORSTANDARDCASE)

public:
    virtual ~DoorStandardCase(void);


protected:
    DoorStandardCase() {}
};

}  // namespace OpenLxApp