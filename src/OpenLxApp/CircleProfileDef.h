#pragma once

#include <OpenLxApp/ParameterizedProfileDef.h>


namespace Part {
class CircleProfileDef;
}

namespace OpenLxApp
{
/*!
 * @brief CircleProfileDef defines a circle as the profile definition used by the
 * swept surface geometry or by the swept area solid. It is given by its Radius attribute
 * and placed within the 2D position coordinate system, established by the Position attribute.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccirclehollowprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcCircleProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT CircleProfileDef : public ParameterizedProfileDef
{
    PROXY_HEADER(CircleProfileDef, Part::CircleProfileDef, IFCCIRCLEPROFILEDEF)

    DECL_PROPERTY(CircleProfileDef, Radius, double)

public:
    virtual ~CircleProfileDef(void);

protected:
    CircleProfileDef(void) {}
};
}  // namespace OpenLxApp