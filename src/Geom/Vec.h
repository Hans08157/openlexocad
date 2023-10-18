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
#include <Geom/XYZ.h>
#include <QString> 

namespace Geom
{
class Ax1;
class Ax2;
class Trsf;
class Dir;
class Pnt;
class Vec;

}  // namespace Geom

namespace Geom
{
//!  Defines a non-persistent vector in 3D space. <br>
class LX_GEOM_EXPORT Vec
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
    //! Creates an indefinite vector. <br>
    Vec();
    //! Creates a unitary vector from a direction V. <br>
    Vec(const Geom::Dir& V);
    //! Creates a vector with a triplet of coordinates. <br>
    Vec(const Geom::XYZ& Coord);
    //! Creates a point with its three Cartesian coordinates. <br>
    Vec(const double Xv, const double Yv, const double Zv);

    //!  Creates a vector from two points. The length of the vector <br>
    //!  is the distance between P1 and P2 <br>
    Vec(const Geom::Pnt& P1, const Geom::Pnt& P2);

    //! Copy constructor
    Vec(const Vec& rhs);

    //! Changes the coordinate of range Index <br>
    //!  Index = 1 => X is modified <br>
    //!  Index = 2 => Y is modified <br>
    //!  Index = 3 => Z is modified <br>//! Raised if Index != {1, 2, 3}. <br>
    void setCoord(const int Index, const double Xi);
    //! For this vector, assigns <br>
    //! -   the values Xv, Yv and Zv to its three coordinates. <br>
    void setCoord(const double Xv, const double Yv, const double Zv);
    //! Assigns the given value to the X coordinate of this vector. <br>
    void setX(const double X);
    //! Assigns the given value to the X coordinate of this vector. <br>
    void setY(const double Y);
    //! Assigns the given value to the X coordinate of this vector. <br>
    void setZ(const double Z);
    //! Assigns the three coordinates of Coord to this vector. <br>
    void setXYZ(const Geom::XYZ& Coord);

    //!  Returns the coordinate of range Index : <br>
    //!  Index = 1 => X is returned <br>
    //!  Index = 2 => Y is returned <br>
    //!  Index = 3 => Z is returned <br>//! Raised if Index != {1, 2, 3}. <br>
    double coord(const int Index) const;
    //! For this vector returns its three coordinates Xv, Yv, and Zvinline <br>
    void coord(double& Xv, double& Yv, double& Zv) const;
    //! For this vector, returns its X coordinate. <br>
    double x() const;
    //! For this vector, returns its Y coordinate. <br>
    double y() const;
    //! For this vector, returns its Z  coordinate. <br>
    double z() const;
    //!    For this vector, returns <br>
    //! -   its three coordinates as a number triple <br>
    const Geom::XYZ& xyz() const;

    float fx() const;
    float fy() const;
    float fz() const;


    //!  Returns True if the two vectors have the same magnitude value <br>
    //!  and the same direction. The precision values are LinearTolerance <br>
    //!  for the magnitude and AngularTolerance for the direction. <br>
    bool isEqual(const Vec& Other, const double LinearTolerance, const double AngularTolerance) const;

    //!  Returns True if abs(<me>.Angle(Other) - PI/2.) <= AngularTolerance <br>
    //!   Raises VectorWithNullMagnitude if <me>.Magnitude() <= Resolution or <br>
    //!  Other.Magnitude() <= Resolution from gp <br>
    bool isNormal(const Vec& Other, const double AngularTolerance) const;

    //!  Returns True if PI - <me>.Angle(Other) <= AngularTolerance <br>
    //!  Raises VectorWithNullMagnitude if <me>.Magnitude() <= Resolution or <br>
    //!  Other.Magnitude() <= Resolution from gp <br>
    bool isOpposite(const Vec& Other, const double AngularTolerance) const;

    //!  Returns True if Angle(<me>, Other) <= AngularTolerance or <br>
    //!  PI - Angle(<me>, Other) <= AngularTolerance <br>
    //!  This definition means that two parallel vectors cannot define <br>
    //!  a plane but two vectors with opposite directions are considered <br>
    //!  as parallel. Raises VectorWithNullMagnitude if <me>.Magnitude() <= Resolution or <br>
    //!  Other.Magnitude() <= Resolution from gp <br>
    bool isParallel(const Vec& Other, const double AngularTolerance) const;

