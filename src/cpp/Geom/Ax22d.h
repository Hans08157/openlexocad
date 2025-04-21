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

namespace Geom
{
class Ax2d;
class Trsf2d;
class Vec2d;

//! Describes a coordinate system in a plane (2D space). <br>
//! A coordinate system is defined by: <br>
//! - its origin (also referred to as its "location point"), and <br>
//! - two orthogonal unit vectors, respectively, called the "X <br>
//! Direction" and the "Y Direction". <br>
//! A Ax22d may be right-handed ("direct sense") or <br>
//! left-handed ("inverse" or "indirect sense"). <br>
//! You use a Ax22d to: <br>
//! - describe 2D geometric entities, in particular to position <br>
//! them. The local coordinate system of a geometric <br>
//! entity serves for the same purpose as the STEP <br>
//! function "axis placement two axes", or <br>
//! - define geometric transformations. <br>
//! Note: we refer to the "X Axis" and "Y Axis" as the axes having: <br>
//! - the origin of the coordinate system as their origin, and <br>
//! - the unit vectors "X Direction" and "Y Direction", <br>
//! respectively, as their unit vectors. <br>
class LX_GEOM_EXPORT Ax22d
{
public:
    //! Creates an indefinite coordinate system. <br>
    Ax22d();

    //! Creates a coordinate system with origin P and where: <br>
    //! - Vx is the "X Direction", and <br>
    //! - the "Y Direction" is orthogonal to Vx and <br>
    //! oriented so that the cross products Vx^"Y <br>
    //! Direction" and Vx^Vy have the same sign. <br>
    //! Raises ConstructionError if Vx and Vy are parallel (same or opposite orientation). <br>
    Ax22d(const Pnt2d& P, const Dir2d& Vx, const Dir2d& Vy);

    //! Creates - a coordinate system with origin P and "X Direction" <br>
    //! V, which is: <br>
    //! - right-handed if Sense is true (default value), or <br>
    //! - left-handed if Sense is false <br>
    Ax22d(const Pnt2d& P, const Dir2d& V, const bool Sense = true);

    //! Creates - a coordinate system where its origin is the origin of <br>
    //! A and its "X Direction" is the unit vector of A, which is: <br>
    //! - right-handed if Sense is true (default value), or <br>
    //! - left-handed if Sense is false. <br>
    Ax22d(const Ax2d& A, const bool Sense = true);

    //! Returns the "location" point (origin) of <me>. <br>
    const Pnt2d& location() const;

    void mirror(const Pnt2d& P);

    void mirror(const Ax2d& A);

    //! Performs the symmetrical transformation of an axis <br>
    //! placement with respect to the point P which is the <br>
    //! center of the symmetry. <br>
    //! Warnings : <br>
    //! The main direction of the axis placement is not changed. <br>
    //! The "xDirection" and the "yDirection" are reversed. <br>
    //! So the axis placement stay right handed. <br>
    Ax22d mirrored(const Pnt2d& P) const;

    //! Performs the symmetrical transformation of an axis <br>
    //! placement with respect to an axis placement which <br>
    //! is the axis of the symmetry. <br>
    //! The transformation is performed on the "location" <br>
    //! point, on the "xDirection" and "yDirection". <br>
    //! The resulting main "Direction" is the cross product between <br>
    //! the "xDirection" and the "yDirection" after transformation. <br>
    Ax22d mirrored(const Ax2d& A) const;

    void rotate(const Pnt2d& P, const double Ang);

    //! Rotates an axis placement. <A1> is the axis of the <br>
    //! rotation . Ang is the angular value of the rotation <br>
    //! in radians. <br>
    Ax22d rotated(const Pnt2d& P, const double Ang) const;

    void scale(const Pnt2d& P, const double S);

    //! Applies a scaling transformation on the axis placement. <br>
    //! The "location" point of the axisplacement is modified. <br>
    //! Warnings : <br>
    //! If the scale <S> is negative : <br>
    //! . the main direction of the axis placement is not changed. <br>
    //! . The "xDirection" and the "yDirection" are reversed. <br>
    //! So the axis placement stay right handed. <br>
    Ax22d scaled(const Pnt2d& P, const double S) const;

    //! Assigns the origin and the two unit vectors of the <br>
    //! coordinate system A1 to this coordinate system. <br>
    void setAxis(const Ax22d& A1);

    //! Changes the "location" point (origin) of <me>. <br>
    void setLocation(const Pnt2d& P);

    //! Changes the xAxis and yAxis ("location" point and "Direction") <br>
    //! of <me>. <br>
    //! The "yDirection" is recomputed in the same sense as before. <br>
    void setXAxis(const Ax2d& A1);
    //! Assigns Vx to the "X Direction" of <br>
    //! this coordinate system. The other unit vector of this <br>
    //! coordinate system is recomputed, normal to Vx , <br>
    //! without modifying the orientation (right-handed or <br>
    //! left-handed) of this coordinate system. <br>
    void setXDirection(const Dir2d& Vx);
    //! Changes the xAxis and yAxis ("location" point and "Direction") of <me>. <br>
    //! The "xDirection" is recomputed in the same sense as before. <br>
    void setYAxis(const Ax2d& A1);

    //! Assignsr Vy to the "Y Direction" of <br>
    //! this coordinate system. The other unit vector of this <br>
    //! coordinate system is recomputed, normal to Vy, <br>
    //! without modifying the orientation (right-handed or <br>
    //! left-handed) of this coordinate system. <br>
    void setYDirection(const Dir2d& Vy);
    void transform(const Trsf2d& T);

    //! Transforms an axis placement with a Trsf. <br>
    //! The "location" point, the "xDirection" and the <br>
    //! "yDirection" are transformed with T. The resulting <br>
    //! main "Direction" of <me> is the cross product between <br>
    //! the "xDirection" and the "yDirection" after transformation. <br>
    Ax22d transformed(const Trsf2d& T) const;

    void translate(const Vec2d& V);

    void translate(const Pnt2d& P1, const Pnt2d& P2);

    //! Translates an axis plaxement in the direction of the vector <br>
    //! <V>. The magnitude of the translation is the vector's magnitude. <br>
    Ax22d translated(const Vec2d& V) const;

    //! Translates an axis placement from the point <P1> to the <br>
    //! point <P2>. <br>
    Ax22d translated(const Pnt2d& P1, const Pnt2d& P2) const;
    //! Returns an axis, for which <br>
    //! - the origin is that of this coordinate system, and <br>
    //! - the unit vector is either the "X Direction" of this coordinate system. <br>
    //! Note: the result is the "X Axis" of this coordinate system. <br>
    Ax2d xAxis() const;
    //! Returns the "xDirection" of <me>. <br>
    const Dir2d& xDirection() const;

    //! Returns an axis, for which <br>
    //! - the origin is that of this coordinate system, and <br>
    //! - the unit vector is either the "Y Direction" of this coordinate system. <br>
    //! Note: the result is the "Y Axis" of this coordinate system. <br>
    Ax2d yAxis() const;

    //! Returns the "yDirection" of <me>. <br>
    const Dir2d& yDirection() const;

    const Pnt2d& _CSFDB_GetAx22dpoint() const { return point; }
    const Dir2d& _CSFDB_GetAx22dvydir() const { return vydir; }
    const Dir2d& _CSFDB_GetAx22dvxdir() const { return vxdir; }

    bool operator==(const Ax22d& other) const;

private:
    Pnt2d point;
    Dir2d vydir;
    Dir2d vxdir;
};

}  // namespace Geom