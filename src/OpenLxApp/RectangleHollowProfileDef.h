#pragma once

#include <OpenLxApp/RectangleProfileDef.h>

FORWARD_DECL(Part, RectangleHollowProfileDef)

namespace OpenLxApp
{
/*!
 * @brief RectangleHollowProfileDef defines a section profile that provides the defining parameters
 * of a rectangular (or square) hollow section to be used by the swept surface geometry or the swept area solid.
 * Its parameters and orientation relative to the position coordinate system are according to the illustration (see link below).
 * A square hollow section can be defined by equal values for h and b. The centre of the position coordinate system is
 * in the profiles centre of the bounding box (for symmetric profiles identical with the centre of gravity).
 * Normally, the longer sides are parallel to the y-axis, the shorter sides parallel to the x-axis.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrectanglehollowprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcRectangleHollowProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT RectangleHollowProfileDef : public RectangleProfileDef
{
    PROXY_HEADER(RectangleHollowProfileDef, Part::RectangleHollowProfileDef, IFCRECTANGLEHOLLOWPROFILEDEF)

    DECL_PROPERTY(RectangleHollowProfileDef, WallThickness, double)
    DECL_PROPERTY(RectangleHollowProfileDef, InnerFilletRadius, double)
    DECL_PROPERTY(RectangleHollowProfileDef, OuterFilletRadius, double)

public:
    virtual ~RectangleHollowProfileDef(void);

protected:
    RectangleHollowProfileDef(void) {}
};
}  // namespace OpenLxApp