    //!  Computes the angular value between <me> and <Other> <br>
    //!  Returns the angle value between 0 and PI in radian. <br>
    //!    Raises VectorWithNullMagnitude if <me>.Magnitude() <= Resolution from gp or <br>
    //!  Other.Magnitude() <= Resolution because the angular value is <br>
    //!  indefinite if one of the vectors has a null magnitude. <br>
    double angle(const Vec& Other) const;
    //! Computes the angle, in radians, between this vector and <br>
    //! vector Other. The result is a value between -Pi and Pi. <br>
    //! For this, VRef defines the positive sense of rotation: the <br>
    //! angular value is positive, if the cross product this ^ Other <br>
    //! has the same orientation as VRef relative to the plane <br>
    //! defined by the vectors this and Other. Otherwise, the <br>
    //! angular value is negative. <br>
    //! Exceptions <br>
    //! gp_VectorWithNullMagnitude if the magnitude of this <br>
    //! vector, the vector Other, or the vector VRef is less than or <br>
    //! equal to Geom::Precision::linear_Resolution(). <br>
    //! Standard_DomainError if this vector, the vector Other, <br>
    //! and the vector VRef are coplanar, unless this vector and <br>
    //! the vector Other are parallel. <br>
    double angleWithRef(const Vec& Other, const Vec& VRef) const;
    //! Computes the magnitude of this vector. <br>
    double magnitude() const;
    //! Computes the square magnitude of this vector. <br>//! Adds two vectors <br>
    double squareMagnitude() const;

    void add(const Vec& Other);
    void operator+=(const Vec& Other) { add(Other); }

    //! Adds two vectors <br>//! Subtracts two vectors <br>
    Vec added(const Vec& Other) const;
    Vec operator+(const Vec& Other) const { return added(Other); }


    void subtract(const Vec& Right);
    void operator-=(const Vec& Right) { subtract(Right); }

    //! Subtracts two vectors <br>//! Multiplies a vector by a scalar <br>
    Vec subtracted(const Vec& Right) const;
    Vec operator-(const Vec& Right) const { return subtracted(Right); }


    void multiply(const double Scalar);
    void operator*=(const double Scalar) { multiply(Scalar); }

    //! Multiplies a vector by a scalar <br>//! Divides a vector by a scalar <br>
    Vec multiplied(const double Scalar) const;
    Vec operator*(const double Scalar) const { return multiplied(Scalar); }


    void divide(const double Scalar);
    void operator/=(const double Scalar) { divide(Scalar); }

    //! Divides a vector by a scalar <br>//! computes the cross product between two vectors <br>
    Vec divided(const double Scalar) const;
    Vec operator/(const double Scalar) const { return divided(Scalar); }


    void cross(const Vec& Right);
    void operator^=(const Vec& Right) { cross(Right); }

    //! computes the cross product between two vectors <br>
    Vec crossed(const Vec& Right) const;
    Vec operator^(const Vec& Right) const { return crossed(Right); }


    //!  Computes the magnitude of the cross <br>
    //!  product between <me> and Right. <br>
    //!  Returns || <me> ^ Right || <br>
    double crossMagnitude(const Vec& Right) const;

    //!  Computes the square magnitude of <br>
    //!  the cross product between <me> and Right. <br>
    //!  Returns || <me> ^ Right ||**2 <br>//! Computes the triple vector product. <br>
    //!  <me> ^ (V1 ^ V2) <br>
    double crossSquareMagnitude(const Vec& Right) const;

    void crossCross(const Vec& V1, const Vec& V2);
    //! Computes the triple vector product. <br>
    //!  <me> ^ (V1 ^ V2) <br>
    Vec crossCrossed(const Vec& V1, const Vec& V2) const;
    //! computes the scalar product <br>
    double dot(const Vec& Other) const;
    double operator*(const Vec& Other) const { return dot(Other); }

    //! Computes the triple scalar product <me> * (V1 ^ V2). <br>//! normalizes a vector <br>
    //!  Raises an exception if the magnitude of the vector is <br>
    //!  lower or equal to Resolution from gp. <br>
    double dotCross(const Vec& V1, const Vec& V2) const;

    void normalize();
    //! normalizes a vector <br>
    //!  Raises an exception if the magnitude of the vector is <br>
    //!  lower or equal to Resolution from gp. <br>//! Reverses the direction of a vector <br>
    Vec normalized() const;

    void reverse();
    //! Reverses the direction of a vector <br>
    Vec reversed() const;
    Vec operator-() const { return reversed(); }
    Vec operator &  (const Vec& rcVct) const;


    //!  <me> is setted to the following linear form : <br>
    //!  A1 * V1 + A2 * V2 + A3 * V3 + V4 <br>
    void setLinearForm(const double A1, const Vec& V1, const double A2, const Vec& V2, const double A3, const Vec& V3, const Vec& V4);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * V1 + A2 * V2 + A3 * V3 <br>
    void setLinearForm(const double A1, const Vec& V1, const double A2, const Vec& V2, const double A3, const Vec& V3);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * V1 + A2 * V2 + V3 <br>
    void setLinearForm(const double A1, const Vec& V1, const double A2, const Vec& V2, const Vec& V3);

