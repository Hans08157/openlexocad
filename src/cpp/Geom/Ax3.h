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

#include <Geom/Ax1.h>

namespace Geom
{
class Ax2;
class Trsf;
class Vec;
class Pnt;

//! Describes a coordinate system in 3D space. Unlike a <br>
//!  Geom::Ax2 coordinate system, a Ax3 can be <br>
//! right-handed ("direct sense) or left-handed ("indirect sense"). <br>
//! A coordinate system is defined by: <br>
//! -   its origin (also referred to as its "Location point"), and <br>
//! -   three orthogonal unit vectors, termed the "X <br>
//!   Direction", the "Y Direction" and the "Direction" (also <br>
//!   referred to as the "main Direction"). <br>
//! The "Direction" of the coordinate system is called its <br>
//! "main Direction" because whenever this unit vector is <br>
//! modified, the "X Direction" and the "Y Direction" are <br>
//! recomputed. However, when we modify either the "X <br>
//! Direction" or the "Y Direction", "Direction" is not modified. <br>
//! "Direction" is also the "Z Direction". <br>
//! The "main Direction" is always parallel to the cross <br>
//! product of its "X Direction" and "Y Direction". <br>
//! If the coordinate system is right-handed, it satisfies the equation: <br>
//! "main Direction" = "X Direction" ^ "Y Direction" <br>
//! and if it is left-handed, it satisfies the equation: <br>
//! "main Direction" = -"X Direction" ^ "Y Direction" <br>
//! A coordinate system is used: <br>
//! -   to describe geometric entities, in particular to position <br>
//!   them. The local coordinate system of a geometric <br>
//!   entity serves the same purpose as the STEP function <br>
//!   "axis placement three axes", or <br>
//! -   to define geometric transformations. <br>
//! Note: <br>
//! -   We refer to the "X Axis", "Y Axis" and "Z Axis", <br>
//!   respectively, as the axes having: <br>
//! -   the origin of the coordinate system as their origin, and <br>
//! -   the unit vectors "X Direction", "Y Direction" and <br>
//!    "main Direction", respectively, as their unit vectors. <br>
//! -   The "Z Axis" is also the "main Axis". <br>
//! -   Geom::Ax2 is used to define a coordinate system that must be always right-handed. <br>
class LX_GEOM_EXPORT Ax3
{
public:
    // Methods PUBLIC
    //

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    //! Creates an indefinite coordinate system. <br>
    Ax3();

    //! Creates  a  coordinate  system from a right-handed <br>
    //!          coordinate system. <br>
    Ax3(const Geom::Ax2& A);

    //!  Creates a  right handed axis placement with the <br>
    //!  "Location"  point  P  and  two  directions, N    gives the <br>
    //!  "Direction" and Vx gives the "XDirection". <br>
    //!  Raises ConstructionError if N and Vx are parallel (same or opposite orientation). <br>
    Ax3(const Geom::Pnt& P, const Geom::Dir& N, const Geom::Dir& Vx);


    //!  Creates an axis placement with the  "Location" point <P> <br>
    //!  and the normal direction <V>. <br>
    Ax3(const Geom::Pnt& P, const Geom::Dir& V);

    //! Reverses the X direction of <me>. <br>
    void xReverse();

    //! Reverses the Y direction of <me>. <br>
    void yReverse();

    //! Reverses the Z direction of <me>. <br>
    void zReverse();

    //! Assigns the origin and "main Direction" of the axis A1 to <br>
    //! this coordinate system, then recomputes its "X Direction" and "Y Direction". <br>
    //! Note: <br>
    //! -   The new "X Direction" is computed as follows: <br>
    //! new "X Direction" = V1 ^(previous "X Direction" ^ V) <br>
    //! where V is the "Direction" of A1. <br>
    //! -   The orientation of this coordinate system <br>
    //!   (right-handed or left-handed) is not modified. <br>
    //!  Raises ConstructionError  if the "Direction" of <A1> and the "XDirection" of <me> <br>
    //!  are parallel (same or opposite orientation) because it is <br>
    //!  impossible to calculate the new "XDirection" and the new <br>
    //!  "YDirection". <br>
    void setAxis(const Geom::Ax1& A1);


    //!  Changes the main direction of this coordinate system, <br>
    //! then recomputes its "X Direction" and "Y Direction". <br>
    //! Note: <br>
    //! -   The new "X Direction" is computed as follows: <br>
    //! new "X Direction" = V ^ (previous "X Direction" ^ V). <br>
    //! -   The orientation of this coordinate system (left- or right-handed) is not modified. <br>
    //! Raises ConstructionError if <V< and the previous "XDirection" are parallel <br>
    //!  because it is impossible to calculate the new "XDirection" <br>
    //!  and the new "YDirection". <br>
    void setDirection(const Geom::Dir& V);


    //!  Changes the "Location" point (origin) of <me>. <br>
    void setLocation(const Geom::Pnt& P);


    //!  Changes the "Xdirection" of <me>. The main direction <br>
    //!  "Direction" is not modified, the "Ydirection" is modified. <br>
    //!  If <Vx> is not normal to the main direction then <XDirection> <br>
    //!  is computed as follows XDirection = Direction ^ (Vx ^ Direction). <br>
    //! Raises ConstructionError if <Vx> is parallel (same or opposite <br>
    //! orientation) to the main direction of <me> <br>
    void setXDirection(const Geom::Dir& Vx);

