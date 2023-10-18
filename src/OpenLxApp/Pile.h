#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Pile)

namespace OpenLxApp
{
/**
 * @brief  pile is a slender timber, concrete, or steel structural element, driven, jetted,
 * or otherwise embedded on end in the ground for the purpose of supporting a load.
 * A pile is also characterized as deep foundation, where the loads are transfered to deeper subsurface layers.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcpile.htm" target="_blank">Documentation from IFC4: IfcPile</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Pile : public Element
{
    PROXY_HEADER(Pile, App::Pile, IFCPILE)

public:
    enum class PileTypeEnum
    {
        BORED,
        DRIVEN,
        JETGROUTING,
        COHESION,
        FRICTION,
        SUPPORT,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(PileTypeEnum aType);
    PileTypeEnum getPredefinedType() const;

    virtual ~Pile(void);


protected:
    Pile() {}
};

}  // namespace OpenLxApp