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

#include <Geom/Dir.h>
#include <Geom/Pnt.h>


namespace Geom
{
class Ax2;
class Trsf;
class Vec;
}  // namespace Geom

namespace Geom
{
//! Describes an axis in 3D space. <br>
//! An axis is defined by: <br>
//! -   its origin (also referred to as its "Location point"), and <br>
//! -   its unit vector (referred to as its "Direction" or "main   Direction"). <br>
//! An axis is used: <br>
//! -   to describe 3D geometric entities (for example, the <br>
//! axis of a revolution entity). It serves the same purpose <br>
//! as the STEP function "axis placement one axis", or <br>
//! -   to define geometric transformations (axis of <br>
//!   symmetry, axis of rotation, and so on). <br>
//! For example, this entity can be used to locate a geometric entity <br>
//!  or to define a symmetry axis. <br>
class LX_GEOM_EXPORT Ax1
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
    //! Creates a undefined Ax1. <br>
    Ax1() = default;

    //!  P is the location point and V is the direction of <me>. <br>
    Ax1(const Geom::Pnt& P, const Geom::Dir& V);
    //! Assigns V as the "Direction"  of this axis. <br>
    void setDirection(const Geom::Dir& V);
    //! Assigns  P as the origin of this axis. <br>
    void setLocation(const Geom::Pnt& P);
    //! Returns the direction of <me>. <br>
    const Geom::Dir& direction() const;
    //! Returns the location point of <me>. <br>
    const Geom::Pnt& location() const;


    //!  Returns True if  : <br>
    //!  . the angle between <me> and <Other> is lower or equal <br>
    //!    to <AngularTolerance> and <br>
    //!  . the distance between <me>.Location() and <Other> is lower <br>
    //!    or equal to <LinearTolerance> and <br>
    //!  . the distance between <Other>.Location() and <me> is lower <br>
    //!    or equal to LinearTolerance. <br>
    bool isCoaxial(const Ax1& Other, const double AngularTolerance, const double LinearTolerance) const;

    //!  Returns True if the direction of the <me> and <Other> <br>
    //!  are normal to each other. <br>
    //! That is, if the angle between the two axes is equal to Pi/2. <br>
    //! Note: the tolerance criterion is given by AngularTolerance.. <br>
    bool isNormal(const Ax1& Other, const double AngularTolerance) const;

    //!  Returns True if the direction of <me> and <Other> are <br>
    //!  parallel with opposite orientation. That is, if the angle <br>
    //! between the two axes is equal to Pi. <br>
    //! Note: the tolerance criterion is given by AngularTolerance. <br>
    bool isOpposite(const Ax1& Other, const double AngularTolerance) const;

    //!  Returns True if the direction of <me> and <Other> are <br>
    //!  parallel with same orientation or opposite orientation. That <br>
    //! is, if the angle between the two axes is equal to 0 or Pi. <br>
    //! Note: the tolerance criterion is given by <br>
    //! AngularTolerance. <br>
    bool isParallel(const Ax1& Other, const double AngularTolerance) const;

    //!  Computes the angular value, in radians, between <me>.Direction() and <br>
    //!  <Other>.Direction(). Returns the angle between 0 and 2*PI <br>
    //!  radians. <br>
    double angle(const Ax1& Other) const;
    //!  Reverses the unit vector of this axis. <br>
    //! and  assigns the result to this axis. <br>
    void reverse();
    //! Reverses the unit vector of this axis and creates a new one. <br>
    Ax1 reversed() const;


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to the point P which is the <br>
    //!  center of the symmetry and assigns the result to this axis. <br>
    void mirror(const Geom::Pnt& P);

    //! Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to the point P which is the <br>
    //!  center of the symmetry and creates a new axis. <br>
    Ax1 mirrored(const Geom::Pnt& P) const;


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to an axis placement which <br>
    //!  is the axis of the symmetry and assigns the result to this axis. <br>
    void mirror(const Ax1& A1);


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to an axis placement which <br>
    //!  is the axis of the symmetry and creates a new axis. <br>
    Ax1 mirrored(const Ax1& A1) const;


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to a plane. The axis placement <br>
    //!  <A2> locates the plane of the symmetry : <br>
    //!  (Location, XDirection, YDirection) and assigns the result to this axis. <br>
    void mirror(const Geom::Ax2& A2);


    //!  Performs the symmetrical transformation of an axis <br>
    //!  placement with respect to a plane. The axis placement <br>
    //!  <A2> locates the plane of the symmetry : <br>
    //!  (Location, XDirection, YDirection) and creates a new axis. <br>
    Ax1 mirrored(const Geom::Ax2& A2) const;
    //! Rotates this axis at an angle Ang (in radians) about the axis A1 <br>
    //! and assigns the result to this axis. <br>
    void rotate(const Ax1& A1, const double Ang);
    //! Rotates this axis at an angle Ang (in radians) about the axis A1 <br>
    //! and creates a new one. <br>
    Ax1 rotated(const Ax1& A1, const double Ang) const;

    //! Applies a scaling transformation to this axis with: <br>
    //! -   scale factor S, and <br>
    //! -   center P and assigns the result to this axis. <br>
    void scale(const Geom::Pnt& P, const double S);

    //! Applies a scaling transformation to this axis with: <br>
    //! -   scale factor S, and <br>
    //! -   center P and creates a new axis. <br>
    Ax1 scaled(const Geom::Pnt& P, const double S) const;
    //! Applies the transformation T to this axis. <br>
    //! and assigns the result to this axis. <br>
    void transform(const Geom::Trsf& T);

    //! Applies the transformation T to this axis and creates a new one. <br>
    //!  Translates an axis plaxement in the direction of the vector <br>
    //!  <V>. The magnitude of the translation is the vector's magnitude. <br>
    Ax1 transformed(const Geom::Trsf& T) const;

    //! Translates this axis by the vector V, <br>
    //! and assigns the result to this axis. <br>
    void translate(const Geom::Vec& V);

    //! Translates this axis by the vector V, <br>
    //! and creates a new one. <br>
    Ax1 translated(const Geom::Vec& V) const;

    //! Translates this axis by: <br>
    //! the vector (P1, P2) defined from point P1 to point P2. <br>
    //! and assigns the result to this axis. <br>
    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //! Translates this axis by: <br>
    //! the vector (P1, P2) defined from point P1 to point P2. <br>
    //! and creates a new one. <br>
    Ax1 translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

private:
    Geom::Pnt loc;
    Geom::Dir vdir;
};

}  // namespace Geom
