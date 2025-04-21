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
#include <vector>
//xdone 

namespace Geom
{
class Mat;
class XYZ;
}  // namespace Geom

typedef std::vector<Geom::XYZ> COORDS;

namespace Geom
{
//!  This class describes a Cartesian coordinate entity in <br>
//!  3D space {X,Y,Z}. This class is non-persistent. This entity is <br>
//!  used for algebraic calculation. This entity can be transformed <br>
//!  with a "Trsf" or a  "GTrsf" from package "gp". <br>
//! It is used in vectorial computations or for holding this type <br>
//! of information in data structures. <br>

class LX_GEOM_EXPORT XYZ
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
    //! creates an indefinite XYZ. <br>
    XYZ();
    //! modification of the XYZ coordinates <br>
    XYZ(const double X, const double Y, const double Z);
    //! For this number triple, assigns <br>
    //!   the values X, Y and Z to its three coordinates <br>
    void setCoord(const double X, const double Y, const double Z);

    //!  modifies the coordinate of range Index <br>
    //!  Index = 1 => X is modified <br>
    //!  Index = 2 => Y is modified <br>
    //!  Index = 3 => Z is modified <br>
    //!  Raises OutOfRange if Index != {1, 2, 3}. <br>
    void setCoord(const int Index, const double Xi);
    //! Assigns the given value to the X coordinate of this number triple. <br>
    void setX(const double X);
    //! Assigns the given value to the  Y coordinate of this number triple. <br>
    void setY(const double Y);
    //! Assigns the given value to ther Z coordinate of this number triple. <br>
    void setZ(const double Z);

    //!  returns the coordinate of range Index : <br>
    //!  Index = 1 => X is returned <br>
    //!  Index = 2 => Y is returned <br>
    //!  Index = 3 => Z is returned <br>
    //! <br>
    //! Raises OutOfRange if Index != {1, 2, 3}. <br>
    double coord(const int Index) const;

    void coord(double& X, double& Y, double& Z) const;
    //! Returns the X, Y, or Z coordinate of this number triple. <br>
    double x() const;
    //! Returns the X, Y, or Z coordinate of this number triple. <br>
    double y() const;
    //! Returns the X, Y, or Z coordinate of this number triple. <br>
    double z() const;
    //! computes Sqrt (X*X + Y*Y + Z*Z) where X, Y and Z are the three coordinates of this number triple. <br>
    double modulus() const;
    //! Computes X*X + Y*Y + Z*Z where X, Y and Z are the three coordinates of this number triple. <br>
    double squareModulus() const;


    //!  Returns True if he coordinates of this number triple are <br>
    //! equal to the respective coordinates of the number triple <br>
    //! Other, within the specified tolerance Tolerance. I.e.: <br>
    //!  abs(<me>.X() - Other.X()) <= Tolerance and <br>
    //!  abs(<me>.Y() - Other.Y()) <= Tolerance and <br>
    //!  abs(<me>.Z() - Other.Z()) <= Tolerance. <br>
    bool isEqual(const XYZ& Other, const double Tolerance) const;

    //! <me>.X() = <me>.X() + Other.X() <br>
    //! <me>.Y() = <me>.Y() + Other.Y() <br>
    //! <me>.Z() = <me>.Z() + Other.Z() <br>
    void add(const XYZ& Other);
    void operator+=(const XYZ& Other) { add(Other); }


    //! new.X() = <me>.X() + Other.X() <br>
    //! new.Y() = <me>.Y() + Other.Y() <br>
    //! new.Z() = <me>.Z() + Other.Z() <br>
    XYZ added(const XYZ& Other) const;
    XYZ operator+(const XYZ& Other) const { return added(Other); }


    //! <me>.X() = <me>.Y() * Other.Z() - <me>.Z() * Other.Y() <br>
    //! <me>.Y() = <me>.Z() * Other.X() - <me>.X() * Other.Z() <br>
    //! <me>.Z() = <me>.X() * Other.Y() - <me>.Y() * Other.X() <br>
    void cross(const XYZ& Right);
    void operator^=(const XYZ& Right) { cross(Right); }


    //! new.X() = <me>.Y() * Other.Z() - <me>.Z() * Other.Y() <br>
    //! new.Y() = <me>.Z() * Other.X() - <me>.X() * Other.Z() <br>
    //! new.Z() = <me>.X() * Other.Y() - <me>.Y() * Other.X() <br>
    XYZ crossed(const XYZ& Right) const;
    XYZ operator^(const XYZ& Right) const { return crossed(Right); }


    //!  Computes the magnitude of the cross product between <me> and <br>
    //!  Right. Returns || <me> ^ Right || <br>
    double crossMagnitude(const XYZ& Right) const;

    //!  Computes the square magnitude of the cross product between <me> and <br>
    //!  Right. Returns || <me> ^ Right ||**2 <br>
    double crossSquareMagnitude(const XYZ& Right) const;
    //! Triple vector product <br>
    //!  Computes <me> = <me>.Cross(Coord1.Cross(Coord2)) <br>
    void crossCross(const XYZ& Coord1, const XYZ& Coord2);
    //! Triple vector product <br>
    //!  computes New = <me>.Cross(Coord1.Cross(Coord2)) <br>
    XYZ crossCrossed(const XYZ& Coord1, const XYZ& Coord2) const;
    //! divides <me> by a real. <br>
    void divide(const double Scalar);
    void operator/=(const double Scalar) { divide(Scalar); }

    //! divides <me> by a real. <br>
    XYZ divided(const double Scalar) const;
    XYZ operator/(const double Scalar) const { return divided(Scalar); }

