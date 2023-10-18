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
class Pnt;
class Trsf;
class Vec;

}  // namespace Geom

namespace Geom
{
//!  Describes a right-handed coordinate system in 3D space. <br>
//! A coordinate system is defined by: <br>
//! -   its origin (also referred to as its "Location point"), and <br>
//! -   three orthogonal unit vectors, termed respectively the <br>
//! "X Direction", the "Y Direction" and the "Direction" (also <br>
//!   referred to as the "main Direction"). <br>
//! The "Direction" of the coordinate system is called its <br>
//! "main Direction" because whenever this unit vector is <br>
//! modified, the "X Direction" and the "Y Direction" are <br>
//! recomputed. However, when we modify either the "X <br>
//! Direction" or the "Y Direction", "Direction" is not modified. <br>
//! The "main Direction" is also the "Z Direction". <br>
//! Since an Ax2 coordinate system is right-handed, its <br>
//! "main Direction" is always equal to the cross product of <br>
//! its "X Direction" and "Y Direction". (To define a <br>
//! left-handed coordinate system, use Geom::Ax3.) <br>
//! A coordinate system is used: <br>
//! -   to describe geometric entities, in particular to position <br>
//!   them. The local coordinate system of a geometric <br>
//!   entity serves the same purpose as the STEP function <br>
//!   "axis placement two axes", or <br>
//! -   to define geometric transformations. <br>
//! Note: we refer to the "X Axis", "Y Axis" and "Z Axis", <br>
//! respectively, as to axes having: <br>
//! - the origin of the coordinate system as their origin, and <br>
//! -   the unit vectors "X Direction", "Y Direction" and "main <br>
//!   Direction", respectively, as their unit vectors. <br>
//! The "Z Axis" is also the "main Axis". <br>

class LX_GEOM_EXPORT Ax2
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
    //! Creates an indefinite coordinate system. <br>
    Ax2() = default;

    //!  Creates an axis placement with an origin P such that: <br>
    //!   -   N is the Direction, and <br>
    //!   -   the "X Direction" is normal to N, in the plane <br>
    //!    defined by the vectors (N, Vx): "X <br>
    //!    Direction" = (N ^ Vx) ^ N, <br>
    //!  Exception: raises ConstructionError if N and Vx are parallel (same or opposite orientation). <br>
    Ax2(const Geom::Pnt& P, const Geom::Dir& N, const Geom::Dir& Vx);


    //!  Creates -   a coordinate system with an origin P, where V <br>
    //! gives the "main Direction" (here, "X Direction" and "Y <br>
    //!  Direction" are defined automatically). <br>
    Ax2(const Geom::Pnt& P, const Geom::Dir& V);

    Ax2(const Geom::Pnt& aP, const Geom::Dir& aZDir, const Geom::Dir& aYDir, const Geom::Dir& aXDir);

    //! Assigns the origin and "main Direction" of the axis A1 to <br>
    //! this coordinate system, then recomputes its "X Direction" and "Y Direction". <br>
    //! Note: The new "X Direction" is computed as follows: <br>
    //! new "X Direction" = V1 ^(previous "X Direction" ^ V) <br>
    //! where V is the "Direction" of A1. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if A1 is parallel to the "X <br>
    //! Direction" of this coordinate system. <br>
    void setAxis(const Geom::Ax1& A1);


    //!  Changes the "main Direction" of this coordinate system, <br>
    //! then recomputes its "X Direction" and "Y Direction". <br>
    //! Note: the new "X Direction" is computed as follows: <br>
    //! new "X Direction" = V ^ (previous "X Direction" ^ V) <br>
    //!   Exceptions <br>
    //! Standard_ConstructionError if V is parallel to the "X <br>
    //! Direction" of this coordinate system. <br>
    void setDirection(const Geom::Dir& V);


    //!  Changes the "Location" point (origin) of <me>. <br>
    void setLocation(const Geom::Pnt& P);


    //!  Changes the "Xdirection" of <me>. The main direction <br>
    //!  "Direction" is not modified, the "Ydirection" is modified. <br>
    //!  If <Vx> is not normal to the main direction then <XDirection> <br>
    //!  is computed as follows XDirection = Direction ^ (Vx ^ Direction). <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if Vx or Vy is parallel to <br>
    //! the "main Direction" of this coordinate system. <br>
    void setXDirection(const Geom::Dir& Vx);


    //!  Changes the "Ydirection" of <me>. The main direction is not <br>
    //!  modified but the "Xdirection" is changed. <br>
    //!  If <Vy> is not normal to the main direction then "YDirection" <br>
    //!  is computed as  follows <br>
    //!  YDirection = Direction ^ (<Vy> ^ Direction). <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if Vx or Vy is parallel to <br>
    //! the "main Direction" of this coordinate system. <br>
    void setYDirection(const Geom::Dir& Vy);


