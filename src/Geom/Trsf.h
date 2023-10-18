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

#include <Geom/Mat.h>
#include <Geom/XYZ.h>
namespace Base { class Matrix4D; }

namespace Geom
{
class Ax1;
class Ax2;
class Ax3;
class Pnt;
class Vec;
class GTrsf;
class Trsf2d;
}  // namespace Geom


namespace Geom
{
//! Defines a non-persistent transformation in 3D space. <br>
//!  The following transformations are implemented : <br>
//!  . Translation, Rotation, Scale <br>
//!  . Symmetry with respect to a point, a line, a plane. <br>
//!  Complex transformations can be obtained by combining the <br>
//!  previous elementary transformations using the method <br>
//!  Multiply. <br>
//!  The transformations can be represented as follow : <br>
//! <br>
//!       V1   V2   V3    T       XYZ        XYZ <br>
//!    | a11  a12  a13   a14 |   | x |      | x'| <br>
//!    | a21  a22  a23   a24 |   | y |      | y'| <br>
//!    | a31  a32  a33   a34 |   | z |   =  | z'| <br>
//!    |  0    0    0     1  |   | 1 |      | 1 | <br>

class LX_GEOM_EXPORT Trsf
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
    //! Returns the identity transformation. <br>
    Trsf();
    //! Creates  a 3D transformation from the 2D transformation T. <br>
    //! The resulting transformation has a homogeneous <br>
    //! vectorial part, V3, and a translation part, T3, built from T: <br>
    //!       a11    a12 <br>
    //! 0             a13 <br>
    //! V3 =    a21    a22    0       T3 <br>
    //! =   a23 <br>
    //!           0    0    1. <br>
    //! 0 <br>
    //! It also has the same scale factor as T. This <br>
    //! guarantees (by projection) that the transformation <br>
    //! which would be performed by T in a plane (2D space) <br>
    //! is performed by the resulting transformation in the xOy <br>
    //! plane of the 3D space, (i.e. in the plane defined by the <br>
    //! origin (0., 0., 0.) and the vectors DX (1., 0., 0.), and DY <br>
    //! (0., 1., 0.)). The scale factor is applied to the entire space. <br>
    explicit Trsf(const Geom::Trsf2d& T);

    Trsf(const Geom::Mat& mat, const Geom::XYZ& location, double scale);
    Trsf(const Base::Matrix4D& mtrx);

    //! Copy constructor
    Trsf(const Trsf& rhs);

    enum FormEnum
    {
        Identity,
        Rotation,
        Translation,
        PntMirror,
        Ax1Mirror,
        Ax2Mirror,
        Scale,
        CompoundTrsf,
        Other
    };

    //!  Makes the transformation into a symmetrical transformation. <br>
    //!  P is the center of the symmetry. <br>
    void setMirror(const Geom::Pnt& P);


    //!  Makes the transformation into a symmetrical transformation. <br>
    //!  A1 is the center of the axial symmetry. <br>
    void setMirror(const Geom::Ax1& A1);


    //!  Makes the transformation into a symmetrical transformation. <br>
    //!  A2 is the center of the planar symmetry <br>
    //!  and defines the plane of symmetry by its origin, "X <br>
    //!  Direction" and "Y Direction". <br>
    void setMirror(const Geom::Ax2& A2);


    //!  Changes the transformation into a rotation. <br>
    //!  A1 is the rotation axis and Ang is the angular value of the <br>
    //!  rotation in radians. <br>
    void setRotation(const Geom::Ax1& A1, const double Ang);


    //!  Changes the transformation into a scale. <br>
    //!  P is the center of the scale and S is the scaling value. <br>
    //!  Raises ConstructionError  If <S> is null. <br>
    void setScale(const Geom::Pnt& P, const double S);


    //!  Modifies this transformation so that it transforms the <br>
    //!  coordinate system defined by FromSystem1 into the <br>
    //!  one defined by ToSystem2. After this modification, this <br>
    //!  transformation transforms: <br>
    //! -   the origin of FromSystem1 into the origin of ToSystem2, <br>
    //! -   the "X Direction" of FromSystem1 into the "X <br>
    //!   Direction" of ToSystem2, <br>
    //! -   the "Y Direction" of FromSystem1 into the "Y <br>
    //!   Direction" of ToSystem2, and <br>
    //! -   the "main Direction" of FromSystem1 into the "main <br>
    //!   Direction" of ToSystem2. <br>
    //! Warning <br>
    //! When you know the coordinates of a point in one <br>
    //! coordinate system and you want to express these <br>
    //! coordinates in another one, do not use the <br>
    //! transformation resulting from this function. Use the <br>
    //! transformation that results from SetTransformation instead. <br>
    //! SetDisplacement and SetTransformation create <br>
    //! related transformations: the vectorial part of one is the <br>
    //! inverse of the vectorial part of the other. <br>
    void setDisplacement(const Geom::Ax3& FromSystem1, const Geom::Ax3& ToSystem2);

