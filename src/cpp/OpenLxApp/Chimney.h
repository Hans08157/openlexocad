#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Chimney)

namespace OpenLxApp
{
/**
 * @brief Chimneys are typically vertical, or as near as vertical, parts of the construction of a
 * building and part of the building fabric. Often constructed by pre-cast or insitu concrete, today seldom by bricks.
 *
 * @see <a href="https://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcchimney.htm" target="_blank">Documentation from IFC4:
 * IfcChimney</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Chimney : public Element
{
    PROXY_HEADER(Chimney, App::Chimney, IFCCHIMNEY)

public:
    enum class ChimneyTypeEnum
    {
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(ChimneyTypeEnum aType);
    ChimneyTypeEnum getPredefinedType() const;

    virtual ~Chimney(void);

protected:
    Chimney() {}
};

}  // namespace OpenLxApp