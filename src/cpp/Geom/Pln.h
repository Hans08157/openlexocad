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

#include <Geom/Ax3.h>

namespace Geom
{
class Lin;

//! Describes a plane. <br>
//! A plane is positioned in space with a coordinate system <br>
//! (a Geom::Ax3 object), such that the plane is defined by the <br>
//! origin, "X Direction" and "Y Direction" of this coordinate <br>
//! system, which is the "local coordinate system" of the <br>
//! plane. The "main Direction" of the coordinate system is a <br>
//! vector normal to the plane. It gives the plane an implicit <br>
//! orientation such that the plane is said to be "direct", if the <br>
//! coordinate system is right-handed, or "indirect" in the other case. <br>
//! Note: when a Pln plane is converted into a <br>
//! Geom_Plane plane, some implicit properties of its local <br>
//! coordinate system are used explicitly: <br>
//! -   its origin defines the origin of the two parameters of <br>
//!   the planar surface, <br>
//! -   its implicit orientation is also that of the Geom_Plane. <br>
//! See Also <br>
//! gce_MakePln which provides functions for more complex <br>
//! plane constructions <br>
//! Geom_Plane which provides additional functions for <br>
//! constructing planes and works, in particular, with the <br>
//! parametric equations of planes <br>
class LX_GEOM_EXPORT Pln
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
    //! Creates an indefinite plane. <br>
    Pln();

    //!  The coordinate system of the plane is defined with the axis <br>
    //!  placement A3. <br>
    //!  The "Direction" of A3 defines the normal to the plane. <br>
    //!  The "Location" of A3 defines the location (origin) of the plane. <br>
    //!  The "XDirection" and "YDirection" of A3 define the "XAxis" and <br>
    //!  the "YAxis" of the plane used to parametrize the plane. <br>
    Pln(const Geom::Ax3& A3);


    //!  Creates a plane with the  "Location" point <P> <br>
    //!  and the normal direction <V>. <br>
    Pln(const Geom::Pnt& P, const Geom::Dir& V);


    //!  Creates a plane from its cartesian equation : <br>
    //!  A * X + B * Y + C * Z + D = 0.0 <br>
    //!  Raises ConstructionError if Sqrt (A*A + B*B + C*C) <= Resolution from gp. <br>
    Pln(const double A, const double B, const double C, const double D);

    //!  Returns the coefficients of the plane's cartesian equation : <br>
    //!  A * X + B * Y + C * Z + D = 0. <br>
    void coefficients(double& A, double& B, double& C, double& D) const;
    //! Modifies this plane, by redefining its local coordinate system so that <br>
    //! -   its origin and "main Direction" become those of the <br>
    //!   axis A1 (the "X Direction" and "Y Direction" are then recomputed). <br>
    //!  Raises ConstructionError if the A1 is parallel to the "XAxis" of the plane. <br>
    void setAxis(const Geom::Ax1& A1);
    //! Changes the origin of the plane. <br>
    void setLocation(const Geom::Pnt& Loc);
    //! Changes the local coordinate system of the plane. <br>
    void setPosition(const Geom::Ax3& A3);
    //! Reverses the   U   parametrization of   the  plane <br>
    //!          reversing the XAxis. <br>
    void uReverse();
    //! Reverses the   V   parametrization of   the  plane <br>
    //!          reversing the YAxis. <br>
    void vReverse();
    //! returns true if the Ax3 is right handed. <br>
    bool direct() const;
    //! Returns the plane's normal Axis. <br>
    const Geom::Ax1& axis() const;
    //! Returns the plane's location (origin). <br>
    const Geom::Pnt& location() const;
    //! Returns the local coordinate system of the plane . <br>
    const Geom::Ax3& position() const;
    //! Computes the distance between <me> and the point <P>. <br>
    double distance(const Geom::Pnt& P) const;
    //! Computes the signed distance between <me> and the point <P>. <br>
    double signeddistance(const Geom::Pnt& P) const;
    //! Computes the distance between <me> and the line <L>. <br>
    double distance(const Geom::Lin& L) const;
    //! Computes the distance between two planes. <br>
    double distance(const Pln& Other) const;

