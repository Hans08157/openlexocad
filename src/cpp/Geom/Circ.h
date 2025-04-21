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

#include <Geom/Ax2.h>


namespace Geom
{
//!  Describes a circle in 3D space. <br>
//! A circle is defined by its radius and positioned in space <br>
//! with a coordinate system (a Geom::Ax2 object) as follows: <br>
//! -   the origin of the coordinate system is the center of the circle, and <br>
//! -   the origin, "X Direction" and "Y Direction" of the <br>
//!   coordinate system define the plane of the circle. <br>
//! This positioning coordinate system is the "local <br>
//! coordinate system" of the circle. Its "main Direction" <br>
//! gives the normal vector to the plane of the circle. The <br>
//! "main Axis" of the coordinate system is referred to as <br>
//! the "Axis" of the circle. <br>
//! Note: when a Geom::Circ circle is converted into a <br>
//! Geom_Circle circle, some implicit properties of the <br>
//! circle are used explicitly: <br>
//! -   the "main Direction" of the local coordinate system <br>
//!   gives an implicit orientation to the circle (and defines <br>
//!   its trigonometric sense), <br>
//! -   this orientation corresponds to the direction in <br>
//!   which parameter values increase, <br>
//! -   the starting point for parameterization is that of the <br>
//! "X Axis" of the local coordinate system (i.e. the "X Axis" of the circle). <br>
//! See Also <br>
//! gce_MakeCirc which provides functions for more complex circle constructions <br>
//! Geom_Circle which provides additional functions for <br>
//! constructing circles and works, in particular, with the <br>
//! parametric equations of circles <br>
class LX_GEOM_EXPORT Circ
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    //! Creates an indefinite circle. <br>
    Circ();

    //!  A2 locates the circle and gives its orientation in 3D space. <br>
    //! Warnings : <br>
    //!  It is not forbidden to create a circle with Radius = 0.0  Raises ConstructionError if Radius < 0.0 <br>
    Circ(const Geom::Ax2& A2, const double Radius);

    //!  Changes the main axis of the circle. It is the axis <br>
    //!  perpendicular to the plane of the circle. <br>
    //! Raises ConstructionError if the direction of A1 <br>
    //! is parallel to the "XAxis" of the circle. <br>
    void setAxis(const Geom::Ax1& A1);

    //!  Changes the "Location" point (center) of the circle. <br>
    void setLocation(const Geom::Pnt& P);
    //! Changes the position of the circle. <br>
    void setPosition(const Geom::Ax2& A2);
    //! Modifies the radius of this circle. <br>
    //! Warning. This class does not prevent the creation of a circle where Radius is null. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if Radius is negative. <br>
    void setRadius(const double Radius);
    //! Computes the area of the circle. <br>
    double area() const;

    //!  Returns the main axis of the circle. <br>
    //!  It is the axis perpendicular to the plane of the circle, <br>
    //!  passing through the "Location" point (center) of the circle. <br>
    const Geom::Ax1& axis() const;
    //!  Computes the circumference of the circle. <br>
    double length() const;

    //!  Returns the center of the circle. It is the <br>
    //!  "Location" point of the local coordinate system <br>
    //!  of the circle <br>
    const Geom::Pnt& location() const;

    //!  Returns the position of the circle. <br>
    //!  It is the local coordinate system of the circle. <br>
    const Geom::Ax2& position() const;
    //!  Returns the radius of this circle. <br>
    double radius() const;

    //!  Returns the "XAxis" of the circle. <br>
    //!  This axis is perpendicular to the axis of the conic. <br>
    //!  This axis and the "Yaxis" define the plane of the conic. <br>
    Geom::Ax1 xAxis() const;

    //!  Returns the "YAxis" of the circle. <br>
    //!  This axis and the "Xaxis" define the plane of the conic. <br>
    //!  The "YAxis" is perpendicular to the "Xaxis". <br>
    Geom::Ax1 yAxis() const;

    //!  Computes the minimum of distance between the point P and <br>
    //!  any point on the circumference of the circle. <br>
    double distance(const Geom::Pnt& P) const;

    //!  Computes the square distance between <me> and the point P. <br>
    double squareDistance(const Geom::Pnt& P) const;

    //!  Returns True if the point P is on the circumference. <br>
    //!  The distance between <me> and <P> must be lower or <br>
    //!  equal to LinearTolerance. <br>
    bool contains(const Geom::Pnt& P, const double LinearTolerance) const;

    void mirror(const Geom::Pnt& P);

    //!  Performs the symmetrical transformation of a circle <br>
    //!  with respect to the point P which is the center of the <br>
    //!  symmetry. <br>
    Geom::Circ mirrored(const Geom::Pnt& P) const;

    void mirror(const Geom::Ax1& A1);

    //!  Performs the symmetrical transformation of a circle with <br>
    //!  respect to an axis placement which is the axis of the <br>
    //!  symmetry. <br>
    Geom::Circ mirrored(const Geom::Ax1& A1) const;

    void mirror(const Geom::Ax2& A2);

    //!  Performs the symmetrical transformation of a circle with respect <br>
    //!  to a plane. The axis placement A2 locates the plane of the <br>
    //!  of the symmetry : (Location, XDirection, YDirection). <br>
    Geom::Circ mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  Rotates a circle. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Geom::Circ rotated(const Geom::Ax1& A1, const double Ang) const;

    void scale(const Geom::Pnt& P, const double S);

    //!  Scales a circle. S is the scaling value. <br>
    //!  Warnings : <br>
    //!  If S is negative the radius stay positive but <br>
    //!  the "XAxis" and the "YAxis" are  reversed as for <br>
    //!  an ellipse. <br>
    Geom::Circ scaled(const Geom::Pnt& P, const double S) const;

    void transform(const Geom::Trsf& T);

    //!  Transforms a circle with the transformation T from class Trsf. <br>
    Geom::Circ transformed(const Geom::Trsf& T) const;

    void translate(const Geom::Vec& V);

    //!  Translates a circle in the direction of the vector V. <br>
    //!  The magnitude of the translation is the vector's magnitude. <br>
    Geom::Circ translated(const Geom::Vec& V) const;

    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //!  Translates a circle from the point P1 to the point P2. <br>
    Geom::Circ translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

private:
    Geom::Ax2 _pos;
    double _radius;
};

}  // namespace Geom
