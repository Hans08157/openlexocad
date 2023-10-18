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
class Trsf;

//! Describes a line in 3D space. <br>
//! A line is positioned in space with an axis (a Geom::Ax1 <br>
//! object) which gives it an origin and a unit vector. <br>
//! A line and an axis are similar objects, thus, we can <br>
//! convert one into the other. A line provides direct access <br>
//! to the majority of the edit and query functions available <br>
//! on its positioning axis. In addition, however, a line has <br>
//! specific functions for computing distances and positions. <br>
//! See Also <br>
//! gce_MakeLin which provides functions for more complex <br>
//! line constructions <br>
//! Geom_Line which provides additional functions for <br>
//! constructing lines and works, in particular, with the <br>
//! parametric equations of lines <br>
class LX_GEOM_EXPORT Lin
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
    //! Creates an indefinite Line. <br>
    Lin();
    //! Creates a line defined by axis A1. <br>
    Lin(const Geom::Ax1& A1);

    //! Creates a line passing through point P and parallel to <br>
    //!  vector V (P and V are, respectively, the origin and <br>
    //! the unit vector of the positioning axis of the line). <br>
    Lin(const Geom::Pnt& P, const Geom::Dir& V);

    void reverse();
    //! Reverses the direction of the line. <br>
    //! Note: <br>
    //! -   Reverse assigns the result to this line, while <br>
    //! -   Reversed creates a new one. <br>
    Lin reversed() const;
    //!  Changes the direction of the line. <br>
    void setDirection(const Geom::Dir& V);
    //! Changes the location point (origin) of the line. <br>
    void setLocation(const Geom::Pnt& P);

    //!  Complete redefinition of the line. <br>
    //!  The "Location" point of <A1> is the origin of the line. <br>
    //!  The "Direction" of <A1> is  the direction of the line. <br>
    void setPosition(const Geom::Ax1& A1);
    //! Returns the direction of the line. <br>
    const Geom::Dir& direction() const;

    //!  Returns the location point (origin) of the line. <br>
    const Geom::Pnt& location() const;

    //!  Returns the axis placement one axis whith the same <br>
    //!  location and direction as <me>. <br>
    const Geom::Ax1& position() const;
    //! Computes the angle between two lines in radians. <br>
    double angle(const Lin& Other) const;
    //! Returns true if this line contains the point P, that is, if the <br>
    //! distance between point P and this line is less than or <br>
    //! equal to LinearTolerance.. <br>
    bool contains(const Geom::Pnt& P, const double LinearTolerance) const;
    //! Computes the distance between <me> and the point P. <br>
    double distance(const Geom::Pnt& P) const;

    //! Computes the distance between two lines. <br>
    double distance(const Lin& Other) const;

    //!  Computes the square distance between <me> and the point P. <br>
    double squareDistance(const Geom::Pnt& P) const;
    //! Computes the square distance between two lines. <br>
    double squareDistance(const Lin& Other) const;

    //!  Computes the line normal to the direction of <me>, passing <br>
    //!  through the point P.  Raises ConstructionError <br>
    //!  if the distance between <me> and the point P is lower <br>
    //!  or equal to Resolution from gp because there is an infinity of <br>
    //!  solutions in 3D space. <br>
    Lin normal(const Geom::Pnt& P) const;


    void mirror(const Geom::Pnt& P);


    //!  Performs the symmetrical transformation of a line <br>
    //!  with respect to the point P which is the center of <br>
    //!  the symmetry. <br>
    Lin mirrored(const Geom::Pnt& P) const;


    void mirror(const Geom::Ax1& A1);


    //!  Performs the symmetrical transformation of a line <br>
    //!  with respect to an axis placement which is the axis <br>
    //!  of the symmetry. <br>
    Lin mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);


    //!  Performs the symmetrical transformation of a line <br>
    //!  with respect to a plane. The axis placement  <A2> <br>
    //!  locates the plane of the symmetry : <br>
    //!  (Location, XDirection, YDirection). <br>
    Lin mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  Rotates a line. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Lin rotated(const Geom::Ax1& A1, const double Ang) const;

    void scale(const Geom::Pnt& P, const double S);

    //!  Scales a line. S is the scaling value. <br>
    //!  The "Location" point (origin) of the line is modified. <br>
    //!  The "Direction" is reversed if the scale is negative. <br>
    Lin scaled(const Geom::Pnt& P, const double S) const;

    void transform(const Geom::Trsf& T);

    //!  Transforms a line with the transformation T from class Trsf. <br>
    Lin transformed(const Geom::Trsf& T) const;

    void translate(const Geom::Vec& V);

    //!  Translates a line in the direction of the vector V. <br>
    //!  The magnitude of the translation is the vector's magnitude. <br>
    Lin translated(const Geom::Vec& V) const;

    void translate(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //!  Translates a line from the point P1 to the point P2. <br>
    Lin translated(const Geom::Pnt& P1, const Geom::Pnt& P2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

private:
    Geom::Ax1 pos;
};

}  // namespace Geom
