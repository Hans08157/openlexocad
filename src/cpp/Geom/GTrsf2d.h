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

#include <Geom/Trsf2d.h>

namespace Geom
{
class Ax2d;
class Mat2d;
class XY;

//! Defines a non persistent transformation in 2D space. <br>
//! This transformation is a general transformation. <br>
//! It can be a Trsf2d from package gp, an affinity, or you can <br>
//! define your own transformation giving the corresponding <br>
//! matrix of transformation. <br>
//! <br>
//! With a GTrsf2d you can transform only a doublet of coordinates <br>
//! XY. It is not possible to transform other geometric objects <br>
//! because these transformations can change the nature of non- <br>
//! elementary geometric objects. <br>
//! A GTrsf2d is represented with a 2 rows * 3 columns matrix : <br>
//! <br>
//! V1 V2 T XY XY <br>
//! | a11 a12 a14 | | x | | x'| <br>
//! | a21 a22 a24 | | y | | y'| <br>
//! | 0 0 1 | | 1 | | 1 | <br>
class LX_GEOM_EXPORT GTrsf2d
{
public:
    //! returns identity transformation. <br>
    GTrsf2d();
    //! Converts the Trsf2d transformation T into a <br>
    //! general transformation. <br>
    GTrsf2d(const Trsf2d& T);
    //! Creates a transformation based on the matrix M and the <br>
    //! vector V where M defines the vectorial part of the <br>
    //! transformation, and V the translation part. <br>
    GTrsf2d(const Mat2d& M, const XY& V);


    //! Returns the nature of the transformation. It can be <br>
    //! an identity transformation, a rotation, a translation, a mirror <br>
    //! transformation (relative to a point or axis), a scaling <br>
    //! transformation, a compound transformation or some <br>
    //! other type of transformation. <br>
    Trsf2d::FormEnum form() const;


    void invert();



    //! Computes the reverse transformation. <br>
    //! Raised an exception if the matrix of the transformation <br>
    //! is not inversible. <br>
    GTrsf2d inverted() const;



    //! Returns true if the determinant of the vectorial part of <br>
    //! this transformation is negative. <br>
    bool isNegative() const;

    //! Returns true if this transformation is singular (and <br>
    //! therefore, cannot be inverted). <br>
    //! Note: The Gauss LU decomposition is used to invert the <br>
    //! transformation matrix. Consequently, the transformation <br>
    //! is considered as singular if the largest pivot found is less <br>
    //! than or equal to Geom::Precision::linear_Resolution(). <br>
    //! Warning <br>
    //! If this transformation is singular, it cannot be inverted. <br>
    bool isSingular() const;


    //! Computes the transformation composed with T and <me>. <br>
    //! In a C++ implementation you can also write Tcomposed = <me> * T. <br>
    //! Example : <br>
    //! GTrsf2d T1, T2, Tcomp; ............... <br>
    //! //composition : <br>
    //! Tcomp = T2.multiplied(T1); // or (Tcomp = T2 * T1) <br>
    //! // transformation of a point <br>
    //! XY P(10.,3.); <br>
    //! XY P1(P); <br>
    //! Tcomp.transforms(P1); //using Tcomp <br>
    //! XY P2(P); <br>
    //! T1.transforms(P2); //using T1 then T2 <br>
    //! T2.transforms(P2); // P1 = P2 !!! <br>
    GTrsf2d multiplied(const GTrsf2d& T) const;


    void multiply(const GTrsf2d& T);

    void operator*=(const GTrsf2d& T) { multiply(T); }

    //
    GTrsf2d operator*(const GTrsf2d& T) const { return multiplied(T); }


    double operator()(const int Row, const int Col) const { return value(Row, Col); }


    void power(const int N);


    GTrsf2d powered(const int N) const;



    //! Computes the product of the transformation T and this <br>
    //! transformation, and assigns the result to this transformation: <br>
    //! this = T * this <br>
    void preMultiply(const GTrsf2d& T);

    //! Changes this transformation into an affinity of ratio Ratio <br>
    //! with respect to the axis A. <br>
    //! Note: An affinity is a point-by-point transformation that <br>
    //! transforms any point P into a point P' such that if H is <br>
    //! the orthogonal projection of P on the axis A, the vectors <br>
    //! HP and HP' satisfy: HP' = Ratio * HP. <br>
    void setAffinity(const Ax2d& A, const double Ratio);

    //! Replaces the translation part of this <br>
    //! transformation by the coordinates of the number pair Coord. <br>
    void setTranslationPart(const XY& Coord);

    //! Assigns the vectorial and translation parts of T to this transformation. <br>
    void setTrsf2d(const Trsf2d& T);


    //! Replaces the coefficient (Row, Col) of the matrix representing <br>
    //! this transformation by Value, <br>
    //! Raises OutOfRange if Row < 1 or Row > 2 or Col < 1 or Col > 3 <br>
    void setValue(const int Row, const int Col, const double Value);
    //! Replaces the vectorial part of this transformation by Matrix. <br>
    void setVectorialPart(const Mat2d& Matrix);


    //! Returns the translation part of the GTrsf2d. <br>
    const XY& translationPart() const;



    XY transformed(const XY& Coord) const;



    void transforms(XY& Coord) const;



    //! Applies this transformation to the coordinates: <br>
    //! - of the number pair Coord, or <br>
    //! - X and Y. <br>
    //! <br>
    //! Note: <br>
    //! - transforms modifies X, Y, or the coordinate pair Coord, while <br>
    //! - transformed creates a new coordinate pair. <br>
    void transforms(double& X, double& Y) const;



    //! Converts this transformation into a Trsf2d transformation. <br>
    //! Exceptions <br>
    //! Standard_ConstructionError if this transformation <br>
    //! cannot be converted, i.e. if its form is Trsf2d::Other. <br>
    Trsf2d trsf2d() const;

    //! Returns the coefficients of the global matrix of transformation. <br>
    //! Raises OutOfRange if Row < 1 or Row > 2 or Col < 1 or Col > 3 <br>
    double value(const int Row, const int Col) const;
    //! Computes the vectorial part of the GTrsf2d. The returned <br>
    //! Matrix is a 2*2 matrix. <br>
    const Mat2d& vectorialPart() const;

    const Mat2d& _CSFDB_GetGTrsf2dmatrix() const { return matrix; }
    const XY& _CSFDB_GetGTrsf2dloc() const { return loc; }
    Trsf2d::FormEnum _CSFDB_GetGTrsf2dshape() const { return shape; }
    void _CSFDB_SetGTrsf2dshape(const Trsf2d::FormEnum p) { shape = p; }
    double _CSFDB_GetGTrsf2dscale() const { return scale; }
    void _CSFDB_SetGTrsf2dscale(const double p) { scale = p; }



protected:
private:
    Mat2d matrix;
    XY loc;
    Trsf2d::FormEnum shape;
    double scale;
};

}  // namespace Geom