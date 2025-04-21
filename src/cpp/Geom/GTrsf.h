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

#include <Geom/Trsf.h>




//!  Defines a non-persistent transformation in 3D space. <br>
//!  This transformation is a general transformation. <br>
//!  It can be a Trsf from gp, an affinity, or you can define <br>
//!  your own transformation giving the matrix of transformation. <br>
//! <br>
//!  With a Gtrsf you can transform only a triplet of coordinates <br>
//!  XYZ. It is not possible to transform other geometric objects <br>
//!  because these transformations can change the nature of non- <br>
//!  elementary geometric objects. <br>
//!  The transformation GTrsf can be represented as follow : <br>
//! <br>
//!       V1   V2   V3    T       XYZ        XYZ <br>
//!    | a11  a12  a13   a14 |   | x |      | x'| <br>
//!    | a21  a22  a23   a24 |   | y |      | y'| <br>
//!    | a31  a32  a33   a34 |   | z |   =  | z'| <br>
//!    |  0    0    0     1  |   | 1 |      | 1 | <br>

namespace Geom
{
class LX_GEOM_EXPORT GTrsf
{
public:
    //! Returns the Identity transformation. <br>
    GTrsf();

    //!  Converts the Geom::Trsf transformation T into a <br>
    //!   general transformation, i.e. Returns a GTrsf with <br>
    //! the same matrix of coefficients as the Trsf T. <br>
    GTrsf(const Geom::Trsf& T);

    //!  Creates a transformation based on the matrix M and the <br>
    //!    vector V where M defines the vectorial part of <br>
    //!    the transformation, and V the translation part, or <br>
    GTrsf(const Geom::Mat& M, const Geom::XYZ& V);
    //! Changes this transformation into an affinity of ratio Ratio <br>
    //! with respect to the axis A1. <br>
    //!   Note: an affinity is a point-by-point transformation that <br>
    //! transforms any point P into a point P' such that if H is <br>
    //! the orthogonal projection of P on the axis A1 or the <br>
    //! plane A2, the vectors HP and HP' satisfy: <br>
    //! HP' = Ratio * HP. <br>
    void SetAffinity(const Geom::Ax1& A1, const double Ratio);
    //! Changes this transformation into an affinity of ratio Ratio <br>
    //! with respect to  the plane defined by the origin, the "X Direction" and <br>
    //!   the "Y Direction" of coordinate system A2. <br>
    //!   Note: an affinity is a point-by-point transformation that <br>
    //! transforms any point P into a point P' such that if H is <br>
    //! the orthogonal projection of P on the axis A1 or the <br>
    //! plane A2, the vectors HP and HP' satisfy: <br>
    //! HP' = Ratio * HP. <br>
    void SetAffinity(const Geom::Ax2& A2, const double Ratio);

    //!  Replaces  the coefficient (Row, Col) of the matrix representing <br>
    //! this transformation by Value.  Raises OutOfRange <br>
    //! if  Row < 1 or Row > 3 or Col < 1 or Col > 4 <br>
    void SetValue(const int Row, const int Col, const double Value);
    //! Replaces the vectorial part of this transformation by Matrix. <br>
    void SetVectorialPart(const Geom::Mat& Matrix);
    //! Replaces the translation part of <br>
    //! this transformation by the coordinates of the number triple Coord. <br>
    void SetTranslationPart(const Geom::XYZ& Coord);
    //!  Assigns the vectorial and translation parts of T to this transformation. <br>
    void SetTrsf(const Geom::Trsf& T);

    //!   Returns true if the determinant of the vectorial part of <br>
    //! this transformation is negative. <br>
    unsigned int IsNegative() const;

    //!  Returns true if this transformation is singular (and <br>
    //! therefore, cannot be inverted). <br>
    //! Note: The Gauss LU decomposition is used to invert the <br>
    //! transformation matrix. Consequently, the transformation <br>
    //! is considered as singular if the largest pivot found is less <br>
    //! than or equal to Geom::Precision::linear_Resolution(). <br>
    //! Warning <br>
    //! If this transformation is singular, it cannot be inverted. <br>
    unsigned int IsSingular() const;

    //!  Returns the nature of the transformation.  It can be an <br>
    //! identity transformation, a rotation, a translation, a mirror <br>
    //! transformation (relative to a point, an axis or a plane), a <br>
    //! scaling transformation, a compound transformation or <br>
    //! some other type of transformation. <br>
    Geom::Trsf::FormEnum Form() const;

