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
#include <Geom/Pnt2d.h>

namespace Geom
{
class Ax2d;
class Dir2d;
class Trsf2d;

//! Defines a non-persistent vector in 2D space. <br>
class LX_GEOM_EXPORT Vec2d
{
public:
    //! Creates an indefinite vector. <br>
    Vec2d();
    //! Creates a unitary vector from a direction V. <br>
    Vec2d(const Dir2d& V);
    //! Creates a vector with a doublet of coordinates. <br>
    Vec2d(const XY& Coord);
    //! Creates a point with its two cartesian coordinates. <br>
    Vec2d(const double Xv, const double Yv);

    //! Creates a vector from two points. The length of the vector <br>
    //! is the distance between P1 and P2 <br>
    Vec2d(const Pnt2d& P1, const Pnt2d& P2);
    void add(const Vec2d& Other);
    //! Adds two vectors <br>
    Vec2d added(const Vec2d& Other) const;
    //! Computes the angular value between <me> and <Other> <br>
    //! returns the angle value between -PI and PI in radian. <br>
    //! The orientation is from <me> to Other. The positive sense is the <br>
    //! trigonometric sense. <br>
    double angle(const Vec2d& Other) const;
    //! Returns the coordinate of range Index : <br>
    //! Index = 1 => X is returned <br>
    //! Index = 2 => Y is returned <br>//! Raised if Index != {1, 2}. <br>
    double coord(const int Index) const;
    //! For this vector, returns its two coordinates Xv and Yv <br>
    void coord(double& Xv, double& Yv) const;
    //! Computes the crossing product between two vectors <br>
    double crossed(const Vec2d& Right) const;
    //! Computes the magnitude of the cross product between <me> and <br>
    //! Right. Returns || <me> ^ Right || <br>
    double crossMagnitude(const Vec2d& Right) const;

    //! Computes the square magnitude of the cross product between <me> and <br>
    //! Right. Returns || <me> ^ Right ||**2 <br>
    double crossSquareMagnitude(const Vec2d& Right) const;

    void divide(const double Scalar);
    //! divides a vector by a scalar <br>
    Vec2d divided(const double Scalar) const;
    //! Computes the scalar product <br>
    double dot(const Vec2d& Other) const;
    //! Returns True if the two vectors have the same magnitude value <br>
    //! and the same direction. The precision values are LinearTolerance <br>
    //! for the magnitude and AngularTolerance for the direction. <br>
    bool isEqual(const Vec2d& Other, const double LinearTolerance, const double AngularTolerance) const;

    //! Returns True if abs(abs(<me>.angle(Other)) - PI/2.) <= AngularTolerance <br>
    bool isNormal(const Vec2d& Other, const double AngularTolerance) const;

    //! Returns True if PI - abs(<me>.angle(Other)) <= AngularTolerance <br>
    bool isOpposite(const Vec2d& Other, const double AngularTolerance) const;

    //! Returns true if abs(angle(<me>, Other)) <= AngularTolerance or <br>
    //! PI - abs(angle(<me>, Other)) <= AngularTolerance <br>
    //! Two vectors with opposite directions are considered as parallel. <br>
    bool isParallel(const Vec2d& Other, const double AngularTolerance) const;

    //! Computes the magnitude of this vector. <br>
    double magnitude() const;
    //! Computes the square magnitude of this vector. <br>
    double squareMagnitude() const;

    void operator+=(const Vec2d& Other) { add(Other); }
    Vec2d operator+(const Vec2d& Other) const { return added(Other); }
    void operator-=(const Vec2d& Right) { subtract(Right); }
    Vec2d operator-() const { return reversed(); }

    Vec2d operator-(const Vec2d& Right) const { return subtracted(Right); }

    void operator*=(const double Scalar) { multiply(Scalar); }
    double operator*(const Vec2d& Other) const { return dot(Other); }

    Vec2d operator*(const double Scalar) const { return multiplied(Scalar); }

