#pragma once

#include <OpenLxApp/Element.h>

FORWARD_DECL(App, Railing)

namespace OpenLxApp
{
/**
 * @brief The railing is a frame assembly adjacent to human circulation spaces and at some space boundaries
 * where it is used in lieu of walls or to compliment walls. Designed to aid humans, either as an optional physical support, or to prevent injury by
 * falling.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcrailing.htm" target="_blank">Documentation from IFC4: IfcRailing</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Railing : public Element
{
    PROXY_HEADER(Railing, App::Railing, IFCRAILING)

public:
    enum class RailingTypeEnum
    {
        HANDRAIL,
        GUARDRAIL,
        BALUSTRADE,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(RailingTypeEnum aType) const;
    RailingTypeEnum getPredefinedType() const;

    virtual ~Railing() = default;

protected:
    Railing() = default;
};

}  // namespace OpenLxApp