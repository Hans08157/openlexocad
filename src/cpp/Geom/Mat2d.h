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
class GTrsf2d;
class Trsf2d;
class XY;

//! Describes a two column, two row matrix. This sort of <br>
//! object is used in various vectorial or matrix computations. <br>
class LX_GEOM_EXPORT Mat2d
{
public:
    //! Creates a matrix with null coefficients. <br>
    Mat2d();

    //! Col1, Col2 are the 2 columns of the matrix. <br>
    Mat2d(const XY& Col1, const XY& Col2);
    void add(const Mat2d& Other);
    //! Computes the sum of this matrix and the matrix <br>
    //! Other.for each coefficient of the matrix : <br>
    //! <me>.Coef(i,j) + <Other>.Coef(i,j) <br>
    //! Note: <br>
    //! - operator += assigns the result to this matrix, while <br>
    //! - operator + creates a new one. <br>
    Mat2d added(const Mat2d& Other) const;
    //! Returns the coefficient of range (Row, Col) <br>
    //! Raises OutOfRange <br>
    //! if Row < 1 or Row > 2 or Col < 1 or Col > 2 <br>
    double& changeValue(const int Row, const int Col);
    //! Returns the column of Col index. <br>
    //! Raises OutOfRange if Col < 1 or Col > 2 <br>
    XY column(const int Col) const;
    //! Computes the determinant of the matrix. <br>
    double determinant() const;
    //! Returns the main diagonal of the matrix. <br>
    XY diagonal() const;
    void divide(const double Scalar);
    //! Divides all the coefficients of the matrix by a scalar. <br>
    Mat2d divided(const double Scalar) const;
    void invert();

    //! Inverses the matrix and raises exception if the matrix <br>
    //! is singular. <br>
    Mat2d inverted() const;

    static inline bool isEven(const int Value) { return Value % 2 == 0; }

    static inline bool isOdd(const int Value) { return Value % 2 != 0; }
    //! Returns true if this matrix is singular (and therefore, cannot be inverted). <br>
    //! The Gauss LU decomposition is used to invert the matrix <br>
    //! so the matrix is considered as singular if the largest <br>
    //! pivot found is lower or equal to Resolution from gp. <br>
    bool isSingular() const;

    Mat2d multiplied(const Mat2d& Other) const;
    //! Computes the product of two matrices <me> * <Other> <br>
    void multiply(const Mat2d& Other);
    Mat2d multiplied(const double Scalar) const;
    //! Multiplies all the coefficients of the matrix by a scalar. <br>
    void multiply(const double Scalar);
    void operator+=(const Mat2d& Other) { add(Other); }

    Mat2d operator+(const Mat2d& Other) const { return added(Other); }

    void operator-=(const Mat2d& Other) { subtract(Other); }

    Mat2d operator-(const Mat2d& Other) const { return subtracted(Other); }

    void operator*=(const double Scalar) { multiply(Scalar); }

    Mat2d operator*(const double Scalar) const { return multiplied(Scalar); }

    Mat2d operator*(const Mat2d& Other) const { return multiplied(Other); }

    void operator/=(const double Scalar) { divide(Scalar); }

    Mat2d operator/(const double Scalar) const { return divided(Scalar); }

    const double& operator()(const int Row, const int Col) const { return value(Row, Col); }
    double& operator()(const int Row, const int Col) { return changeValue(Row, Col); }

    void power(const int N);

    //! computes <me> = <me> * <me> * .......* <me>, N time. <br>
    //! if N = 0 <me> = Identity <br>
    //! if N < 0 <me> = <me>.Invert() *...........* <me>.Invert(). <br>
    //! If N < 0 an exception can be raised if the matrix is not <br>
    //! invertible <br>
    Mat2d powered(const int N) const;

    //! Modifies this matrix by pre-multiplying it by the matrix Other <br>
    //! <me> = Other * <me>. <br>
    void preMultiply(const Mat2d& Other);

    //! Returns the row of index Row. <br>//! Raised if Row < 1 or Row > 2 <br>
    XY row(const int Row) const;
    //! Assigns the two coordinates of Value to the column of range <br>
    //! Col of this matrix <br>
    //! Raises OutOfRange if Col < 1 or Col > 2. <br>
    void setCol(const int Col, const XY& Value);
    //! Assigns the number pairs Col1, Col2 to the two columns of this matrix <br>
    void setCols(const XY& Col1, const XY& Col2);

    //! Modifies the main diagonal of the matrix. <br>
    //! <me>.value (1, 1) = X1 <br>
    //! <me>.value (2, 2) = X2 <br>
    //! The other coefficients of the matrix are not modified. <br>
    void setDiagonal(const double X1, const double X2);
    //! Modifies this matrix, so that it represents the Identity matrix. <br>
    void setIdentity();

    //! Modifies this matrix, so that it represents a rotation. Ang is the angular <br>
    //! value in radian of the rotation. <br>
    void setRotation(const double Ang);
    //! Assigns the two coordinates of Value to the row of index Row of this matrix. <br>
    //! Raises OutOfRange if Row < 1 or Row > 2. <br>
    void setRow(const int Row, const XY& Value);
    //! Assigns the number pairs Row1, Row2 to the two rows of this matrix. <br>
    void setRows(const XY& Row1, const XY& Row2);

    //! Modifies the matrix such that it <br>
    //! represents a scaling transformation, where S is the scale factor : <br>
    //! | S 0.0 | <br>
    //! <me> = | 0.0 S | <br>
    void setScale(const double S);
    //! Assigns <Value> to the coefficient of row Row, column Col of this matrix. <br>
    //! Raises OutOfRange if Row < 1 or Row > 2 or Col < 1 or Col > 2 <br>
    void setValue(const int Row, const int Col, const double Value);
    void subtract(const Mat2d& Other);
    //! Computes for each coefficient of the matrix : <br>
    //! <me>.Coef(i,j) - <Other>.Coef(i,j) <br>
    Mat2d subtracted(const Mat2d& Other) const;
    void transpose();

    //! Transposes the matrix. A(j, i) -> A (i, j) <br>
    Mat2d transposed() const;

    //! Returns the coefficient of range (Row, Col) <br>
    //! Raises OutOfRange <br>
    //! if Row < 1 or Row > 2 or Col < 1 or Col > 2 <br>
    const double& value(const int Row, const int Col) const;
    friend class GTrsf2d;
    friend class Trsf2d;
    friend class XY;

protected:
private:
    double _matrix[2][2];
};
}  // namespace Geom