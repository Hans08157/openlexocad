#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Window)

namespace OpenLxApp
{
/**
 * @brief The window is a building element that is predominately used to provide natural light and fresh air.
 * It includes vertical opening but also horizontal opening such as skylights or light domes.
 * It includes constructions with swinging, pivoting, sliding, or revolving panels and fixed panels.
 * A window consists of a lining and one or several panels.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcwindow.htm" target="_blank">Documentation from IFC4: IfcWindow</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Window : public Element
{
    PROXY_HEADER(Window, App::Window, IFCWINDOW)

public:
    enum class WindowTypeEnum
    {
        WINDOW,
        SKYLIGHT,
        LIGHTDOME,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(WindowTypeEnum aType);
    WindowTypeEnum getPredefinedType() const;

    virtual ~Window(void);

protected:
    Window() {}
};

}  // namespace OpenLxApp