    //! Modifies this transformation so that it transforms the <br>
    //! coordinates of any point, (x, y, z), relative to a source <br>
    //! coordinate system into the coordinates (x', y', z') which <br>
    //! are relative to a target coordinate system, but which <br>
    //! represent the same point <br>
    //!  The transformation is from the coordinate <br>
    //!  system "FromSystem1" to the coordinate system "ToSystem2". <br>
    //! Example : <br>
    //!  In a C++ implementation : <br>
    //!  Real x1, y1, z1;  // are the coordinates of a point in the <br>
    //!                    // local system FromSystem1 <br>
    //!  Real x2, y2, z2;  // are the coordinates of a point in the <br>
    //!                    // local system ToSystem2 <br>
    //!  Geom::Pnt P1 (x1, y1, z1) <br>
    //!  Trsf T; <br>
    //!  T.SetTransformation (FromSystem1, ToSystem2); <br>
    //!  Geom::Pnt P2 = P1.Transformed (T); <br>
    //!  P2.Coord (x2, y2, z2); <br>
    void setTransformation(const Geom::Ax3& FromSystem1, const Geom::Ax3& ToSystem2);

    //! Modifies this transformation so that it transforms the <br>
    //!  coordinates of any point, (x, y, z), relative to a source <br>
    //!  coordinate system into the coordinates (x', y', z') which <br>
    //!  are relative to a target coordinate system, but which <br>
    //!  represent the same point <br>
    //!  The transformation is from the default coordinate system <br>
    //!  {P(0.,0.,0.), VX (1.,0.,0.), VY (0.,1.,0.), VZ (0., 0. ,1.) } <br>
    //!  to the local coordinate system defined with the Ax3 ToSystem. <br>
    //!  Use in the same way  as the previous method. FromSystem1 is <br>
    //!  defaulted to the absolute coordinate system. <br>
    void setTransformation(const Geom::Ax3& ToSystem);

    //!  Changes the transformation into a translation. <br>
    //!  V is the vector of the translation. <br>
    void setTranslation(const Geom::Vec& V);

