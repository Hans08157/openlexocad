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
namespace Geom
{
class Mat2d;

//!  This class describes a cartesian coordinate entity in 2D <br>
//!  space {X,Y}. This class is non persistent. This entity used <br>
//!  for algebraic calculation. An XY can be transformed with a <br>
//!  Trsf2d or a  GTrsf2d from package gp. <br>
//! It is used in vectorial computations or for holding this type <br>
//! of information in data structures. <br>
class LX_GEOM_EXPORT XY
{
public:
    //! Creates an indefinite XY number pair. <br>
    XY();
    //! a number pair defined by the XY coordinates <br>
    XY(const double X, const double Y);

    //! Computes the sum of this number pair and number pair Other <br>
    //! <me>.x() = <me>.x() + Other.x() <br>
    //! <me>.y() = <me>.y() + Other.y() <br>
    void add(const XY& Other);
    //! Computes the sum of this number pair and number pair Other <br>
    //! new.x() = <me>.x() + Other.x() <br>
    //! new.y() = <me>.y() + Other.y() <br>
    XY added(const XY& Other) const;
    //!  returns the coordinate of range Index : <br>
    //!  Index = 1 => X is returned <br>
    //!  Index = 2 => Y is returned <br>
    //! Raises OutOfRange if Index != {1, 2}. <br>
    double coord(const int Index) const;
    //! For this number pair, returns its coordinates X and Y. <br>
    void coord(double& X, double& Y) const;
    //!  Real D = <me>.x() * Other.y() - <me>.y() * Other.x() <br>
    double crossed(const XY& Right) const;
    //!  computes the magnitude of the cross product between <me> and <br>
    //!  Right. Returns || <me> ^ Right || <br>
    double crossMagnitude(const XY& Right) const;

    //!  computes the square magnitude of the cross product between <me> and <br>
    //!  Right. Returns || <me> ^ Right ||**2 <br>
    double crossSquareMagnitude(const XY& Right) const;
    //! divides <me> by a real. <br>
    void divide(const double Scalar);
    //! Divides <me> by a real. <br>
    XY divided(const double Scalar) const;
    //! Computes the scalar product between <me> and Other <br>
    double dot(const XY& Other) const;
    //!  Returns true if the coordinates of this number pair are <br>
    //! equal to the respective coordinates of the number pair <br>
    //! Other, within the specified tolerance Tolerance. I.e.: <br>
    //!  abs(<me>.x() - Other.x()) <= Tolerance and <br>
    //!  abs(<me>.y() - Other.y()) <= Tolerance and <br>//! computations <br>
    bool isEqual(const XY& Other, const double Tolerance) const;
    //! Computes Sqrt (x*x + y*y) where x and y are the two coordinates of this number pair. <br>
    double modulus() const;
    //!  New.x() = <me>.x() * Scalar; <br>
    //!  New.y() = <me>.y() * Scalar; <br>
    XY multiplied(const double Scalar) const;
    //!  new.x() = <me>.x() * Other.x(); <br>
    //!  new.y() = <me>.y() * Other.y(); <br>
    XY multiplied(const XY& Other) const;
    //!  New = Matrix * <me> <br>
    XY multiplied(const Mat2d& Matrix) const;
    //!  <me>.x() = <me>.x() * Scalar; <br>
    //!  <me>.y() = <me>.y() * Scalar; <br>
    void multiply(const double Scalar);
    //!  <me>.x() = <me>.x() * Other.x(); <br>
    //!  <me>.y() = <me>.y() * Other.y(); <br>
    void multiply(const XY& Other);
    //! <me> = Matrix * <me> <br>
    void multiply(const Mat2d& Matrix);
    //!  <me>.x() = <me>.x()/ <me>.Modulus() <br>
    //!  <me>.y() = <me>.y()/ <me>.Modulus() <br>
    //! Raises ConstructionError if <me>.Modulus() <= Resolution from gp <br>
    void normalize();

    //!  New.x() = <me>.x()/ <me>.Modulus() <br>
    //!  New.y() = <me>.y()/ <me>.Modulus() <br>
    //! Raises ConstructionError if <me>.Modulus() <= Resolution from gp <br>
    XY normalized() const;

    void operator+=(const XY& Other) { add(Other); }
    XY operator+(const XY& Other) const { return added(Other); }

    XY operator-() const { return reversed(); }

    void operator-=(const XY& Right) { subtract(Right); }

    XY operator-(const XY& Right) const { return subtracted(Right); }

    XY operator*(const Mat2d& Matrix) const { return multiplied(Matrix); }

    double operator*(const XY& Other) const { return dot(Other); }

    void operator*=(const double Scalar) { multiply(Scalar); }

    void operator*=(const XY& Other) { multiply(Other); }
    void operator*=(const Mat2d& Matrix) { multiply(Matrix); }

    XY operator*(const double Scalar) const { return multiplied(Scalar); }

    void operator/=(const double Scalar) { divide(Scalar); }
    XY operator/(const double Scalar) const { return divided(Scalar); }
    double operator^(const XY& Right) const { return crossed(Right); }

    //!  <me>.x() = -<me>.x() <br>
    //!  <me>.y() = -<me>.y() <br>
    void reverse();

    //!  New.x() = -<me>.x() <br>
    //!  New.y() = -<me>.y() <br>
    XY reversed() const;
    //!  modifies the coordinate of range Index <br>
    //!  Index = 1 => X is modified <br>
    //!  Index = 2 => Y is modified <br>
    //!   Raises OutOfRange if Index != {1, 2}. <br>
    void setCoord(const int Index, const double Xi);
    //!  For this number pair, assigns <br>
    //!   the values X and Y to its coordinates <br>
    void setCoord(const double X, const double Y);
    //!  Computes  the following linear combination and <br>
    //! assigns the result to this number pair: <br>
    //!  A1 * XY1 + A2 * XY2 <br>
    void setLinearForm(const double A1, const XY& XY1, const double A2, const XY& XY2);

    //!  --  Computes  the following linear combination and <br>
    //! assigns the result to this number pair: <br>
    //!  A1 * XY1 + A2 * XY2 + XY3 <br>
    void setLinearForm(const double A1, const XY& XY1, const double A2, const XY& XY2, const XY& XY3);

    //!  Computes  the following linear combination and <br>
    //! assigns the result to this number pair: <br>
    //!  A1 * XY1 + XY2 <br>
    void setLinearForm(const double A1, const XY& XY1, const XY& XY2);

    //!   Computes  the following linear combination and <br>
    //! assigns the result to this number pair: <br>
    //!  XY1 + XY2 <br>
    void setLinearForm(const XY& XY1, const XY& XY2);

    //! Assigns the given value to the X coordinate of this number pair. <br>
    void setX(const double X);
    //! Assigns the given value to the Y  coordinate of this number pair. <br>
    void setY(const double Y);

    //! Computes x*x + y*y where x and y are the two coordinates of this number pair. <br>
    double squareModulus() const;

    //!  <me>.x() = <me>.x() - Other.x() <br>
    //!  <me>.y() = <me>.y() - Other.y() <br>
    void subtract(const XY& Right);
    //!  new.x() = <me>.x() - Other.x() <br>
    //!  new.y() = <me>.y() - Other.y() <br>
    XY subtracted(const XY& Right) const;
    //! Returns the x coordinate of this number pair. <br>
    double x() const;
    //! Returns the y coordinate of this number pair. <br>
    double y() const;

protected:
private:
    double _x;
    double _y;
};

}  // namespace Geom