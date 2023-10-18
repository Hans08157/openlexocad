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
class XYZ;
class GTrsf;
}  // namespace Geom



namespace Geom
{
//! Describes a three column, three row matrix. This sort of <br>
//! object is used in various vectorial or matrix computations. <br>
class LX_GEOM_EXPORT Mat
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    //! creates  a matrix with null coefficients. <br>
    Mat();

    Mat(const double a11,
        const double a12,
        const double a13,
        const double a21,
        const double a22,
        const double a23,
        const double a31,
        const double a32,
        const double a33);
    //! Creates a matrix. <br>
    //!  Col1, Col2, Col3 are the 3 columns of the matrix. <br>
    Mat(const XYZ& Col1, const XYZ& Col2, const XYZ& Col3);
    //! Assigns the three coordinates of Value to the column of index <br>
    //!   Col of this matrix. <br>
    //! Raises OutOfRange if Col < 1 or Col > 3. <br>
    void setCol(const int Col, const XYZ& Value);
    //! Assigns the number triples Col1, Col2, Col3 to the three <br>
    //!   columns of this matrix. <br>
    void setCols(const XYZ& Col1, const XYZ& Col2, const XYZ& Col3);

    //!  Modifies the matrix  M so that applying it to any number <br>
    //! triple (X, Y, Z) produces the same result as the cross <br>
    //! product of Ref and the number triple (X, Y, Z): <br>
    //! i.e.: M * {X,Y,Z}t = Ref.Cross({X, Y ,Z}) <br>
    //!  this matrix is anti symmetric. To apply this matrix to the <br>
    //!  triplet  {XYZ} is the same as to do the cross product between the <br>
    //!  triplet Ref and the triplet {XYZ}. <br>
    //! Note: this matrix is anti-symmetric. <br>
    void setCross(const XYZ& Ref);

    //!  Modifies the main diagonal of the matrix. <br>
    //!  <me>.Value (1, 1) = X1 <br>
    //!  <me>.Value (2, 2) = X2 <br>
    //!  <me>.Value (3, 3) = X3 <br>
    //!  The other coefficients of the matrix are not modified. <br>
    void setDiagonal(const double X1, const double X2, const double X3);

    //!  Modifies this matrix so that applying it to any number <br>
    //! triple (X, Y, Z) produces the same result as the scalar <br>
    //! product of Ref and the number triple (X, Y, Z): <br>
    //! this * (X,Y,Z) = Ref.(X,Y,Z) <br>
    //! Note: this matrix is symmetric. <br>
    void setDot(const XYZ& Ref);
    //! Modifies this matrix so that it represents the Identity matrix. <br>
    void setIdentity();
    //! Returns true if this matrix represents the Identity matrix. <br>
    bool isIdentity() const;

    //!  Modifies this matrix so that it represents a rotation. Ang is the angular value in <br>
    //!  radians and the XYZ axis gives the direction of the <br>
    //!  rotation. <br>
    //!  Raises ConstructionError if XYZ.Modulus() <= Resolution() <br>
    void setRotation(const XYZ& Axis, const double Ang);
    //! Assigns the three coordinates of Value to the row of index <br>
    //!   Row of this matrix. Raises OutOfRange if Row < 1 or Row > 3. <br>
    void setRow(const int Row, const XYZ& Value);
    //! Assigns the number triples Row1, Row2, Row3 to the three <br>
    //!   rows of this matrix. <br>
    void setRows(const XYZ& Row1, const XYZ& Row2, const XYZ& Row3);

    //!  Modifies the the matrix so that it represents <br>
    //! a scaling transformation, where S is the scale factor. : <br>
    //!           | S    0.0  0.0 | <br>
    //!   <me> =  | 0.0   S   0.0 | <br>
    //!           | 0.0  0.0   S  | <br>
    void setScale(const double S);
    //! Assigns <Value> to the coefficient of row Row, column Col of   this matrix. <br>
    //! Raises OutOfRange if Row < 1 or Row > 3 or Col < 1 or Col > 3 <br>
    void setValue(const int Row, const int Col, const double Value);
    //! Returns the column of Col index. <br>
    //!   Raises OutOfRange if Col < 1 or Col > 3 <br>
    XYZ column(const int Col) const;
    //! Computes the determinant of the matrix. <br>
    double determinant() const;
    //! Returns the main diagonal of the matrix. <br>
    XYZ diagonal() const;
    //! returns the row of Row index. <br>
    //!  Raises OutOfRange if Row < 1 or Row > 3 <br>
    XYZ row(const int Row) const;
    //! Returns the coefficient of range (Row, Col) <br>
    //!  Raises OutOfRange if Row < 1 or Row > 3 or Col < 1 or Col > 3 <br>
    const double& value(const int Row, const int Col) const;