    //!  verify and set the shape of the GTrsf Other or CompoundTrsf <br>
    //!  Ex : <br>
    //!  myGTrsf.SetValue(row1,col1,val1); <br>
    //!  myGTrsf.SetValue(row2,col2,val2); <br>
    //!  ... <br>
    //!  myGTrsf.SetForm(); <br>
    void SetForm();
    //!  Returns the translation part of the GTrsf. <br>
    const Geom::XYZ& TranslationPart() const;

    //!  Computes the vectorial part of the GTrsf. The returned Matrix <br>
    //!  is a  3*3 matrix. <br>
    const Geom::Mat& VectorialPart() const;

    //!  Returns the coefficients of the global matrix of transformation. <br>
    //! Raises OutOfRange if Row < 1 or Row > 3 or Col < 1 or Col > 4 <br>
    double Value(const int Row, const int Col) const;
    double operator()(const int Row, const int Col) const { return Value(Row, Col); }

    void Invert();

    //!  Computes the reverse transformation. <br>
    //!  Raises an exception if the matrix of the transformation <br>
    //!  is not inversible. <br>
    Geom::GTrsf Inverted() const;

    //!  Computes the transformation composed from T and <me>. <br>
    //!  In a C++ implementation you can also write Tcomposed = <me> * T. <br>
    //! Example : <br>
    //!      GTrsf T1, T2, Tcomp; ............... <br>
    //!      //composition : <br>
    //!        Tcomp = T2.Multiplied(T1);         // or   (Tcomp = T2 * T1) <br>
    //!      // transformation of a point <br>
    //!        XYZ P(10.,3.,4.); <br>
    //!        XYZ P1(P); <br>
    //!        Tcomp.Transforms(P1);               //using Tcomp <br>
    //!        XYZ P2(P); <br>
    //!        T1.Transforms(P2);                  //using T1 then T2 <br>
    //!        T2.Transforms(P2);                  // P1 = P2 !!! <br>
    //! C++: alias operator *= <br>
    void Multiply(const Geom::GTrsf& T);

    //!  Computes the transformation composed with <me> and T. <br>
    //!  <me> = T * <me> <br>
    Geom::GTrsf Multiplied(const Geom::GTrsf& T) const;

    //! Computes the product of the transformation T and this <br>
    //! transformation and assigns the result to this transformation. <br>
    //! this = T * this <br>
    void PreMultiply(const Geom::GTrsf& T);

    void Power(const int N);

    //!  Computes: <br>
    //!  -   the product of this transformation multiplied by itself <br>
    //!   N times, if N is positive, or <br>
    //! -   the product of the inverse of this transformation <br>
    //!   multiplied by itself |N| times, if N is negative. <br>
    //!   If N equals zero, the result is equal to the Identity <br>
    //!  transformation. <br>
    //!  I.e.:  <me> * <me> * .......* <me>, N time. <br>
    //!  if N =0 <me> = Identity <br>
    //!  if N < 0 <me> = <me>.Inverse() *...........* <me>.Inverse(). <br>
    Geom::GTrsf Powered(const int N) const;

    void Transforms(Geom::XYZ& Coord) const;
    //! Transforms a triplet XYZ with a GTrsf. <br>
    void Transforms(double& X, double& Y, double& Z) const;

    Geom::Trsf Trsf(bool aAllowOtherFormInConstruction = false) const;
    // const Geom::Mat& _CSFDB_GetGTrsfmatrix() const { return matrix; }
    // const Geom::XYZ& _CSFDB_GetGTrsfloc() const { return loc; }
    // Base::TrsfForm _CSFDB_GetGTrsfshape() const { return shape; }
    // void _CSFDB_SetGTrsfshape(const Base::TrsfForm p) { shape = p; }
    // double _CSFDB_GetGTrsfscale() const { return scale; }
    // void _CSFDB_SetGTrsfscale(const double p) { scale = p; }

    bool operator==(const Geom::GTrsf& Other) const;
    size_t hash() const;

protected:
private:
    Geom::Mat matrix;
    Geom::XYZ loc;
    Geom::Trsf::FormEnum shape;
    double scale;
};



}  // namespace Geom


namespace std
{
template <>
struct hash<Geom::GTrsf>
{
    size_t operator()(const Geom::GTrsf& t) const { return t.hash(); }
};
}  // namespace std
