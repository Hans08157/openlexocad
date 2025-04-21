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

#include <Geom/Precision.h>
#include <Geom/XY.h>         // for XY

namespace Geom { class Ax2d; }
namespace Geom { class Trsf2d; }
namespace Geom { class Vec2d; }

namespace Geom
{
//! Describes a unit vector in the plane (2D space). This unit <br>
//! vector is also called "Direction". <br>
//! See Also <br>
//! gce_MakeDir2d which provides functions for more <br>
//! complex unit vector constructions <br>
//! Geom2d_Direction which provides additional functions <br>
//! for constructing unit vectors and works, in particular, with <br>
//! the parametric equations of unit vectors <br>
class LX_GEOM_EXPORT Dir2d
{
public:
    //! Creates an indefinite Direction. <br>
    Dir2d();
    //! Normalizes the vector V and creates a Direction. Raises ConstructionError if V.Magnitude() <= Resolution from gp. <br>
    Dir2d(const Vec2d& V);
    //! Creates a Direction from a doublet of coordinates. Raises ConstructionError if Coord.Modulus() <= Resolution from gp. <br>
    Dir2d(const XY& Coord);
    //! Creates a Direction with its 2 cartesian coordinates. Raises ConstructionError if Sqrt(Xv*Xv + Yv*Yv) <= Resolution from gp. <br>
    Dir2d(const double Xv, const double Yv);

    //! Computes the angular value in radians between <me> and <br>
    //! <Other>. Returns the angle in the range [-PI, PI]. <br>
    double angle(const Dir2d& Other) const;

    //! For this unit vector returns the coordinate of range Index : <br>
    //! Index = 1 => x is returned <br>
    //! Index = 2 => y is returned <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    double coord(const int Index) const;
    //! For this unit vector returns its two coordinates Xv and Yv. <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    void coord(double& Xv, double& Yv) const;
    //! Computes the cross product between two directions. <br>
    double crossed(const Dir2d& Right) const;
    //! Computes the scalar product <br>
    double dot(const Dir2d& Other) const;
    //! Returns True if the two vectors have the same direction <br>
    //! i.e. the angle between this unit vector and the <br>
    //! unit vector Other is less than or equal to AngularTolerance. <br>
    bool isEqual(const Dir2d& Other, const double AngularTolerance) const;

    //! Returns True if the angle between this unit vector and the <br>
    //! unit vector Other is equal to Pi/2 or -Pi/2 (normal) <br>
    //! i.e. abs(abs(<me>.Angle(Other)) - PI/2.) <= AngularTolerance <br>
    bool isNormal(const Dir2d& Other, const double AngularTolerance) const;

    //! Returns True if the angle between this unit vector and the <br>
    //! unit vector Other is equal to Pi or -Pi (opposite). <br>
    //! i.e. PI - abs(<me>.Angle(Other)) <= AngularTolerance <br>
    bool isOpposite(const Dir2d& Other, const double AngularTolerance) const;

    //! returns true if if the angle between this unit vector and unit <br>
    //! vector Other is equal to 0, Pi or -Pi. <br>
    //! i.e. abs(Angle(<me>, Other)) <= AngularTolerance or <br>
    //! PI - abs(Angle(<me>, Other)) <= AngularTolerance <br>
    bool isParallel(const Dir2d& Other, const double AngularTolerance) const;

    void mirror(const Dir2d& V);

    void mirror(const Ax2d& A);

    ////! Performs the symmetrical transformation of a direction <br>
    ////! with respect to an axis placement which is the axis <br>
    ////! of the symmetry. <br>
    Dir2d mirrored(const Ax2d& A) const;

    //! Performs the symmetrical transformation of a direction <br>
    //! with respect to the direction V which is the center of <br>
    //! the symmetry. <br>
    Dir2d mirrored(const Dir2d& V) const;

    Dir2d operator-() const { return reversed(); }

    double operator^(const Dir2d& Right) const { return crossed(Right); }
    double operator*(const Dir2d& Other) const { return dot(Other); }

    bool operator==(const Dir2d& other) const { return _coord.isEqual(other._coord, Geom::Precision::epsilon()); }

    void reverse();
    //! Reverses the orientation of a direction <br>
    Dir2d reversed() const;
    void rotate(const double Ang);

    //! Rotates a direction. Ang is the angular value of <br>
    //! the rotation in radians. <br>
    Dir2d rotated(const double Ang) const;

    //! For this unit vector, assigns: <br>
    //! the value Xi to: <br>
    //! - the X coordinate if Index is 1, or <br>
    //! - the Y coordinate if Index is 2, and then normalizes it. <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_OutOfRange if Index is not 1 or 2. <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! - Sqrt(Xv*Xv + Yv*Yv), or <br>
    //! - the modulus of the number pair formed by the new <br>
    //! value Xi and the other coordinate of this vector that <br>
    //! was not directly modified. <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    void setCoord(const int Index, const double Xi);

    //! For this unit vector, assigns: <br>
    //! - the values Xv and Yv to its two coordinates, <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_OutOfRange if Index is not 1 or 2. <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! - Sqrt(Xv*Xv + Yv*Yv), or <br>
    //! - the modulus of the number pair formed by the new <br>
    //! value Xi and the other coordinate of this vector that <br>
    //! was not directly modified. <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    void setCoord(const double Xv, const double Yv);

    //! Assigns the given value to the X coordinate of this unit vector, <br>
    //! and then normalizes it. <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! - the modulus of Coord, or <br>
    //! - the modulus of the number pair formed from the new <br>
    //! X or Y coordinate and the other coordinate of this <br>
    //! vector that was not directly modified. <br>
    void setX(const double X);

    //! Assigns: <br>
    //! - the two coordinates of Coord to this unit vector, <br>
    //! and then normalizes it. <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! - the modulus of Coord, or <br>
    //! - the modulus of the number pair formed from the new <br>
    //! x or y coordinate and the other coordinate of this <br>
    //! vector that was not directly modified. <br>
    void setXY(const XY& Coord);

    //! Assigns the given value to the Y coordinate of this unit vector, <br>
    //! and then normalizes it. <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! - the modulus of Coord, or <br>
    //! - the modulus of the number pair formed from the new <br>
    //! x or Y coordinate and the other coordinate of this <br>
    //! vector that was not directly modified. <br>
    void setY(const double Y);

    void transform(const Trsf2d& T);

    ////! Transforms a direction with the "Trsf" T. <br>
    ////! Warnings : <br>
    ////! If the scale factor of the "Trsf" T is negative then the <br>
    ////! direction <me> is reversed. <br>
    Dir2d transformed(const Trsf2d& T) const;

    //! For this unit vector, returns its x coordinate. <br>
    double x() const;
    //! For this unit vector, returns its two coordinates as a number pair. <br>//! Comparison between Directions <br>
    //! The precision value is an input data. <br>
    const XY& xy() const;

    //! For this unit vector, returns its y coordinate. <br>
    double y() const;

protected:
private:
    XY _coord;
};
}  // namespace Geom