#pragma once

#include <Geom/Pnt.h>
#include <Geom/Vec.h>
#include <OpenLxApp/Geometry.h>

namespace Part
{
class Curve;
}

namespace Topo
{
class Wire;
}

namespace OpenLxApp
{
/*!
 * @brief A curve can be envisioned as the path of a point moving in its coordinate space.
 * (Definition from ISO/CD 16739:2011)
 *
 ** @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccurve.htm" target="_blank">Documentation from IFC4: IfcCurve</a>
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Curve : public Geometry
{
    PROXY_HEADER_ABSTRACT(Curve, Part::Curve, IFCCURVE)

public:
    std::shared_ptr<Topo::Wire const> getWire() const;

    void translate(const Geom::Vec& v);
    void transform(const Geom::Trsf& t);
    void reverse();

    double firstParameter() const;
    double lastParameter() const;

    void d0(double u, Geom::Pnt& p) const;
    void d1(double u, Geom::Pnt& p, Geom::Vec& v1) const;
    void d2(double u, Geom::Pnt& p, Geom::Vec& v1, Geom::Vec& v2) const;
    Geom::Pnt value(double U) const;
    double transformedParameter(double U, const Geom::Trsf& t) const;

    virtual ~Curve(void);

protected:
    Curve(void) = default;
};
}  // namespace OpenLxApp