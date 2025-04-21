#pragma once 

namespace Geom
{
class XYZ;
class Vec;

}  // namespace Geom



namespace Geom
{
//! Describes a three column, three row matrix. This sort of <br>
//! object is used in various vectorial or matrix computations. <br>
class LX_GEOM_EXPORT Rotation
{
public:
    Rotation(void);
    Rotation(const Geom::Vec& axis, const double radians);
    Rotation(double m[4][4]);
    void getValue(Geom::Vec& axis, double& radians) const;
    Rotation& operator*=(double q);

    Rotation& setValue(double m[4][4]);
    Rotation& setValue(const Geom::Vec& axis, const double radians);

    void multVec(const Geom::Vec& src, Geom::Vec& dst) const;

private:
    double quat[4];
};

}  // namespace Geom
