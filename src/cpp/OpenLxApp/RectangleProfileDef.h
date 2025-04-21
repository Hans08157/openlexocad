#pragma once

#include <OpenLxApp/ParameterizedProfileDef.h>



FORWARD_DECL(Part, RectangleProfileDef)

namespace OpenLxApp
{
/*!
 * @brief RectangleProfileDef defines a rectangle as the profile definition used by the
 * swept surface geometry or the swept area solid. It is given by its X extent and its Y extent,
 * and placed within the 2D position coordinate system, established by the Position attribute.
 * It is placed centric within the position coordinate system.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrectangleprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcRectangleProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT RectangleProfileDef : public ParameterizedProfileDef
{
    PROXY_HEADER(RectangleProfileDef, Part::RectangleProfileDef, IFCRECTANGLEPROFILEDEF)

    DECL_PROPERTY(RectangleProfileDef, XDim, double)
    DECL_PROPERTY(RectangleProfileDef, YDim, double)

public:
    virtual ~RectangleProfileDef(void);

protected:
    RectangleProfileDef(void) {}
};
}  // namespace OpenLxApp