    //!  Computes the square distance between <me> and the point <P>. <br>
    double squareDistance(const Geom::Pnt& P) const;

    //!  Computes the square distance between <me> and the line <L>. <br>
    double squareDistance(const Geom::Lin& L) const;

    //!  Computes the square distance between two planes. <br>
    double squareDistance(const Pln& Other) const;
    //! Returns the X axis of the plane. <br>
    Geom::Ax1 xAxis() const;
    //! Returns the Y axis  of the plane. <br>
    Geom::Ax1 yAxis() const;
    //! Returns true if this plane contains the point P. This means that <br>
    //! -   the distance between point P and this plane is less <br>
    //!   than or equal to LinearTolerance, or <br>
    //! -   line L is normal to the "main Axis" of the local <br>
    //!   coordinate system of this plane, within the tolerance <br>
    //!   AngularTolerance, and the distance between the origin <br>
    //!   of line L and this plane is less than or equal to <br>
    //!   LinearTolerance. <br>
    bool contains(const Geom::Pnt& P, const double LinearTolerance) const;
    //! Returns true if this plane contains the line L. This means that <br>
    //! -   the distance between point P and this plane is less <br>
    //!   than or equal to LinearTolerance, or <br>
    //! -   line L is normal to the "main Axis" of the local <br>
    //!   coordinate system of this plane, within the tolerance <br>
    //!   AngularTolerance, and the distance between the origin <br>
    //!   of line L and this plane is less than or equal to <br>
    //!   LinearTolerance. <br>
    bool contains(const Geom::Lin& L, const double LinearTolerance, const double AngularTolerance) const;


    void mirror(const Geom::Pnt& P);


    //!  Performs the symmetrical transformation of a plane with respect <br>
    //!  to the point <P> which is the center of the symmetry <br>
    //! Warnings : <br>
    //!  The normal direction to the plane is not changed. <br>
    //!  The "XAxis" and the "YAxis" are reversed. <br>
    Pln mirrored(const Geom::Pnt& P) const;


    void mirror(const Geom::Ax1& A1);

    //! Performs   the symmetrical transformation  of a <br>
    //!  plane with respect to an axis placement  which is the axis <br>
    //!  of  the symmetry.  The  transformation is performed on the <br>
    //!  "Location" point, on  the "XAxis"  and the "YAxis".    The <br>
    //!  resulting normal  direction  is  the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation <br>
    //!  if  the  initial plane was right  handed,  else  it is the <br>
    //!  opposite. <br>
    Pln mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);

    //!  Performs the  symmetrical transformation  of  a <br>
    //!  plane    with respect to    an axis  placement.   The axis <br>
    //!  placement  <A2> locates the plane  of  the symmetry.   The <br>
    //!  transformation is performed  on  the  "Location" point, on <br>
    //!  the  "XAxis" and  the    "YAxis".  The resulting    normal <br>
    //!  direction is the cross  product between   the "XDirection" <br>
    //!  and the "YDirection"  after  transformation if the initial <br>
    //!  plane was right handed, else it is the opposite. <br>
    Pln mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  rotates a plane. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Pln rotated(const Geom::Ax1& A1, const double Ang) const;

    void scale(const Geom::Pnt& P, const double S);

    //!  Scales a plane. S is the scaling value. <br>
    Pln scaled(const Geom::Pnt& P, const double S) const;

    void transform(const Geom::Trsf& T);

    //!  Transforms a plane with the transformation T from class Trsf. <br>
    //!  The transformation is performed on the "Location" <br>
    //!  point, on the "XAxis" and the "YAxis". <br>
    //!  The resulting normal direction is the cross product between <br>
    //!  the "XDirection" and the "YDirection" after transformation. <br>
    Pln transformed(const Geom::Trsf& T) const;

    void translate(const Geom::Vec& V);

    //!  Translates a plane in the direction of the vector V. <br>
    //!  The magnitude of the translation is the vector's magnitude. <br>
    Pln translated(const Geom::Vec& V) const;

    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //!  Translates a plane from the point P1 to the point P2. <br>
    Pln translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


private:
    Geom::Ax3 pos;
};

}  // namespace Geom
