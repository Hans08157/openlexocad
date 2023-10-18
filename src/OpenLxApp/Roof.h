#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Roof)

namespace OpenLxApp
{
/**
 * @brief A roof is the covering of the top part of a building, it protects the building against the effects of weather.
 * The Roof is a description of the total roof. It acts as a container entity, that aggregates all components of the roof, it represents.
 * The aggregation is handled via 'Product.addRelatedProduct()', relating an Roof with the related roof elements,
 * like slabs (represented by OpenLxApp.Slab), rafters and purlins (represented by OpenLxApp.Beam), or other included roofs, such as dormers
 * (represented by OpenLxApp.Roof).
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcroof.htm" target="_blank">Documentation from IFC4: IfcRoof</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Roof : public Element
{
    PROXY_HEADER(Roof, App::Roof, IFCROOF)

public:
    enum class RoofTypeEnum
    {
        FLAT_ROOF,
        SHED_ROOF,
        GABLE_ROOF,
        HIP_ROOF,
        HIPPED_GABLE_ROOF,
        GAMBREL_ROOF,
        MANSARD_ROOF,
        BARREL_ROOF,
        RAINBOW_ROOF,
        BUTTERFLY_ROOF,
        PAVILION_ROOF,
        DOME_ROOF,
        FREEFORM,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(RoofTypeEnum aType);
    RoofTypeEnum getPredefinedType() const;

    virtual ~Roof(void);


protected:
    Roof() {}
};

}  // namespace OpenLxApp