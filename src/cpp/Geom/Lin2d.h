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

#include <Geom/Ax2d.h>

namespace Geom
{
class Dir2d;
class Pnt2d;
class Trsf2d;
class Vec2d;

//! Describes a line in 2D space. <br>
//! A line is positioned in the plane with an axis (a Ax2d <br>
//! object) which gives the line its origin and unit vector. A <br>
//! line and an axis are similar objects, thus, we can convert <br>
//! one into the other. <br>
//! A line provides direct access to the majority of the edit <br>
//! and query functions available on its positioning axis. In <br>
//! addition, however, a line has specific functions for <br>
//! computing distances and positions. <br>
//! See Also <br>
//! GccAna and Geom2dGcc packages which provide <br>
//! functions for constructing lines defined by geometric <br>
//! constraints <br>
//! gce_MakeLin2d which provides functions for more <br>
//! complex line constructions <br>
//! Geom2d_Line which provides additional functions for <br>
//! constructing lines and works, in particular, with the <br>
//! parametric equations of lines <br>
class LX_GEOM_EXPORT Lin2d
{
public:
    //! Creates an indefinite Line. <br>
    Lin2d();
    //! Creates a line located with A. <br>
    Lin2d(const Ax2d& A);

    //! <P> is the location point (origin) of the line and <br>
    //! <V> is the direction of the line. <br>
    Lin2d(const Pnt2d& P, const Dir2d& V);

    //! Creates the line from the equation A*X + B*Y + C = 0.0 Raises ConstructionError if Sqrt(A*A + B*B) <= Resolution from gp. <br>//! Raised if
    //! Sqrt(A*A + B*B) <= Resolution from gp. <br>
    Lin2d(const double A, const double B, const double C);

    //! Computes the angle between two lines in radians. <br>
    double angle(const Lin2d& Other) const;
    //! Returns the normalized coefficients of the line : <br>
    //! A * X + B * Y + C = 0. <br>
    void coefficients(double& A, double& B, double& C) const;
    //! Returns true if this line contains the point P, that is, if the <br>
    //! distance between point P and this line is less than or <br>
    //! equal to LinearTolerance. <br>
    bool contains(const Pnt2d& P, const double LinearTolerance) const;

    //! Computes the distance between <me> and the point <P>. <br>
    double distance(const Pnt2d& P) const;
    //! Computes the distance between two lines. <br>
    double distance(const Lin2d& Other) const;

    //! Computes the signed distance between <me> and the point <P>. <br>
    double signedDistance(const Pnt2d& P) const;

    //! Returns the direction of the line. <br>
    const Dir2d& direction() const;
    //! Returns the location point (origin) of the line. <br>
    const Pnt2d& location() const;

    void mirror(const Pnt2d& P);

    void mirror(const Ax2d& A);

    //! Performs the symmetrical transformation of a line <br>
    //! with respect to an axis placement which is the axis <br>
    //! of the symmetry. <br>
    Lin2d mirrored(const Ax2d& A) const;

    //! Performs the symmetrical transformation of a line <br>
    //! with respect to the point <P> which is the center <br>
    //! of the symmetry <br>
    Lin2d mirrored(const Pnt2d& P) const;

    //! Computes the line normal to the direction of <me>, <br>
    //! passing through the point <P>. <br>
    Lin2d normal(const Pnt2d& P) const;

    //! Returns the axis placement one axis whith the same <br>
    //! location and direction as <me>. <br>
    const Ax2d& position() const;
    void reverse();

    //! Reverses the positioning axis of this line. <br>
    //! Note: <br>
    //! - reverse assigns the result to this line, while <br>
    //! - reversed creates a new one. <br>
    Lin2d reversed() const;
    void rotate(const Pnt2d& P, const double Ang);

    //! Rotates a line. P is the center of the rotation. <br>
    //! Ang is the angular value of the rotation in radians. <br>
    Lin2d rotated(const Pnt2d& P, const double Ang) const;

    void scale(const Pnt2d& P, const double S);

    //! Scales a line. S is the scaling value. Only the <br>
    //! origin of the line is modified. <br>
    Lin2d scaled(const Pnt2d& P, const double S) const;

    //! Changes the direction of the line. <br>
    void setDirection(const Dir2d& V);
    //! Changes the origin of the line. <br>
    void setLocation(const Pnt2d& P);

    //! Complete redefinition of the line. <br>
    //! The "location" point of <A> is the origin of the line. <br>
    //! The "direction" of <A> is the direction of the line. <br>
    void setPosition(const Ax2d& A);

    //! Computes the square distance between <me> and the point <br>
    //! <P>. <br>
    double squareDistance(const Pnt2d& P) const;
    //! Computes the square distance between two lines. <br>
    double squareDistance(const Lin2d& Other) const;

    void transform(const Trsf2d& T);

    //! Transforms a line with the transformation T from class Trsf2d. <br>
    Lin2d transformed(const Trsf2d& T) const;

    void translate(const Vec2d& V);

    void translate(const Pnt2d& P1, const Pnt2d& P2);

    //! Translates a line in the direction of the vector V. <br>
    //! The magnitude of the translation is the vector's magnitude. <br>
    Lin2d translated(const Vec2d& V) const;

    //! Translates a line from the point P1 to the point P2. <br>
    Lin2d translated(const Pnt2d& P1, const Pnt2d& P2) const;
    const Ax2d& _CSFDB_GetLin2dpos() const { return _pos; }


protected:
private:
    Ax2d _pos;
};

}  // namespace Geom