    //!  Computes the angular value, in radians, between the main direction of <br>
    //!  <me> and the main direction of <Other>. Returns the angle <br>
    //!  between 0 and PI in radians. <br>
    double angle(const Ax2& Other) const;

    //!  Returns the main axis of <me>. It is the "Location" point <br>
    //!  and the main "Direction". <br>
    const Geom::Ax1& axis() const;

    //!  Returns the main direction of <me>. <br>
    const Geom::Dir& direction() const;

    //!  Returns the "Location" point (origin) of <me>. <br>
    const Geom::Pnt& location() const;

    //!  Returns the "XDirection" of <me>. <br>
    const Geom::Dir& xDirection() const;

    //!  Returns the "YDirection" of <me>. <br>
    const Geom::Dir& yDirection() const;


    bool isCoplanar(const Ax2& Other, const double LinearTolerance, const double AngularTolerance) const;

    //!  Returns True if <br>
    //!  . the distance between <me> and the "Location" point of A1 <br>
    //!    is lower of equal to LinearTolerance and <br>
    //!  . the main direction of <me> and the direction of A1 are normal. <br>
    //! Note: the tolerance criterion for angular equality is given by AngularTolerance. <br>
    bool isCoplanar(const Geom::Ax1& A1, const double LinearTolerance, const double AngularTolerance) const;


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the point P, and assigns the result to this coordinate system. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    void mirror(const Geom::Pnt& P);


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the point P, and creates a new one. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    Ax2 mirrored(const Geom::Pnt& P) const;


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the axis A1, and assigns the result to this coordinate systeme. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    void mirror(const Geom::Ax1& A1);


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the axis A1, and  creates a new one. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    Ax2 mirrored(const Geom::Ax1& A1) const;


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the plane defined by the origin, "X Direction" and "Y <br>
    //!   Direction" of coordinate system A2 and  assigns the result to this coordinate systeme. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    void mirror(const Ax2& A2);


    //! Performs a symmetrical transformation of this coordinate <br>
    //! system with respect to: <br>
    //! -   the plane defined by the origin, "X Direction" and "Y <br>
    //!   Direction" of coordinate system A2 and creates a new one. <br>
    //! Warning <br>
    //! This transformation is always performed on the origin. <br>
    //! In case of a reflection with respect to a point: <br>
    //! - the main direction of the coordinate system is not changed, and <br>
    //! - the "X Direction" and the "Y Direction" are simply reversed <br>
    //! In case of a reflection with respect to an axis or a plane: <br>
    //!   -   the transformation is applied to the "X Direction" <br>
    //!    and the "Y Direction", then <br>
    //!   -   the "main Direction" is recomputed as the cross <br>
    //!    product "X Direction" ^ "Y   Direction". <br>
    //!  This maintains the right-handed property of the <br>
    //! coordinate system. <br>
    Ax2 mirrored(const Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  Rotates an axis placement. <A1> is the axis of the <br>
    //!  rotation . Ang is the angular value of the rotation <br>
    //!  in radians. <br>
    Ax2 rotated(const Geom::Ax1& A1, const double Ang) const;

    void scale(const Geom::Pnt& P, const double S);

    //!  Applies a scaling transformation on the axis placement. <br>
    //!  The "Location" point of the axisplacement is modified. <br>
    //! Warnings : <br>
    //!  If the scale <S> is negative : <br>
    //!   . the main direction of the axis placement is not changed. <br>
    //!   . The "XDirection" and the "YDirection" are reversed. <br>
    //!  So the axis placement stay right handed. <br>
    Ax2 scaled(const Geom::Pnt& P, const double S) const;

    void transform(const Geom::Trsf& T);

    //!  Transforms an axis placement with a Trsf. <br>
    //!  The "Location" point, the "XDirection" and the <br>
    //!  "YDirection" are transformed with T.  The resulting <br>
    //!  main "Direction" of <me> is the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation. <br>
    Ax2 transformed(const Geom::Trsf& T) const;

    void translate(const Geom::Vec& V);

    //!  Translates an axis plaxement in the direction of the vector <br>
    //!  <V>. The magnitude of the translation is the vector's magnitude. <br>
    Ax2 translated(const Geom::Vec& V) const;

    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //!  Translates an axis placement from the point <P1> to the <br>
    //!  point <P2>. <br>
    Ax2 translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


    bool isEqual(const Ax2& Other, const double tolerance) const;


private:
    Ax1 myaxis = Ax1({0, 0, 0}, {0, 0, 1});
    Dir vydir = Dir(XYZ{0, 1, 0});
    Dir vxdir = Dir(XYZ{1, 0, 0});
};

}  // namespace Geom
