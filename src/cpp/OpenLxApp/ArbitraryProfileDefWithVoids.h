#pragma once

#include <OpenLxApp/ArbitraryClosedProfileDef.h>
#include <OpenLxApp/Curve.h>


FORWARD_DECL(Part, ArbitraryProfileDefWithVoids)

namespace OpenLxApp
{
/*!
 * @brief The IfcArbitraryProfileDefWithVoids defines an arbitrary closed two-dimensional profile with holes.
 * It is given by an outer boundary and inner boundaries. A common usage of IfcArbitraryProfileDefWithVoids
 * is as the cross section for the creation of swept surfaces or swept solids.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcarbitraryprofiledefwithvoids.htm" target="_blank">Documentation from
 * IFC4: IfcArbitraryProfileDefWithVoids</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT ArbitraryProfileDefWithVoids : public ArbitraryClosedProfileDef
{
    PROXY_HEADER(ArbitraryProfileDefWithVoids, Part::ArbitraryProfileDefWithVoids, IFCARBITRARYPROFILEDEFWITHVOIDS)


public:
    void setInnerCurves(const std::vector<std::shared_ptr<Curve>>& innerCurves);
    std::vector<std::shared_ptr<Curve>> getInnerCurves() const;

    virtual ~ArbitraryProfileDefWithVoids(void);

protected:
    ArbitraryProfileDefWithVoids(void) {}
};
}  // namespace OpenLxApp