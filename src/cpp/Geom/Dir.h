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
class Dir;


//! Describes a unit vector in 3D space. This unit vector is also called "Direction". <br>
//! See Also <br>
//! gce_MakeDir which provides functions for more complex <br>
//! unit vector constructions <br>
//! Geom_Direction which provides additional functions for <br>
//! constructing unit vectors and works, in particular, with the <br>
//! parametric equations of unit vectors. <br>
class LX_GEOM_EXPORT Dir
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    // Methods PUBLIC
    //
    //! Creates an indefinite direction. <br>
    Dir();
    //! Normalizes the vector V and creates a direction. Raises ConstructionError if V.Magnitude() <= Resolution. <br>
    Dir(const Geom::Vec& V);
    //! Creates a direction from a triplet of coordinates. Raises ConstructionError if Coord.Modulus() <= Resolution from gp. <br>
    Dir(const Geom::XYZ& Coord);
    //! Creates a direction with its 3 cartesian coordinates. Raises ConstructionError if Sqrt(Xv*Xv + Yv*Yv + Zv*Zv) <= Resolution <br>//!
    //! Modification of the direction's coordinates <br>
    //!  If Sqrt (X*X + Y*Y + Z*Z) <= Resolution from gp where <br>
    //!  X, Y ,Z are the new coordinates it is not possible to <br>
    //!  construct the direction and the method raises the <br>
    //!  exception ConstructionError. <br>
    Dir(const double Xv, const double Yv, const double Zv);
    //! Copy constructor
    Dir(const Dir& rhs);

    // named constr.
    static Dir XDir() { return Dir(1, 0, 0); };
    static Dir YDir() { return Dir(0, 1, 0); };
    static Dir ZDir() { return Dir(0, 0, 1); };

    //! For this unit vector,  assigns the value Xi to: <br>
    //!   -   the X coordinate if Index is 1, or <br>
    //!   -   the Y coordinate if Index is 2, or <br>
    //!   -   the Z coordinate if Index is 3, <br>
    //!   and then normalizes it. <br>
    //! Warning <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    //! Exceptions <br>
    //! Standard_OutOfRange if Index is not 1, 2, or 3. <br>
    //! Standard_ConstructionError if either of the following <br>
    //! is less than or equal to Geom::Precision::linear_Resolution(): <br>
    //! -   Sqrt(Xv*Xv + Yv*Yv + Zv*Zv), or <br>
    //! -   the modulus of the number triple formed by the new <br>
    //!   value Xi and the two other coordinates of this vector <br>
    //!   that were not directly modified. <br>
    void setCoord(const int Index, const double Xi);
    //! For this unit vector,  assigns the values Xv, Yv and Zv to its three coordinates. <br>
    //! Remember that all the coordinates of a unit vector are <br>
    //! implicitly modified when any single one is changed directly. <br>
    void setCoord(const double Xv, const double Yv, const double Zv);
    //! Assigns the given value to the X coordinate of this   unit vector. <br>
    void setX(const double X);
    //! Assigns the given value to the Y coordinate of this   unit vector. <br>
    void setY(const double Y);
    //! Assigns the given value to the Z  coordinate of this   unit vector. <br>
    void setZ(const double Z);
    //! Assigns the three coordinates of Coord to this unit vector. <br>
    void setXYZ(const Geom::XYZ& Coord);

    //!  Returns the coordinate of range Index : <br>
    //!  Index = 1 => X is returned <br>
    //!  Index = 2 => Y is returned <br>
    //!  Index = 3 => Z is returned <br>
    //! Exceptions <br>
    //! Standard_OutOfRange if Index is not 1, 2, or 3. <br>
    double coord(const int Index) const;
    //! Returns for the  unit vector  its three coordinates Xv, Yv, and Zv. <br>
    void coord(double& Xv, double& Yv, double& Zv) const;
    //! Returns the X coordinate for a  unit vector. <br>
    double x() const;
    //! Returns the Y coordinate for a  unit vector. <br>
    double y() const;
    //! Returns the Z coordinate for a  unit vector. <br>
    double z() const;
    //! for this unit vector, returns  its three coordinates as a number triplea. <br>
    const Geom::XYZ& xyz() const;

    //!  Returns True if the angle between the two directions is <br>
    //!  lower or equal to AngularTolerance. <br>
    bool isEqual(const Dir& Other, const double AngularTolerance) const;

    //!  Returns True if  the angle between this unit vector and the unit vector Other is equal to Pi/2 (normal). <br>
    bool isNormal(const Dir& Other, const double AngularTolerance) const;

    //!  Returns True if  the angle between this unit vector and the unit vector Other is equal to  Pi (opposite). <br>
    bool isOpposite(const Dir& Other, const double AngularTolerance) const;

    //! Returns true if the angle between this unit vector and the <br>
    //! unit vector Other is equal to 0 or to Pi. <br>
    //! Note: the tolerance criterion is given by AngularTolerance. <br>
    bool isParallel(const Dir& Other, const double AngularTolerance) const;


    //!  Computes the angular value in radians between <me> and <br>
    //!  <Other>. This value is always positive in 3D space. <br>
    //!  Returns the angle in the range [0, PI] <br>
    double angle(const Dir& Other) const;


    //!  Computes the angular value between <me> and <Other>. <br>
    //!  <VRef> is the direction of reference normal to <me> and <Other> <br>
    //!  and its orientation gives the positive sense of rotation. <br>
    //!  If the cross product <me> ^ <Other> has the same orientation <br>
    //!  as <VRef> the angular value is positive else negative. <br>
    //!  Returns the angular value in the range -PI and PI (in radians). Raises  DomainError if <me> and <Other> are not parallel this exception is
    //!  raised <br> when <VRef> is in the same plane as <me> and <Other> <br> The tolerance criterion is Resolution from package gp. <br>
    double angleWithRef(const Dir& Other, const Dir& VRef) const;
    //! Computes the cross product between two directions <br>
    //!  Raises the exception ConstructionError if the two directions <br>
    //!  are parallel because the computed vector cannot be normalized <br>
    //!  to create a direction. <br>
    void cross(const Dir& Right);
    void operator^=(const Dir& Right) { cross(Right); }

    //! Computes the triple vector product. <br>
    //!  <me> ^ (V1 ^ V2) <br>
    //!  Raises the exception ConstructionError if V1 and V2 are parallel <br>
    //!  or <me> and (V1^V2) are parallel because the computed vector <br>
    //!  can't be normalized to create a direction. <br>
    Dir crossed(const Dir& Right) const;
    Dir operator^(const Dir& Right) const { return crossed(Right); }


    void crossCross(const Dir& V1, const Dir& V2);
    //!  Computes the double vector product this ^ (V1 ^ V2). <br>
    //!  -   CrossCrossed creates a new unit vector. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if: <br>
    //! -   V1 and V2 are parallel, or <br>
    //! -   this unit vector and (V1 ^ V2) are parallel. <br>
    //! This is because, in these conditions, the computed vector <br>
    //! is null and cannot be normalized. <br>
    Dir crossCrossed(const Dir& V1, const Dir& V2) const;
    //! Computes the scalar product <br>
    double dot(const Dir& Other) const;
    double operator*(const Dir& Other) const { return dot(Other); }


    //!  Computes the triple scalar product <me> * (V1 ^ V2). <br>
    //! Warnings : <br>
    //!  The computed vector V1' = V1 ^ V2 is not normalized <br>
    //!  to create a unitary vector. So this method never <br>
    //!  raises an exception even if V1 and V2 are parallel. <br>
    double dotCross(const Dir& V1, const Dir& V2) const;

    void reverse();
    //! Reverses the orientation of a direction <br>//! geometric transformations <br>
    //!  Performs the symmetrical transformation of a direction <br>
    //!  with respect to the direction V which is the center of <br>
    //!  the  symmetry.] <br>
    Dir reversed() const;
    Dir operator-() const { return reversed(); }



    void mirror(const Dir& V);


    //!  Performs the symmetrical transformation of a direction <br>
    //!  with respect to the direction V which is the center of <br>
    //!  the  symmetry. <br>
    Dir mirrored(const Dir& V) const;


    void mirror(const Geom::Ax1& A1);


    //!  Performs the symmetrical transformation of a direction <br>
    //!  with respect to an axis placement which is the axis <br>
    //!  of the symmetry. <br>
    Dir mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);


    //!  Performs the symmetrical transformation of a direction <br>
    //!  with respect to a plane. The axis placement A2 locates <br>
    //!  the plane of the symmetry : (Location, XDirection, YDirection). <br>
    Dir mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  Rotates a direction. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Dir rotated(const Geom::Ax1& A1, const double Ang) const;


    void transform(const Geom::Trsf& T);

    //!  Transforms a direction with a "Trsf" from gp. <br>
    //! Warnings : <br>
    //!  If the scale factor of the "Trsf" T is negative then the <br>
    //!  direction <me> is reversed. <br>
    Dir transformed(const Geom::Trsf& T) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Checks whether two points are equal within linear tolerance (default 1E-07)
    bool operator==(const Geom::Dir& other) const;


    double& operator[](int i);
    const double& operator[](int i) const;


private:
    Geom::XYZ _coord;
};
    LX_GEOM_EXPORT QString to_string(const Dir& dir);

}  // namespace Geom
