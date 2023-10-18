#pragma once

#include <OpenLxApp/Curve.h>
#include <OpenLxApp/Geometry.h>



FORWARD_DECL(Part, SweptDiskSolid)

namespace OpenLxApp
{
/*!
 * @brief A SweptDiskSolid represents the 3D shape by a sweeping
 * representation scheme allowing a two dimensional circularly bounded
 * plane to sweep along a three dimensional Directrix through space.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcsweptdisksolid.htm" target="_blank">Documentation from IFC4:
 * IfcSweptDiskSolid</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT SweptDiskSolid : public Geometry
{
    PROXY_HEADER(SweptDiskSolid, Part::SweptDiskSolid, IFCSWEPTDISKSOLID)

    DECL_PROPERTY(SweptDiskSolid, Radius, double)
public:
    ~SweptDiskSolid(void);

    void setDirectrix(std::shared_ptr<Curve> curve);
    std::shared_ptr<Curve> getDirectrix() const;


private:
    SweptDiskSolid(void) {}
};

}  // namespace OpenLxApp