    void operator/=(const double Scalar) { divide(Scalar); }
    Vec2d operator/(const double Scalar) const { return divided(Scalar); }
    double operator^(const Vec2d& Right) const { return crossed(Right); }

    void multiply(const double Scalar);
    //! Normalizes a vector <br>
    //! Raises an exception if the magnitude of the vector is <br>
    //! lower or equal to Resolution from package gp. <br>
    Vec2d multiplied(const double Scalar) const;
    void mirror(const Vec2d& V);

    void mirror(const Ax2d& A1);

    ////! Performs the symmetrical transformation of a vector <br>
    ////! with respect to an axis placement which is the axis <br>
    ////! of the symmetry. <br>
    Vec2d mirrored(const Ax2d& A1) const;

    //! Performs the symmetrical transformation of a vector <br>
    //! with respect to the vector V which is the center of <br>
    //! the symmetry. <br>
    //! Performs the symmetrical transformation of a vector <br>
    //! with respect to an axis placement which is the axis <br>
    //! of the symmetry. <br>
    Vec2d mirrored(const Vec2d& V) const;

    void normalize();
    //! Normalizes a vector <br>
    //! Raises an exception if the magnitude of the vector is <br>
    //! lower or equal to Resolution from package gp. <br>//! Reverses the direction of a vector <br>
    Vec2d normalized() const;

    void reverse();
    //! Reverses the direction of a vector <br>//! Subtracts two vectors <br>
    Vec2d reversed() const;
    void rotate(const double Ang);

    //! Rotates a vector. Ang is the angular value of the <br>
    //! rotation in radians. <br>
    Vec2d rotated(const double Ang) const;

    void scale(const double S);
    //! Scales a vector. S is the scaling value. <br>
    Vec2d scaled(const double S) const;

    //! Changes the coordinate of range Index <br>
    //! Index = 1 => X is modified <br>
    //! Index = 2 => Y is modified <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    void setCoord(const int Index, const double Xi);
    //! For this vector, assigns <br>
    //! the values Xv and Yv to its two coordinates <br>
    void setCoord(const double Xv, const double Yv);
    //! <me> is setted to the following linear form : <br>
    //! A1 * V1 + A2 * V2 + V3 <br>
    void setLinearForm(const double A1, const Vec2d& V1, const double A2, const Vec2d& V2, const Vec2d& V3);

    //! <me> is setted to the following linear form : A1 * V1 + A2 * V2 <br>
    void setLinearForm(const double A1, const Vec2d& V1, const double A2, const Vec2d& V2);

    //! <me> is setted to the following linear form : A1 * V1 + V2 <br>
    void setLinearForm(const double A1, const Vec2d& V1, const Vec2d& V2);

    //! <me> is setted to the following linear form : Left + Right <br>
    //! Performs the symmetrical transformation of a vector <br>
    //! with respect to the vector V which is the center of <br>
    //! the symmetry. <br>
    void setLinearForm(const Vec2d& Left, const Vec2d& Right);

    //! Assigns the given value to the X coordinate of this vector. <br>
    void setX(const double X);
    //! Assigns the two coordinates of Coord to this vector. <br>
    void setXY(const XY& Coord);

    //! Assigns the given value to the Y coordinate of this vector. <br>
    void setY(const double Y);
    void subtract(const Vec2d& Right);
    //! Subtracts two vectors <br>
    Vec2d subtracted(const Vec2d& Right) const;
    void transform(const Trsf2d& T);
    ////! Transforms a vector with a Trsf from gp. <br>
    Vec2d transformed(const Trsf2d& T) const;

    //! For this vector, returns its X coordinate. <br>
    double x() const;
    //! For this vector, returns its two coordinates as a number pair <br>
    const XY& xy() const;

    //! For this vector, returns its Y coordinate. <br>
    double y() const;

protected:
private:
    XY _coord;
};
}  // namespace Geom