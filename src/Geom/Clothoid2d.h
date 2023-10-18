#pragma once

#include <vector>
#include <Geom/Pnt2d.h>  // for Pnt2d

namespace Geom { class Ax2d; }

namespace Geom
{
/*
    "The clothoid is the standard transition curve used in railroad engineering/highway engineering for connecting a straight and a circular curve.
    A clothoid has a CONSTANT INCREASING curvature proportional to its curve length.
    Two input parameters are required : the radius R and the parameter A. Suggested values of A : R / 3 <= A <= R.
    All clothoids are geometrically similar : as with the radius R, the parameter A serves as a modification factor(enlargement / reduction).
    For practical applications, a clothoid is viewed in the *1st quadrant* of the coordinate system."
    The smaller the parameter A is, the faster the curvature increases.The length of the transition arc L grows with the parameter A.
    (Source "Fundamentals of Road Design" - ISBN 9781845643362)
*/
class LX_GEOM_EXPORT Clothoid2d
{
public:
    Clothoid2d() = default;
    Clothoid2d(const double& endRadius, const double& constant);
    Clothoid2d(const double& startRadius, const double &endRadius, const double& constant);
    Clothoid2d(const Clothoid2d& other);
    Clothoid2d(Clothoid2d&& other) noexcept;
    Clothoid2d& operator=(const Clothoid2d& other);
    Clothoid2d& operator=(Clothoid2d&& other) noexcept;
    ~Clothoid2d() = default;

    /// Clothoid parameter.
    double getConstant() const;
    void setConstant(const double& A);

    /// Radius at the end of the clothoid section.
    double getEndRadius() const;
    void setEndRadius(const double& R);

    /// Radius at the start of the clothoid section.
    double getStartRadius() const;
    void setStartRadius(const double& R);

    /// Compute tangent angle τ (radians) "τ=A²/(2×R²)".
    double computeTauFromRadius(const double& R) const;
    double computeTauEnd() const;
    double computeTauStart() const;

    /// Tangent retraction Δ at angle 𝛕.
    double computeDeltaR(const double& 𝛕, const double& R) const;

    /// Get distance L from origin for angle 𝛕.
    static double computeLength(const double& 𝛕, const double& R);
    double computeLengthEnd() const;
    double computeLengthStart() const;

    /// Get tangent angle τ (radians) at distance L.
    double computeTauFromLength(const double& L) const;

    /// Get XY-coordinates of point at distance L.
    Geom::XY computeCoordinates(const double& L) const;
    Geom::XY computeCoordinatesEnd() const;
    Geom::XY computeCoordinatesOrigin() const;
    Geom::XY computeCoordinatesStart() const;

    /// Get XY-coordinates of circle center at distance L.
    Geom::XY computeCenter(const double& L, const double& R) const;
    Geom::XY computeCenterEnd() const;
    Geom::XY computeCenterStart() const;

    /// Tangent length (used as debug value)
    double computeTk(const double& R) const;
    /// Tangent length (used as debug value)
    double computeTl(const double& R) const;

    std::vector<Geom::XY> approximate(const unsigned int& segments) const;

private:
    double _constant = 1.;   // Constant A
    double _endRadius = 1.;
    double _startRadius = 0.;
};
}  // namespace Geom
