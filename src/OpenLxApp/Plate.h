#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Plate)

namespace OpenLxApp
{
/**
 * @brief An Plate is a planar and often flat part with constant thickness.
 * A plate may carry loads between or beyond points of support, or provide stiffening.
 * The location of the plate (being horizontal, vertical or sloped) is not relevant to its definition (in contrary to Wall and Slab (as floor slab)).
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcplate.htm" target="_blank">Documentation from IFC4: IfcPlate</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Plate : public Element
{
    PROXY_HEADER(Plate, App::Plate, IFCPLATE)

public:
    enum class PlateTypeEnum
    {
        CURTAIN_PANEL,
        SHEET,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(PlateTypeEnum aType);
    PlateTypeEnum getPredefinedType() const;

    virtual ~Plate(void);

protected:
    Plate() {}
};

}  // namespace OpenLxApp