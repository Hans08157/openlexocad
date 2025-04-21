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

#include <Geom/XY.h> 

namespace Geom
{
class Ax2d;
class Trsf2d;
class Vec2d;

//! Defines a non-persistent 2D cartesian point. <br>
class LX_GEOM_EXPORT Pnt2d
{
public:
    Pnt2d();
    //! Creates a point with a doublet of coordinates. <br>
    Pnt2d(const XY& Coord);

    //! Creates a point with its 2 cartesian's coordinates : Xp, Yp. <br>
    Pnt2d(const double Xp, const double Yp);

    //! Returns the coordinates of this point. <br>
    //! Note: This syntax allows direct modification of the returned value. <br>
    XY& changeCoord();
    //! For this point, returns its two coordinates as a number pair. <br>
    const XY& coord() const;

    //! Returns the coordinate of range Index : <br>
    //! Index = 1 => x is returned <br>
    //! Index = 2 => y is returned <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    double coord(const int Index) const;
    //! For this point returns its two coordinates as a number pair. <br>
    void coord(double& Xp, double& Yp) const;
    //! Computes the distance between two points. <br>
    double distance(const Pnt2d& Other) const;
    //! Comparison <br>
    //! Returns True if the distance between the two <br>
    //! points is lower or equal to LinearTolerance. <br>
    bool isEqual(const Pnt2d& Other, const double LinearTolerance) const;
    //! Performs the symmetrical transformation of a point <br>
    //! with respect to the point P which is the center of <br>
    //! the symmetry. <br>
    void mirror(const Pnt2d& P);

    //! Performs the symmetrical transformation of a point <br>
    //! with respect to an axis placement which is the axis <br>
    Pnt2d mirrored(const Pnt2d& P) const;

    void mirror(const Ax2d& A);

    //! Rotates a point. A1 is the axis of the rotation. <br>
    //! Ang is the angular value of the rotation in radians. <br>
    Pnt2d mirrored(const Ax2d& A) const;

    void rotate(const Pnt2d& P, const double Ang);
    //! Scales a point. S is the scaling value. <br>
    Pnt2d rotated(const Pnt2d& P, const double Ang) const;

    void scale(const Pnt2d& P, const double S);
    //! Transforms a point with the transformation T. <br>
    Pnt2d scaled(const Pnt2d& P, const double S) const;

    //! Assigns the value Xi to the coordinate that corresponds to Index: <br>
    //! Index = 1 => X is modified <br>
    //! Index = 2 => Y is modified <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    void setCoord(const int Index, const double Xi);
    //! For this point, assigns the values Xp and Yp to its two coordinates <br>
    void setCoord(const double Xp, const double Yp);
    //! Assigns the given value to the X coordinate of this point. <br>
    void setX(const double X);
    //! Assigns the two coordinates of Coord to this point. <br>
    void setXY(const XY& Coord);

    //! Assigns the given value to the Y coordinate of this point. <br>
    void setY(const double Y);
    //! Computes the square distance between two points. <br>
    double squareDistance(const Pnt2d& Other) const;

    void transform(const Trsf2d& T);
    //
    ////! Translates a point in the direction of the vector V. <br>
    ////! The magnitude of the translation is the vector's magnitude. <br>
    Pnt2d transformed(const Trsf2d& T) const;

    void translate(const Vec2d& V);
    //
    ////! Translates a point from the point P1 to the point P2. <br>
    Pnt2d translated(const Vec2d& V) const;

    void translate(const Pnt2d& P1, const Pnt2d& P2);

    Pnt2d translated(const Pnt2d& P1, const Pnt2d& P2) const;

    //! For this point, returns its x coordinate. <br>
    double x() const;
    //! For this point, returns its two coordinates as a number pair. <br>
    const XY& xy() const;
    //! For this point, returns its y coordinate. <br>
    double y() const;

    /// Checks whether two points are equal within linear tolerance (default 1E-07)
    bool operator==(const Geom::Pnt2d& other) const;
    /// Checks whether two points are unequal within linear tolerance (default 1E-07)
    bool operator!=(const Geom::Pnt2d& other) const;

protected:
private:
    XY _coord;
};

}  // namespace Geom