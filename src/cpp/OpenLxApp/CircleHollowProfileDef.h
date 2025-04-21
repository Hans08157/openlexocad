#pragma once

#include <OpenLxApp/CircleProfileDef.h>


namespace Part {
class CircleHollowProfileDef;
}

namespace OpenLxApp
{
/*!
 * @brief CircleHollowProfileDef defines a section profile that provides the
 * defining parameters of a circular hollow section (tube) to be used by the swept area solid.
 * Its parameters and orientation relative to the position coordinate system are according to the
 * following illustration.The centre of the position coordinate system is in the profile's centre
 * of the bounding box (for symmetric profiles identical with the centre of gravity).
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccirclehollowprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcCircleHollowProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT CircleHollowProfileDef : public CircleProfileDef
{
    PROXY_HEADER(CircleHollowProfileDef, Part::CircleHollowProfileDef, IFCCIRCLEHOLLOWPROFILEDEF)

    DECL_PROPERTY(CircleHollowProfileDef, WallThickness, double)

public:
    virtual ~CircleHollowProfileDef(void);

protected:
    CircleHollowProfileDef(void) {}
};
}  // namespace OpenLxApp