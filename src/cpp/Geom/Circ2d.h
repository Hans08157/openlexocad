///////////////////////////////////////////////////////////////////////
//
// Copyright(C) 2013-2016  OpenCascade [www.opencascade.org]
//
// This library is free software; you can redistribute it and / or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street,
// Fifth Floor, Boston, MA  02110 - 1301  USA
//
///////////////////////////////////////////////////////////////////////

#pragma once 

#include <Geom/Ax22d.h>
#include <Geom/Ax2d.h>

namespace Geom
{
class Pnt2d;
class Trsf2d;
class Vec2d;

//! Describes a circle in the plane (2D space). <br>
//! A circle is defined by its radius and positioned in the <br>
//! plane with a coordinate system (a Ax22d object) as follows: <br>
//! - the origin of the coordinate system is the center of the circle, and <br>
//! - the orientation (direct or indirect) of the coordinate <br>
//! system gives an implicit orientation to the circle (and <br>
//! defines its trigonometric sense). <br>
//! This positioning coordinate system is the "local <br>
//! coordinate system" of the circle. <br>
//! Note: when a Circ2d circle is converted into a <br>
//! Geom2d_Circle circle, some implicit properties of the <br>
//! circle are used explicitly: <br>
//! - the implicit orientation corresponds to the direction in <br>
//! which parameter values increase, <br>
//! - the starting point for parameterization is that of the "X <br>
//! Axis" of the local coordinate system (i.e. the "X Axis" of the circle). <br>
//! See Also <br>
//! GccAna and Geom2dGcc packages which provide <br>
//! functions for constructing circles defined by geometric constraints <br>
//! gce_MakeCirc2d which provides functions for more <br>
//! complex circle constructions <br>
//! Geom2d_Circle which provides additional functions for <br>
//! constructing circles and works, with the parametric <br>
//! equations of circles in particular Ax22d <br>
class LX_GEOM_EXPORT Circ2d
{
public:
    //! creates an indefinite circle. <br>
    Circ2d();

    //! The location point of XAxis is the center of the circle. <br>
    //! Warnings : <br>
    //! It is not forbidden to create a circle with Radius = 0.0 Raises ConstructionError if Radius < 0.0. <br>//! Raised if Radius < 0.0. <br>
    Circ2d(const Ax2d& XAxis, const double Radius, const bool Sense = true);

    //! Axis defines the Xaxis and Yaxis of the circle which defines <br>
    //! the origin and the sense of parametrization. <br>
    //! The location point of Axis is the center of the circle. <br>
    //! Warnings : <br>
    //! It is not forbidden to create a circle with Radius = 0.0 Raises ConstructionError if Radius < 0.0. <br>//! Raised if Radius < 0.0. <br>
    Circ2d(const Ax22d& Axis, const double Radius);
    //! Changes the location point (center) of the circle. <br>
    void SetLocation(const Pnt2d& P);
    //! Changes the X axis of the circle. <br>
    void SetXAxis(const Ax2d& A);
    //! Changes the X axis of the circle. <br>
    void SetAxis(const Ax22d& A);
    //! Changes the Y axis of the circle. <br>
    void SetYAxis(const Ax2d& A);
    //! Modifies the radius of this circle. <br>
    //! This class does not prevent the creation of a circle where <br>
    //! Radius is null. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if Radius is negative. <br>
    void SetRadius(const double Radius);
    //! Computes the area of the circle. <br>
    double Area() const;

    //! Returns the normalized coefficients from the implicit equation <br>
    //! of the circle : <br>
    //! A * (X**2) + B * (Y**2) + 2*C*(X*Y) + 2*D*X + 2*E*Y + F = 0.0 <br>
    void Coefficients(double& A, double& B, double& C, double& D, double& E, double& F) const;
    //! Does <me> contain P ? <br>
    //! Returns True if the distance between P and any point on <br>
    //! the circumference of the circle is lower of equal to <br>
    //! <LinearTolerance>. <br>
    bool Contains(const Pnt2d& P, const double LinearTolerance) const;

    //! Computes the minimum of distance between the point P and any <br>
    //! point on the circumference of the circle. <br>
    double Distance(const Pnt2d& P) const;

    //! Computes the square distance between <me> and the point P. <br>
    double SquareDistance(const Pnt2d& P) const;
    //! computes the circumference of the circle. <br>
    double Length() const;
    //! Returns the location point (center) of the circle. <br>
    const Pnt2d& Location() const;
    //! Returns the radius value of the circle. <br>
    double Radius() const;
    //! returns the position of the circle. <br>
    const Ax22d& Axis() const;
    //! returns the position of the circle. Idem Axis(me). <br>
    const Ax22d& Position() const;
    //! returns the X axis of the circle. <br>
    Ax2d XAxis() const;
    //! Returns the Y axis of the circle. <br>//! Reverses the direction of the circle. <br>
    Ax2d YAxis() const;
    //! Reverses the orientation of the local coordinate system <br>
    //! of this circle (the "Y Direction" is reversed) and therefore <br>
    //! changes the implicit orientation of this circle. <br>
    //! Reverse assigns the result to this circle, <br>
    void Reverse();
    //! Reverses the orientation of the local coordinate system <br>
    //! of this circle (the "Y Direction" is reversed) and therefore <br>
    //! changes the implicit orientation of this circle. <br>
    //! Reversed creates a new circle. <br>
    Circ2d Reversed() const;
    //! Returns true if the local coordinate system is direct <br>
    //! and false in the other case. <br>
    bool IsDirect() const;

    void Mirror(const Pnt2d& P);

    //! Performs the symmetrical transformation of a circle with respect <br>
    //! to the point P which is the center of the symmetry <br>
    Circ2d Mirrored(const Pnt2d& P) const;

    void Mirror(const Ax2d& A);

    //! Performs the symmetrical transformation of a circle with respect <br>
    //! to an axis placement which is the axis of the symmetry. <br>
    Circ2d Mirrored(const Ax2d& A) const;

    void Rotate(const Pnt2d& P, const double Ang);

    //! Rotates a circle. P is the center of the rotation. <br>
    //! Ang is the angular value of the rotation in radians. <br>
    Circ2d Rotated(const Pnt2d& P, const double Ang) const;

    void Scale(const Pnt2d& P, const double S);

    //! Scales a circle. S is the scaling value. <br>
    //! Warnings : <br>
    //! If S is negative the radius stay positive but <br>
    //! the "XAxis" and the "YAxis" are reversed as for <br>
    //! an ellipse. <br>
    Circ2d Scaled(const Pnt2d& P, const double S) const;

    void Transform(const Trsf2d& T);

    //! Transforms a circle with the transformation T from class Trsf2d. <br>
    Circ2d Transformed(const Trsf2d& T) const;

    void Translate(const Vec2d& V);

    //! Translates a circle in the direction of the vector V. <br>
    //! The magnitude of the translation is the vector's magnitude. <br>
    Circ2d Translated(const Vec2d& V) const;

    void Translate(const Pnt2d& P1, const Pnt2d& P2);

    //! Translates a circle from the point P1 to the point P2. <br>
    Circ2d Translated(const Pnt2d& P1, const Pnt2d& P2) const;
    const Ax22d& _CSFDB_GetCirc2dpos() const { return pos; }
    double _CSFDB_GetCirc2dradius() const { return radius; }
    void _CSFDB_SetCirc2dradius(const double p) { radius = p; }



protected:
private:
    Ax22d pos;
    double radius;
};

}  // namespace Geom