    //! Makes the transformation into a translation where the translation vector <br>
    //! is the vector (P1, P2) defined from point P1 to point P2. <br>
    void setTranslation(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //!  Replaces the translation vector with the vector V. <br>
    void setTranslationPart(const Geom::Vec& V);

    //! Add vector V to the translation vector. <br>
    void translate(const Geom::Vec& V);

    //!  Modifies the scale factor. <br>
    //! Raises ConstructionError  If S is null. <br>
    void setScaleFactor(const double S);

    //! Sets the coefficients  of the transformation.  The <br>
    //!          transformation  of the  point  x,y,z is  the point <br>
    //!          x',y',z' with : <br>
    //! <br>
    //!          x' = a11 x + a12 y + a13 z + a14 <br>
    //!          y' = a21 x + a22 y + a23 z + a24 <br>
    //!          z' = a31 x + a32 y + a43 z + a34 <br>
    //! <br>
    //!          Tolang and  TolDist are  used  to  test  for  null <br>
    //!          angles and null distances to determine the form of <br>
    //!          the transformation (identity, translation, etc..). <br>
    //! <br>
    //!          The method Value(i,j) will return aij. <br>
    //!          Raises ConstructionError if the determinant of  the aij is null. Or  if <br>
    //!          the matrix as not a uniform scale. <br>
    void setValues(double a11,
                   double a12,
                   double a13,
                   double a14,
                   double a21,
                   double a22,
                   double a23,
                   double a24,
                   double a31,
                   double a32,
                   double a33,
                   double a34,
                   double Tolang,
                   double TolDist);
    //! Returns true if the determinant of the vectorial part of <br>
    //! this transformation is negative. <br>
    bool isNegative() const;

    //! Returns true if this is an identity transformation of <br>
    //! In contrast to form() == Geom::Trsf::Identity this method checks the values. <br>
    bool isIdentity() const;
    //! Sets the transformation to identity. <br>
    void setIdentity();

    //!  Returns the nature of the transformation. It can be: an <br>
    //! identity transformation, a rotation, a translation, a mirror <br>
    //! transformation (relative to a point, an axis or a plane), a <br>
    //! scaling transformation, or a compound transformation. <br>
    // TODO
    Trsf::FormEnum form() const;
    //! Returns the scale factor. <br>
    double scaleFactor() const;

    //!  Returns the translation part of the transformation's matrix <br>
    const Geom::XYZ& translationPart() const;


    //!  Returns the vectorial part of the transformation. It is <br>
    //!  a 3*3 matrix which includes the scale factor. <br>
    Geom::Mat vectorialPart() const;

    //!  Computes the homogeneous vectorial part of the transformation. <br>
    //!  It is a 3*3 matrix which doesn't include the scale factor. <br>
    //! In other words, the vectorial part of this transformation is <br>
    //! equal to its homogeneous vectorial part, multiplied by the scale factor. <br>
    //!  The coefficients of this matrix must be multiplied by the <br>
    //!  scale factor to obtain the coefficients of the transformation. <br>
    const Geom::Mat& hVectorialPart() const;

    //!  Returns the coefficients of the transformation's matrix. <br>
    //!  It is a 3 rows * 4 columns matrix. <br>
    //!  This coefficient includes the scale factor. <br>
    //!  Raises OutOfRanged if Row < 1 or Row > 3 or Col < 1 or Col > 4 <br>
    double value(const int Row, const int Col) const;


    void invert();

    //!  Computes the reverse transformation <br>
    //!  Raises an exception if the matrix of the transformation <br>
    //!  is not inversible, it means that the scale factor is lower <br>
    //!  or equal to Resolution from package gp. <br>
    //!  Computes the transformation composed with T and  <me>. <br>
    //!  In a C++ implementation you can also write Tcomposed = <me> * T. <br>
    //! Example : <br>
    //!      Trsf T1, T2, Tcomp; ............... <br>
    //!        Tcomp = T2.Multiplied(T1);         // or   (Tcomp = T2 * T1) <br>
    //!        Pnt P1(10.,3.,4.); <br>
    //!        Pnt P2 = P1.Transformed(Tcomp);    //using Tcomp <br>
    //!        Pnt P3 = P1.Transformed(T1);       //using T1 then T2 <br>
    //!        P3.Transform(T2);                  // P3 = P2 !!! <br>
    Trsf inverted() const;

    Trsf multiplied(const Trsf& T) const;
    Trsf operator*(const Trsf& T) const { return multiplied(T); }



    //!  Computes the transformation composed with T and  <me>. <br>
    //!  In a C++ implementation you can also write Tcomposed = <me> * T. <br>
    //!  Example : <br>
    //!      Trsf T1, T2, Tcomp; ............... <br>
    //!      //composition : <br>
    //!        Tcomp = T2.Multiplied(T1);         // or   (Tcomp = T2 * T1) <br>
    //!      // transformation of a point <br>
    //!        Pnt P1(10.,3.,4.); <br>
    //!        Pnt P2 = P1.Transformed(Tcomp);    //using Tcomp <br>
    //!        Pnt P3 = P1.Transformed(T1);       //using T1 then T2 <br>
    //!        P3.Transform(T2);                  // P3 = P2 !!! <br>
    void multiply(const Trsf& T);
    void operator*=(const Trsf& T) { multiply(T); }



    //!  Computes the transformation composed with <me> and T. <br>
    //!  <me> = T * <me> <br>
    void preMultiply(const Trsf& T);


    void power(const int N);

    //!  Computes the following composition of transformations <br>
    //!  <me> * <me> * .......* <me>, N time. <br>
    //!  if N = 0 <me> = Identity <br>
    //!  if N < 0 <me> = <me>.Inverse() *...........* <me>.Inverse(). <br>
    Trsf powered(const int N);

    void transforms(double& X, double& Y, double& Z) const;
    //! Transformation of a triplet XYZ with a Trsf <br>
    void transforms(Geom::XYZ& Coord) const;

    void toMatrix4D(Base::Matrix4D& mtrx);

    friend class gp_GTrsf;
    friend class Geom::GTrsf;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    bool isSameAs(const Trsf& T) const;

private:
    double _scale;
    Trsf::FormEnum _shape;
    Geom::Mat _matrix;
    Geom::XYZ _loc;
};

}  // namespace Geom
