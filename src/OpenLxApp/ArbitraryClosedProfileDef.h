#pragma once

#include <OpenLxApp/Curve.h>
#include <OpenLxApp/ProfileDef.h>

FORWARD_DECL(Part, ArbitraryClosedProfileDef)

namespace OpenLxApp
{
/*!
 * @brief The closed profile ArbitraryClosedProfileDef defines an arbitrary two-dimensional
 * profile for the use within the swept surface geometry, the swept area solid or a sectioned spine.
 * It is given by an outer boundary from which the surface or solid can be constructed.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcarbitraryclosedprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcArbitraryClosedProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT ArbitraryClosedProfileDef : public ProfileDef
{
    PROXY_HEADER(ArbitraryClosedProfileDef, Part::ArbitraryClosedProfileDef, IFCARBITRARYCLOSEDPROFILEDEF)

public:
    void setOuterCurve(std::shared_ptr<Curve> outerBound);
    std::shared_ptr<Curve> getOuterCurve() const;

    virtual ~ArbitraryClosedProfileDef(void);

protected:
    ArbitraryClosedProfileDef(void) {}
};
}  // namespace OpenLxApp