    //!  Changes the "Ydirection" of <me>. The main direction is not <br>
    //!  modified but the "Xdirection" is changed. <br>
    //!  If <Vy> is not normal to the main direction then "YDirection" <br>
    //!  is computed as  follows <br>
    //!  YDirection = Direction ^ (<Vy> ^ Direction). <br>
    //! Raises ConstructionError if <Vy> is parallel to the main direction of <me> <br>
    void setYDirection(const Geom::Dir& Vy);

    //!  Computes the angular value between the main direction of <br>
    //!  <me> and the main direction of <Other>. Returns the angle <br>
    //!  between 0 and PI in radians. <br>
    double angle(const Ax3& Other) const;

    //!  Returns the main axis of <me>. It is the "Location" point <br>
    //!  and the main "Direction". <br>
    const Geom::Ax1& axis() const;

    //! Computes a right-handed coordinate system with the <br>
    //! same "X Direction" and "Y Direction" as those of this <br>
    //! coordinate system, then recomputes the "main Direction". <br>
    //! If this coordinate system is right-handed, the result <br>
    //! returned is the same coordinate system. If this <br>
    //! coordinate system is left-handed, the result is reversed. <br>
    Geom::Ax2 axis2() const;

    //!  Returns the main direction of <me>. <br>
    const Geom::Dir& direction() const;

    //!  Returns the "Location" point (origin) of <me>. <br>
    const Geom::Pnt& location() const;

    //!  Returns the "XDirection" of <me>. <br>
    const Geom::Dir& xDirection() const;

    //!  Returns the "YDirection" of <me>. <br>
    const Geom::Dir& yDirection() const;
    //! Returns  True if  the  coordinate  system is right-handed. i.e. <br>
    //!          XDirection().Crossed(YDirection()).Dot(Direction()) > 0 <br>
    bool direct() const;

    //!  Returns True if <br>
    //!  . the distance between the "Location" point of <me> and <br>
    //!    <Other> is lower or equal to LinearTolerance and <br>
    //!  . the distance between the "Location" point of <Other> and <br>
    //!    <me> is lower or equal to LinearTolerance and <br>
    //!  . the main direction of <me> and the main direction of <br>
    //!    <Other> are parallel (same or opposite orientation). <br>
    bool isCoplanar(const Ax3& Other, const double LinearTolerance, const double AngularTolerance) const;
    //! Returns True if <br>
    //!  . the distance between <me> and the "Location" point of A1 <br>
    //!    is lower of equal to LinearTolerance and <br>
    //!  . the distance between A1 and the "Location" point of <me> <br>
    //!    is lower or equal to LinearTolerance and <br>
    //!  . the main direction of <me> and the direction of A1 are normal. <br>
    bool isCoplanar(const Geom::Ax1& A1, const double LinearTolerance, const double AngularTolerance) const;


    void mirror(const Geom::Pnt& P);


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to the point P which is the <br>
    //!  center of the symmetry. <br>
    //!  Warnings : <br>
    //!  The main direction of the axis placement is not changed. <br>
    //!  The "XDirection" and the "YDirection" are reversed. <br>
    //!  So the axis placement stay right handed. <br>
    Ax3 mirrored(const Geom::Pnt& P) const;


    void mirror(const Geom::Ax1& A1);


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to an axis placement which <br>
    //!  is the axis of the symmetry. <br>
    //!  The transformation is performed on the "Location" <br>
    //!  point, on the "XDirection" and "YDirection". <br>
    //!  The resulting main "Direction" is the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation. <br>
    Ax3 mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to a plane. <br>
    //!  The axis placement  <A2> locates the plane of the symmetry : <br>
    //!  (Location, XDirection, YDirection). <br>
    //!  The transformation is performed on the "Location" <br>
    //!  point, on the "XDirection" and "YDirection". <br>
    //!  The resulting main "Direction" is the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation. <br>
    Ax3 mirrored(const Geom::Ax2& A2) const;


    void rotate(const Geom::Ax1& A1, const double Ang);


    //!  Rotates an axis placement. <A1> is the axis of the <br>
    //!  rotation . Ang is the angular value of the rotation <br>
    //!  in radians. <br>
    Ax3 rotated(const Geom::Ax1& A1, const double Ang) const;


    void scale(const Geom::Pnt& P, const double S);


    //!  Applies a scaling transformation on the axis placement. <br>
    //!  The "Location" point of the axisplacement is modified. <br>
    //! Warnings : <br>
    //!  If the scale <S> is negative : <br>
    //!   . the main direction of the axis placement is not changed. <br>
    //!   . The "XDirection" and the "YDirection" are reversed. <br>
    //!  So the axis placement stay right handed. <br>
    Ax3 scaled(const Geom::Pnt& P, const double S) const;


    void transform(const Geom::Trsf& T);


    //!  Transforms an axis placement with a Trsf. <br>
    //!  The "Location" point, the "XDirection" and the <br>
    //!  "YDirection" are transformed with T.  The resulting <br>
    //!  main "Direction" of <me> is the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation. <br>
    Ax3 transformed(const Geom::Trsf& T) const;


    void translate(const Geom::Vec& V);


    //!  Translates an axis plaxement in the direction of the vector <br>
    //!  <V>. The magnitude of the translation is the vector's magnitude. <br>
    Ax3 translated(const Geom::Vec& V) const;


    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);


    //!  Translates an axis placement from the point <P1> to the <br>
    //!  point <P2>. <br>
    Ax3 translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


private:
    Geom::Ax1 myaxis;
    Geom::Dir vydir;
    Geom::Dir vxdir;
};

}  // namespace Geom
