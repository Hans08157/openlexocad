#pragma once
#include <Geom/Pnt.h> 

namespace Geom
{
//!  Defines a non-persistent Sphere in 3D space. <br>
class LX_GEOM_EXPORT Sphr
{
public:
    Sphr();
    Sphr(const Geom::Pnt& center, const double& radius);
    void setValue(const Geom::Pnt& center, const double& radius);
    void setCenter(const Geom::Pnt& center);
    void setRadius(const double& radius);
    const Geom::Pnt& getCenter(void) const;
    const double& getRadius(void) const;

    bool pointInside(const Geom::Pnt& p) const;

private:
    Geom::Pnt _center;
    double _radius;
};

}  // namespace Geom