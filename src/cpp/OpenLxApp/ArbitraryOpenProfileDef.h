#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/ProfileDef.h>

FORWARD_DECL(Part, ArbitraryOpenProfileDef)

namespace OpenLxApp
{
/*!
 * @brief The profile ArbitraryOpenProfileDef defines an arbitrary two-dimensional
 * profile for the use within the swept surface geometry, the swept area solid or a sectioned spine.
 * It is given by an outer boundary from which the surface or solid can be constructed.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcArbitraryOpenProfileDef.htm" target="_blank">Documentation from IFC4:
 * IfcArbitraryOpenProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT ArbitraryOpenProfileDef : public ProfileDef
{
    PROXY_HEADER(ArbitraryOpenProfileDef, Part::ArbitraryOpenProfileDef, IFCARBITRARYOPENPROFILEDEF)

public:
    void setCurve(std::shared_ptr<BoundedCurve> outerBound) const;
    std::shared_ptr<BoundedCurve> getCurve() const;

    virtual ~ArbitraryOpenProfileDef() = default;

protected:
    ArbitraryOpenProfileDef() = default;
};
}  // namespace OpenLxApp