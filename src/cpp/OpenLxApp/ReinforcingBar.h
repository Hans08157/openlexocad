#pragma once

#include <Base/Enums.h>
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, ReinforcingBar)

namespace OpenLxApp
{
/**
 * @brief A reinforcing bar is usually made of steel with manufactured deformations in the surface,
 * and used in concrete and masonry construction to provide additional strength.
 * A single instance of this class may represent one or many of actual rebars, for example a row of rebars.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcreinforcingbar.htm" target="_blank">Documentation from IFC4:
 * IfcReinforcingBar</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT ReinforcingBar : public Element
{
    PROXY_HEADER(ReinforcingBar, App::ReinforcingBar, IFCWALL)

public:
    enum class ReinforcingBarTypeEnum
    {
        ANCHORING,
        EDGE,
        LIGATURE,
        MAIN,
        PUNCHING,
        RING,
        SHEAR,
        STUD,
        USERDEFINED,
        NOTDEFINED
    };

    enum class ReinforcingBarSurfaceEnum
    {
        PLAIN,
        TEXTURED
    };

    void setPredefinedType(ReinforcingBarTypeEnum aType);
    ReinforcingBarTypeEnum getPredefinedType() const;
    void setBarSurface(ReinforcingBarSurfaceEnum aBarSurface);
    ReinforcingBarSurfaceEnum getBarSurface() const;

    virtual ~ReinforcingBar(void);

protected:
    ReinforcingBar() {}
};

}  // namespace OpenLxApp