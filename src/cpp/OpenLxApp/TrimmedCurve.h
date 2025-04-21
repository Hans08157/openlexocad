#pragma once

#include <OpenLxApp/BoundedCurve.h>
#include <OpenLxApp/Conic.h>
#include <OpenLxApp/Line.h>



FORWARD_DECL(Part, TrimmedCurve)

namespace OpenLxApp
{
/*!
 * @brief A trimmed curve is a bounded curve which is created by taking a selected portion,
 * between two identified points, of the associated basis curve. The basis curve itself is
 * unaltered and more than one trimmed curve may reference the same basis curve.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifctrimmedcurve.htm" target="_blank">Documentation from IFC4:
 * IfcTrimmedCurve</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT TrimmedCurve : public BoundedCurve
{
    PROXY_HEADER(TrimmedCurve, Part::TrimmedCurve, IFCTRIMMEDCURVE)

    DECL_PROPERTY(TrimmedCurve, Trim1, double)
    DECL_PROPERTY(TrimmedCurve, Trim2, double)
    DECL_PROPERTY(TrimmedCurve, Sense, bool)

public:
    ~TrimmedCurve(void);

    void setBasisCurve(std::shared_ptr<Conic> aConic);
    void setBasisCurve(std::shared_ptr<Line> aLine);
    std::shared_ptr<Curve> getBasisCurve() const;

private:
    TrimmedCurve(void) {}
};
}  // namespace OpenLxApp