    //! computes the scalar product between <me> and Other <br>
    double dot(const XYZ& Other) const;
    double operator*(const XYZ& Other) const { return dot(Other); }

    //! computes the triple scalar product. <br>
    double dotCross(const XYZ& Coord1, const XYZ& Coord2) const;

    //!  <me>.X() = <me>.X() * Scalar; <br>
    //!  <me>.Y() = <me>.Y() * Scalar; <br>
    //!  <me>.Z() = <me>.Z() * Scalar; <br>
    void multiply(const double Scalar);
    void operator*=(const double Scalar) { multiply(Scalar); }


    //!  <me>.X() = <me>.X() * Other.X(); <br>
    //!  <me>.Y() = <me>.Y() * Other.Y(); <br>
    //!  <me>.Z() = <me>.Z() * Other.Z(); <br>
    void multiply(const XYZ& Other);
    void operator*=(const XYZ& Other) { multiply(Other); }

    void multiply(const Geom::Mat& Matrix);
    void operator*=(const Geom::Mat& Matrix) { multiply(Matrix); }

    // HPK TODO
    //! <me> = Matrix * <me> <br>
    /*void multiply(const Geom::Mat& Matrix) ;
    void operator *=(const Geom::Mat& Matrix)
    {
    multiply(Matrix);
    }
    */


    //!  New.X() = <me>.X() * Scalar; <br>
    //!  New.Y() = <me>.Y() * Scalar; <br>
    //!  New.Z() = <me>.Z() * Scalar; <br>
    XYZ multiplied(const double Scalar) const;
    XYZ operator*(const double Scalar) const { return multiplied(Scalar); }



    //!  new.X() = <me>.X() * Other.X(); <br>
    //!  new.Y() = <me>.Y() * Other.Y(); <br>
    //!  new.Z() = <me>.Z() * Other.Z(); <br>
    XYZ multiplied(const XYZ& Other) const;
    //!  New = Matrix * <me> <br>

    XYZ multiplied(const Geom::Mat& Matrix) const;
    XYZ operator*(const Geom::Mat& Matrix) const { return multiplied(Matrix); }


    //!  <me>.X() = <me>.X()/ <me>.Modulus() <br>
    //!  <me>.Y() = <me>.Y()/ <me>.Modulus() <br>
    //!  <me>.Z() = <me>.Z()/ <me>.Modulus() <br>//! Raised if <me>.Modulus() <= Resolution from gp <br>
    void normalize();

    //!  New.X() = <me>.X()/ <me>.Modulus() <br>
    //!  New.Y() = <me>.Y()/ <me>.Modulus() <br>
    //!  New.Z() = <me>.Z()/ <me>.Modulus() <br>//! Raised if <me>.Modulus() <= Resolution from gp <br>
    XYZ normalized() const;

    //!  <me>.X() = -<me>.X() <br>
    //!  <me>.Y() = -<me>.Y() <br>
    //!  <me>.Z() = -<me>.Z() <br>
    void reverse();

    //!  New.X() = -<me>.X() <br>
    //!  New.Y() = -<me>.Y() <br>
    //!  New.Z() = -<me>.Z() <br>
    XYZ reversed() const;

    //!  <me>.X() = <me>.X() - Other.X() <br>
    //!  <me>.Y() = <me>.Y() - Other.Y() <br>
    //!  <me>.Z() = <me>.Z() - Other.Z() <br>
    void subtract(const XYZ& Right);
    void operator-=(const XYZ& Right) { subtract(Right); }


    //!  new.X() = <me>.X() - Other.X() <br>
    //!  new.Y() = <me>.Y() - Other.Y() <br>
    //!  new.Z() = <me>.Z() - Other.Z() <br>
    XYZ subtracted(const XYZ& Right) const;
    XYZ operator-(const XYZ& Right) const { return subtracted(Right); }


    //!  <me> is setted to the following linear form : <br>
    //!  A1 * XYZ1 + A2 * XYZ2 + A3 * XYZ3 + XYZ4 <br>
    void setLinearForm(const double A1, const XYZ& XYZ1, const double A2, const XYZ& XYZ2, const double A3, const XYZ& XYZ3, const XYZ& XYZ4);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * XYZ1 + A2 * XYZ2 + A3 * XYZ3 <br>
    void setLinearForm(const double A1, const XYZ& XYZ1, const double A2, const XYZ& XYZ2, const double A3, const XYZ& XYZ3);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * XYZ1 + A2 * XYZ2 + XYZ3 <br>
    void setLinearForm(const double A1, const XYZ& XYZ1, const double A2, const XYZ& XYZ2, const XYZ& XYZ3);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * XYZ1 + A2 * XYZ2 <br>
    void setLinearForm(const double A1, const XYZ& XYZ1, const double A2, const XYZ& XYZ2);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * XYZ1 + XYZ2 <br>
    void setLinearForm(const double A1, const XYZ& XYZ1, const XYZ& XYZ2);

    void setLinearForm(const XYZ& Left, const XYZ& Right);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    double& operator[](int i);
    const double& operator[](int i) const;

    bool operator<(const XYZ& rhs) const;


private:
    double _x;
    double _y;
    double _z;
};


typedef std::vector<XYZ> XYZ_Array;
}  // namespace Geom

inline Geom::XYZ operator*(const Geom::Mat& Matrix, const Geom::XYZ& Coord1)
{
    return Coord1.multiplied(Matrix);
}

inline Geom::XYZ operator*(const double Scalar, const Geom::XYZ& Coord1)
{
    return Coord1.multiplied(Scalar);
}
