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

#include <Geom/Dir2d.h>
#include <Geom/Pnt2d.h>

namespace Geom { class Trsf2d; }
namespace Geom { class Vec2d; }

namespace Geom
{
//! Describes an axis in the plane (2D space). <br>
//! An axis is defined by: <br>
//! - its origin (also referred to as its "Location point"), and <br>
//! - its unit vector (referred to as its "Direction"). <br>
//! An axis implicitly defines a direct, right-handed <br>
//! coordinate system in 2D space by: <br>
//! - its origin, <br>
//! - its "Direction" (giving the "X Direction" of the coordinate system), and <br>
//! - the unit vector normal to "Direction" (positive angle <br>
//! measured in the trigonometric sense). <br>
//! An axis is used: <br>
//! - to describe 2D geometric entities (for example, the <br>
//! axis which defines angular coordinates on a circle). <br>
//! It serves for the same purpose as the STEP function <br>
//! "axis placement one axis", or <br>
//! - to define geometric transformations (axis of <br>
//! symmetry, axis of rotation, and so on). <br>
//! Note: to define a left-handed 2D coordinate system, use Ax22d. <br>
class LX_GEOM_EXPORT Ax2d
{
public:
    //! Creates an indefinite Ax2d <br>
    Ax2d();

    //! Creates an Ax2d. <P> is the "Location" point of <br>
    //! the axis placement and V is the "Direction" of <br>
    //! the axis placement. <br>
    Ax2d(const Pnt2d& P, const Dir2d& V);
    //! Computes the angle, in radians, between this axis and <br>
    //! the axis Other. The value of the angle is between -Pi and Pi. <br>
    double angle(const Ax2d& Other) const;
    //! Returns the direction of <me>. <br>
    const Dir2d& direction() const;

    //! Returns True if : <br>
    //! . the angle between <me> and <Other> is lower or equal <br>
    //! to <AngularTolerance> and <br>
    //! . the distance between <me>.Location() and <Other> is lower <br>
    //! or equal to <LinearTolerance> and <br>
    //! . the distance between <Other>.Location() and <me> is lower <br>
    //! or equal to LinearTolerance. <br>
    bool isCoaxial(const Ax2d& Other, const double AngularTolerance, const double LinearTolerance) const;
    //! Returns true if this axis and the axis Other are normal to <br>
    //! each other. That is, if the angle between the two axes is equal to Pi/2 or -Pi/2. <br>
    //! Note: the tolerance criterion is given by AngularTolerance. <br>
    bool isNormal(const Ax2d& Other, const double AngularTolerance) const;
    //! Returns true if this axis and the axis Other are parallel, <br>
    //! and have opposite orientations. That is, if the angle <br>
    //! between the two axes is equal to Pi or -Pi. <br>
    //! Note: the tolerance criterion is given by AngularTolerance. <br>
    bool isOpposite(const Ax2d& Other, const double AngularTolerance) const;
    //! Returns true if this axis and the axis Other are parallel, <br>
    //! and have either the same or opposite orientations. That <br>
    //! is, if the angle between the two axes is equal to 0, Pi or -Pi. <br>
    //! Note: the tolerance criterion is given by AngularTolerance. <br>
    bool isParallel(const Ax2d& Other, const double AngularTolerance) const;

    //! Returns the origin of <me>. <br>
    const Pnt2d& location() const;
    void mirror(const Pnt2d& P);

    void mirror(const Ax2d& A);

    //! Performs the symmetrical transformation of an axis <br>
    //! placement with respect to the point P which is the <br>
    //! center of the symmetry. <br>
    Ax2d mirrored(const Pnt2d& P) const;

    //! Performs the symmetrical transformation of an axis <br>
    //! placement with respect to an axis placement which <br>
    //! is the axis of the symmetry. <br>
    Ax2d mirrored(const Ax2d& A) const;

    //! Reverses the direction of <me> and assigns the result to this axis. <br>
    void reverse();

    //! Computes a new axis placement with a direction opposite to <br>
    //! the direction of <me>. <br>
    Ax2d reversed() const;

    void rotate(const Pnt2d& P, const double Ang);

    //! Rotates an axis placement. <P> is the center of the <br>
    //! rotation . Ang is the angular value of the rotation <br>
    //! in radians. <br>
    Ax2d rotated(const Pnt2d& P, const double Ang) const;

    void scale(const Pnt2d& P, const double S);

    //! Applies a scaling transformation on the axis placement. <br>
    //! The "Location" point of the axis placement is modified. <br>
    //! The "Direction" is reversed if the scale is negative. <br>
    Ax2d scaled(const Pnt2d& P, const double S) const;

    //! Changes the direction of <me>. <br>
    void setDirection(const Dir2d& V);
    //! Changes the "Location" point (origin) of <me>. <br>
    void setLocation(const Pnt2d& Locat);
    void transform(const Trsf2d& T);
    //! Transforms an axis placement with a Trsf. <br>
    Ax2d transformed(const Trsf2d& T) const;

    void translate(const Vec2d& V);

    //! Translates an axis placement in the direction of the vector <br>
    //! <V>. The magnitude of the translation is the vector's magnitude. <br>
    Ax2d translated(const Vec2d& V) const;

    void translate(const Pnt2d& P1, const Pnt2d& P2);

    //! Translates an axis placement from the point <P1> to the <br>
    //! point <P2>. <br>
    Ax2d translated(const Pnt2d& P1, const Pnt2d& P2) const;

protected:
private:
    Pnt2d _loc;
    Dir2d _vdir;
};

}  // namespace Geom