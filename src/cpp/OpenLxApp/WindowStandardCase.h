#pragma once
#include <OpenLxApp/Window.h>

#include <memory>

FORWARD_DECL(App, WindowStandardCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The standard window, WindowStandardCase, defines a window with certain constraints for the provision of operation types,
 * opening directions, frame and lining parameters, construction types and with certain constraints for the geometric representation.
 * The WindowStandardCase handles all cases of windows, that:
 * - are inserted into an opening, represented by OpeningElement, using the RelFillsElement relationship
 * - have a local placement relative to this opening, and with the y-axis of the placement pointing into the opening direction
 * - have a profile geometry, represented by ShapeRepresentation.RepresentationIdentifier="Profile" as a closed curve to which the window parameter
 * apply. The profile represents a rectangle within the xz plane of the local placement
 * - have a reference to an WindowType to define the opening direction and the operation type (swinging, sliding, folding, etc.) of the window. The
 * attribute OperationType shall be provided and not being UNDEFINED, and the attribute ParameterTakesPrecedence shall be "TRUE".
 * - have a single WindowLiningProperties and a set of WindowPanelProperties instances included in the set of HasPropertySets at WindowType
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcwindowstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcWindowStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT WindowStandardCase : public Window
{
    PROXY_HEADER(WindowStandardCase, App::WindowStandardCase, IFCWINDOWSTANDARDCASE)

public:
    virtual ~WindowStandardCase(void);

protected:
    WindowStandardCase() {}
};

}  // namespace OpenLxApp