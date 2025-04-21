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

#include <Geom/XYZ.h> 
#include <QString>
namespace Geom
{
class Ax1;
class Ax2;
class Trsf;
class Vec;
class Pnt;
}  // namespace Geom

typedef std::vector<Geom::Pnt> PNTS;




namespace Geom
{
    //!  Defines a non-persistent 3D Cartesian point. <br>
class LX_GEOM_EXPORT Pnt
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    //! Creates an indefinite point. <br>
    Pnt();
    //! Creates a point with a triplet of coordinates. <br>
    Pnt(const Geom::XYZ& Coord);

    //!  Creates a  point with its 3 Cartesian's coordinates : Xp, Yp, Zp. <br>
    Pnt(const double Xp, const double Yp, const double Zp = .0);

    //! Copy constructor
    Pnt(const Pnt& rhs);

    static Pnt ZeroPnt() { return Pnt(0, 0, 0); };

    //!  Changes the coordinate of range Index : <br>
    //!  Index = 1 => X is modified <br>
    //!  Index = 2 => Y is modified <br>
    //!  Index = 3 => Z is modified <br>//! Raised if Index != {1, 2, 3}. <br>
    void setCoord(const int Index, const double Xi);
    //! For this point, assigns  the values Xp, Yp and Zp to its three coordinates. <br>
    void setCoord(const double Xp, const double Yp, const double Zp = .0);
    //! Assigns the given value to the X coordinate of this point. <br>
    void setX(const double X);
    //! Assigns the given value to the Y coordinate of this point. <br>
    void setY(const double Y);
    //! Assigns the given value to the Z coordinate of this point. <br>
    void setZ(const double Z);
    //! Assigns the three coordinates of Coord to this point. <br>
    void setXYZ(const Geom::XYZ& Coord);

    //!  Returns the coordinate of corresponding to the value of  Index : <br>
    //!  Index = 1 => X is returned <br>
    //!  Index = 2 => Y is returned <br>
    //!  Index = 3 => Z is returned <br>
    //! Raises OutOfRange if Index != {1, 2, 3}. <br>//! Raised if Index != {1, 2, 3}. <br>
    double coord(const int Index) const;
    //! For this point gives its three coordinates Xp, Yp and Zp. <br>
    void coord(double& Xp, double& Yp, double& Zp) const;
    //! For this point, returns its X coordinate. <br>
    double x() const;
    //! For this point, returns its X coordinate. <br>
    double y() const;
    //! For this point, returns its X coordinate. <br>
    double z() const;

    float fx() const;
    float fy() const;
    float fz() const;
    //! For this point, returns its three coordinates as a number triple. <br>
    const Geom::XYZ& xyz() const;
    //! For this point, returns its three coordinates as a number triple. <br>
    const Geom::XYZ& coord() const;

    //! Returns the coordinates of this point. <br>
    //! Note: This syntax allows direct modification of the returned value. <br>
    Geom::XYZ& changeCoord();
    //! Assigns the result of the following expression to this point <br>
    //! (Alpha*this + Beta*P) / (Alpha + Beta) <br>
    void baryCenter(const double Alpha, const Pnt& P, const double Beta);
    //! Comparison <br>
    //!  Returns True if the distance between the two points is <br>
    //!  lower or equal to LinearTolerance. <br>
    bool isEqual(const Pnt& Other, const double LinearTolerance) const;
    //! Computes the distance between two points. <br>
    double distance(const Pnt& Other) const;
    //! Computes the square distance between two points. <br>
    double squareDistance(const Pnt& Other) const;


    //!  Performs the symmetrical transformation of a point <br>
    //!  with respect to the point P which is the center of <br>
    //!  the  symmetry. <br>
    void mirror(const Pnt& P);


    //!  Performs the symmetrical transformation of a point <br>
    //!  with respect to an axis placement which is the axis <br>
    //!  of the symmetry. <br>
    Pnt mirrored(const Pnt& P) const;


    void mirror(const Geom::Ax1& A1);


    //!  Performs the symmetrical transformation of a point <br>
    //!  with respect to a plane. The axis placement A2 locates <br>
    //!  the plane of the symmetry : (Location, XDirection, YDirection). <br>
    Pnt mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);


    //!  Rotates a point. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Pnt mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);
    Pnt rotated(const Geom::Ax1& A1, const double Ang) const;

    //! Scales a point. S is the scaling value. <br>
    void scale(const Pnt& P, const double S);
    Pnt scaled(const Pnt& P, const double S) const;


    //! Transforms a point with the transformation T. <br>
    void transform(const Geom::Trsf& T);
    Pnt transformed(const Geom::Trsf& T) const;

    //!  Translates a point in the direction of the vector V. <br>
    //!  The magnitude of the translation is the vector's magnitude. <br>
    void translate(const Geom::Vec& V);

    //!  Translates a point from the point P1 to the point P2. <br>
    Pnt translated(const Geom::Vec& V) const;
    void translate(const Pnt& P1, const Pnt& P2);
    Pnt translated(const Pnt& P1, const Pnt& P2) const;

    /// Checks whether two points are equal within linear tolerance (default 1E-07)
    bool operator==(const Geom::Pnt& other) const;
    /// Checks whether two points are unequal within linear tolerance (default 1E-07)
    bool operator!=(const Geom::Pnt& other) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    double& operator[](int i);
    const double& operator[](int i) const;

    Pnt operator-(const Geom::Pnt& other) const;
    Pnt operator+(const Geom::Pnt& other) const;
    Pnt operator*(const Geom::Pnt& other) const;
    Pnt operator*(double scalar) const;

    bool operator<(const Geom::Pnt& rhs) const;

private:
    Geom::XYZ _coord;
};

LX_GEOM_EXPORT QString to_string(const Pnt& pnt);

}  // namespace Geom
