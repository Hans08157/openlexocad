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

#include <Geom/Mat2d.h>
#include <Geom/XY.h>

namespace Geom
{
class Ax2d;
class Pnt2d;
class Vec2d;

//! Defines a non-persistent transformation in 2D space. <br>
//! The following transformations are implemented : <br>
//! . Translation, Rotation, Scale <br>
//! . Symmetry with respect to a point and a line. <br>
//! Complex transformations can be obtained by combining the <br>
//! previous elementary transformations using the method Multiply. <br>
//! The transformations can be represented as follow : <br>
//! <br>
//! V1 V2 T XY XY <br>
//! | a11 a12 a13 | | x | | x'| <br>
//! | a21 a22 a23 | | y | | y'| <br>
//! | 0 0 1 | | 1 | | 1 | <br>

class LX_GEOM_EXPORT Trsf2d
{
public:
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

    //! Returns identity transformation. <br>
    Trsf2d();
    //! Creates a 2d transformation in the XY plane from a <br>
    //! 3d transformation . <br>
    Trsf2d(const Trsf2d& T);

    //! Returns the nature of the transformation. It can be an <br>
    //! identity transformation, a rotation, a translation, a mirror <br>
    //! (relative to a point or an axis), a scaling transformation, <br>
    //! or a compound transformation. <br>
    Trsf2d::FormEnum form() const;
    //! Returns the homogeneous vectorial part of the transformation. <br>
    //! It is a 2*2 matrix which doesn't include the scale factor. <br>
    //! The coefficients of this matrix must be multiplied by the <br>
    //! scale factor to obtain the coefficients of the transformation. <br>
    const Mat2d& hVectorialPart() const;

    void invert();

    //! Computes the reverse transformation. <br>
    //! Raises an exception if the matrix of the transformation <br>
    //! is not inversible, it means that the scale factor is lower <br>
    //! or equal to Resolution from package gp. <br>
    Trsf2d inverted() const;

    //! Returns true if the determinant of the vectorial part of <br>
    //! this transformation is negative.. <br>
    bool isNegative() const;

    Trsf2d multiplied(const Trsf2d& T) const;
    //! Computes the transformation composed from <T> and <me>. <br>
    //! In a C++ implementation you can also write Tcomposed = <me> * T. <br>
    //! Example : <br>
    //! Trsf2d T1, T2, Tcomp; ............... <br>
    //! //composition : <br>
    //! Tcomp = T2.Multiplied(T1); // or (Tcomp = T2 * T1) <br>
    //! // transformation of a point <br>
    //! Pnt2d P1(10.,3.,4.); <br>
    //! Pnt2d P2 = P1.Transformed(Tcomp); //using Tcomp <br>
    //! Pnt2d P3 = P1.Transformed(T1); //using T1 then T2 <br>
    //! P3.Transform(T2); // P3 = P2 !!! <br>
    void multiply(const Trsf2d& T);
    Trsf2d operator*(const Trsf2d& T) const { return multiplied(T); }

    void operator*=(const Trsf2d& T) { multiply(T); }

    void power(const int N);

    //! Computes the following composition of transformations <br>
    //! <me> * <me> * .......* <me>, N time. <br>
    //! if N = 0 <me> = Identity <br>
    //! if N < 0 <me> = <me>.Inverse() *...........* <me>.Inverse(). <br>
    Trsf2d powered(const int N);

    //! Computes the transformation composed from <me> and T. <br>
    //! <me> = T * <me> <br>
    void preMultiply(const Trsf2d& T);

    //! Returns the angle corresponding to the rotational component <br>
    //! of the transformation matrix (operation opposite to SetRotation()). <br>
    double rotationPart() const;

    //! Returns the scale factor. <br>
    double scaleFactor() const;

    //! Changes the transformation into a symmetrical transformation. <br>
    //! P is the center of the symmetry. <br>
    void setMirror(const Pnt2d& P);

    //! Changes the transformation into a symmetrical transformation. <br>
    //! A is the center of the axial symmetry. <br>
    void setMirror(const Ax2d& A);

    //! Changes the transformation into a rotation. <br>
    //! P is the rotation's center and Ang is the angular value of the <br>
    //! rotation in radian. <br>
    void setRotation(const Pnt2d& P, const double Ang);

    //! Changes the transformation into a scale. <br>
    //! P is the center of the scale and S is the scaling value. <br>
    void setScale(const Pnt2d& P, const double S);

    //! Modifies the scale factor. <br>
    void setScaleFactor(const double S);
    //! Changes a transformation allowing passage from the coordinate <br>
    //! system "FromSystem1" to the coordinate system "ToSystem2". <br>
    void setTransformation(const Ax2d& FromSystem1, const Ax2d& ToSystem2);

    //! Changes the transformation allowing passage from the basic <br>
    //! coordinate system <br>
    //! {P(0.,0.,0.), VX (1.,0.,0.), VY (0.,1.,0.)} <br>
    //! to the local coordinate system defined with the Ax2d ToSystem. <br>
    void setTransformation(const Ax2d& ToSystem);

    //! Changes the transformation into a translation. <br>
    //! V is the vector of the translation. <br>
    void setTranslation(const Vec2d& V);

    //! Makes the transformation into a translation from <br>
    //! the point P1 to the point P2. <br>
    void setTranslation(const Pnt2d& P1, const Pnt2d& P2);
    //! Replaces the translation vector with V. <br>
    void setTranslationPart(const Vec2d& V);
    void transforms(double& X, double& Y) const;
    //! Transforms a doublet XY with a Trsf2d <br>
    void transforms(XY& Coord) const;

    //! Returns the translation part of the transformation's matrix <br>
    const XY& translationPart() const;

    //! Returns the coefficients of the transformation's matrix. <br>
    //! It is a 2 rows * 3 columns matrix. <br>
    //! Raises OutOfRange if Row < 1 or Row > 2 or Col < 1 or Col > 3 <br>
    double value(const int Row, const int Col) const;

    //! Returns the vectorial part of the transformation. It is a <br>
    //! 2*2 matrix which includes the scale factor. <br>
    Mat2d vectorialPart() const;

    friend class GTrsf2d;

protected:
private:
    Geom::XY _loc;
    Mat2d _matrix;
    double _scale;
    Trsf2d::FormEnum _shape;
};
}  // namespace Geom