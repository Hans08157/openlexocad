#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Slab)

namespace OpenLxApp
{
/**
 * @brief A slab is a component of the construction that normally encloses a space vertically.
 * The slab may provide the lower support (floor) or upper construction (roof slab) in any space in a building.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcslab.htm" target="_blank">Documentation from IFC4: IfcSlab</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Slab : public Element
{
    PROXY_HEADER(Slab, App::Slab, IFCSLAB)

public:
    enum class SlabTypeEnum
    {
        FLOOR,  // Display name Floor
        ROOF,   // Display name Roof
        LANDING,
        BASESLAB,
        USERDEFINED,  // Display name Slab
        NOTDEFINED
    };

    void setPredefinedType(SlabTypeEnum aType);
    SlabTypeEnum getPredefinedType() const;

    virtual ~Slab(void);


protected:
    Slab() {}
};

}  // namespace OpenLxApp