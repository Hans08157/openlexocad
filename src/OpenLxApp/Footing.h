#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Footing)

namespace OpenLxApp
{
/**
 * @brief A footing is a part of the foundation of a structure that spreads and transmits the load to the soil.
 * A footing is also characterized as shallow foundation, where the loads are transfered to the ground near the surface.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcfooting.htm" target="_blank">Documentation from IFC4: IfcFooting</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Footing : public Element
{
    PROXY_HEADER(Footing, App::Footing, IFCFOOTING)

public:
    enum class FootingTypeEnum
    {
        CAISSON_FOUNDATION,
        FOOTING_BEAM,
        PAD_FOOTING,
        PILE_CAP,
        STRIP_FOOTING,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(FootingTypeEnum aType);
    FootingTypeEnum getPredefinedType() const;

    virtual ~Footing(void);


protected:
    Footing() {}
};

}  // namespace OpenLxApp