    //!  <me> is setted to the following linear form : <br>
    //!  A1 * V1 + A2 * V2 <br>
    void setLinearForm(const double A1, const Vec& V1, const double A2, const Vec& V2);

    //!  <me> is setted to the following linear form : A1 * V1 + V2 <br>
    void setLinearForm(const double A1, const Vec& V1, const Vec& V2);

    //!  <me> is setted to the following linear form : V1 + V2 <br>
    void setLinearForm(const Vec& V1, const Vec& V2);


    void mirror(const Vec& V);


    //!  Performs the symmetrical transformation of a vector <br>
    //!  with respect to the vector V which is the center of <br>
    //!  the  symmetry. <br>
    Vec mirrored(const Vec& V) const;


    void mirror(const Geom::Ax1& A1);


    //!  Performs the symmetrical transformation of a vector <br>
    //!  with respect to an axis placement which is the axis <br>
    //!  of the symmetry. <br>
    Vec mirrored(const Geom::Ax1& A1) const;


    void mirror(const Geom::Ax2& A2);


    //!  Performs the symmetrical transformation of a vector <br>
    //!  with respect to a plane. The axis placement A2 locates <br>
    //!  the plane of the symmetry : (Location, XDirection, YDirection). <br>
    Vec mirrored(const Geom::Ax2& A2) const;

    void rotate(const Geom::Ax1& A1, const double Ang);

    //!  Rotates a vector. A1 is the axis of the rotation. <br>
    //!  Ang is the angular value of the rotation in radians. <br>
    Vec rotated(const Geom::Ax1& A1, const double Ang) const;

    void scale(const double S);
    //! Scales a vector. S is the scaling value. <br>//! Transforms a vector with the transformation T. <br>
    Vec scaled(const double S) const;


    void transform(const Geom::Trsf& T);
    //! Transforms a vector with the transformation T. <br>
    Vec transformed(const Geom::Trsf& T) const;
    /// Projects this point onto the line given by the base \a rclPoint and the direction \a rclLine.
    /**
     * Projects a point \a rclPoint onto the line defined by the origin and the direction \a rclLine.
     * The result is a vector from \a rclPoint to the point on the line. The length of this vector
     * is the distance from \a rclPoint to the line.
     * Note: The resulting vector does not depend on the current vector.
     */
    Geom::Vec& projectToLine(const Geom::Vec& rclPoint, const Geom::Vec& rclLine);

    /**
     * Get the perpendicular of this point to the line defined by rclBase and rclDir.
     * Note: Do not mix up this method with ProjectToLine.
     */
    Geom::Vec perpendicular(const Geom::Vec& rclBase, const Geom::Vec& rclDir) const;

    /** Computes the distance to the given plane. Depending on the side this point is located
     * the distance can also be negative. The distance is positive if the point is at the same
     * side the plane normal points to, negative otherwise.
     */
    double distanceToPlane(const Geom::Vec& rclBase, const Geom::Vec& rclNorm) const;
    /// Computes the distance from this point to the line given by \a rclBase and \a rclDirect.
    double distanceToLine(const Geom::Vec& rclBase, const Geom::Vec& rclDirect) const;
    /** Computes the vector from this point to the point on the line segment with the shortest
     * distance. The line segment is defined by \a rclP1 and \a rclP2.
     * Note: If the projection of this point is outside the segment then the shortest distance
     * to \a rclP1 or \a rclP2 is computed.
     */
    Geom::Vec distanceToLineSegment(const Geom::Vec& rclP1, const Geom::Vec& rclP2) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    double& operator[](int i);

private:
    Geom::XYZ _coord;
};

// global functions

/// Returns the distance between two points
inline double distance(const Geom::Vec& v1, const Geom::Vec& v2)
{
    double x = v1.x() - v2.x(), y = v1.y() - v2.y(), z = v1.z() - v2.z();
    return static_cast<double>(sqrt((x * x) + (y * y) + (z * z)));
}

/// Returns the squared distance between two points
inline double distanceP2(const Geom::Vec& v1, const Geom::Vec& v2)
{
    double x = v1.x() - v2.x(), y = v1.y() - v2.y(), z = v1.z() - v2.z();
    return x * x + y * y + z * z;
}

LX_GEOM_EXPORT QString to_string(const Vec& vec);
}  // namespace Geom

inline Geom::Vec operator*(const double Scalar, const Geom::Vec& V)
{
    return V.multiplied(Scalar);
}