    const double& operator()(const int Row, const int Col) const { return value(Row, Col); }

    //! Returns the coefficient of range (Row, Col) <br>
    //!  Raises OutOfRange if Row < 1 or Row > 3 or Col < 1 or Col > 3 <br>
    double& changeValue(const int Row, const int Col);

    double& operator()(const int Row, const int Col) { return changeValue(Row, Col); }

    //!  The Gauss LU decomposition is used to invert the matrix <br>
    //!  (see Math package) so the matrix is considered as singular if <br>
    //!  the largest pivot found is lower or equal to Resolution from gp. <br>
    bool isSingular() const;

    void add(const Mat& Other);

    void operator+=(const Mat& Other) { add(Other); }

    //! Computes the sum of this matrix and <br>
    //!  the matrix Other for each coefficient of the matrix : <br>
    //!  <me>.Coef(i,j) + <Other>.Coef(i,j) <br>
    Mat added(const Mat& Other) const;

    Mat operator+(const Mat& Other) const { return added(Other); }

    void divide(const double Scalar);

    void operator/=(const double Scalar) { divide(Scalar); }

    //! Divides all the coefficients of the matrix by Scalar <br>
    Mat divided(const double Scalar) const;

    Mat operator/(const double Scalar) const { return divided(Scalar); }

    void invert();

    //!  Inverses the matrix and raises if the matrix is singular. <br>
    //! -   Invert assigns the result to this matrix, while <br>
    //! -   Inverted creates a new one. <br>
    //! Warning <br>
    //! The Gauss LU decomposition is used to invert the matrix. <br>
    //! Consequently, the matrix is considered as singular if the <br>
    //! largest pivot found is less than or equal to Geom::Precision::linear_Resolution(). <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if this matrix is singular, <br>
    //! and therefore cannot be inverted. <br>
    Mat inverted() const;

    //!  Computes  the product of two matrices <me> * <Other> <br>
    Mat multiplied(const Mat& Other) const;

    Mat operator*(const Mat& Other) const { return multiplied(Other); }

    //! Computes the product of two matrices <me> = <Other> * <me>. <br>
    void multiply(const Mat& Other);

    void operator*=(const Mat& Other) { multiply(Other); }

    void preMultiply(const Mat& Other);

    Mat multiplied(const double Scalar) const;

    Mat operator*(const double Scalar) const { return multiplied(Scalar); }

    //!  Multiplies all the coefficients of the matrix by Scalar <br>
    void multiply(const double Scalar);

    void operator*=(const double Scalar) { multiply(Scalar); }

    void power(const int N);

    //!  Computes <me> = <me> * <me> * .......* <me>,   N time. <br>
    //!  if N = 0 <me> = Identity <br>
    //!  if N < 0 <me> = <me>.Invert() *...........* <me>.Invert(). <br>
    //!  If N < 0 an exception will be raised if the matrix is not <br>
    //!  invertible <br>
    Mat powered(const int N) const;

    void subtract(const Mat& Other);

    void operator-=(const Mat& Other) { subtract(Other); }

    //!  cOmputes for each coefficient of the matrix : <br>
    //!  <me>.Coef(i,j) - <Other>.Coef(i,j) <br>
    Mat subtracted(const Mat& Other) const;

    Mat operator-(const Mat& Other) const { return subtracted(Other); }

    bool operator==(const Mat& Other) const;

    bool operator!=(const Mat& Other) const { return !(operator==(Other)); }

    void transpose();

    //!  Transposes the matrix. A(j, i) -> A (i, j) <br>
    Mat transposed() const;

    friend class XYZ;
    friend class CA_Transfrom;
    friend class gp_GTrsf;
    friend class Geom::GTrsf;

    Geom::XYZ computeEulerAngles() const;

    void initFromQuaternion(double w, double x, double y, double z);

    bool toQuaternion(double& w, double& x, double& y, double& z);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    bool isEqual(const Mat& Other, double Tolerance) const;
    size_t hash() const;

private:
    double matrix[3][3];
};
}  // namespace Geom

namespace std
{
template <>
struct hash<Geom::Mat>
{
    size_t operator()(const Geom::Mat& m) const { return m.hash(); }
};
}  // namespace std
