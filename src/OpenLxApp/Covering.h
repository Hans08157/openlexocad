#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Covering)

namespace OpenLxApp
{
/**
 * @brief A covering is an element which covers some part of another element and is fully dependent on that other element.
 * The Covering defines the occurrence of a covering type, that (if given) is expressed by the CoveringType.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccovering.htm" target="_blank">Documentation from IFC4: IfcCovering</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Covering : public Element
{
    PROXY_HEADER(Covering, App::Covering, IFCCOVERING)

public:
    enum class CoveringTypeEnum
    {
        CEILING,
        FLOORING,
        CLADDING,
        ROOFING,
        MOLDING,
        SKIRTINGBOARD,
        INSULATION,
        MEMBRANE,
        SLEEVING,
        WRAPPING,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(CoveringTypeEnum aType);
    CoveringTypeEnum getPredefinedType() const;

    virtual ~Covering(void);


protected:
    Covering() {}
};

}  // namespace OpenLxApp