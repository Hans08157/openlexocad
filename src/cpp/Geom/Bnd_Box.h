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



namespace Geom
{
class Pnt;
class Dir;
class Trsf;
class Lin;
class Pln;
class Vec;
}  // namespace Geom


namespace Geom
{
//! Describes a bounding box in 3D space. <br>
//! A bounding box is parallel to the axes of the coordinates <br>
//! system. If it is finite, it is defined by the three intervals: <br>
//! -   [ Xmin,Xmax ], <br>
//! -   [ Ymin,Ymax ], <br>
//! -   [ Zmin,Zmax ]. <br>
//! A bounding box may be infinite (i.e. open) in one or more <br>
//! directions. It is said to be: <br>
//! -   OpenXmin if it is infinite on the negative side of the   "X Direction"; <br>
//! -   OpenXmax if it is infinite on the positive side of the "X Direction"; <br>
//! -   OpenYmin if it is infinite on the negative side of the   "Y Direction"; <br>
//! -   OpenYmax if it is infinite on the positive side of the "Y Direction"; <br>
//! -   OpenZmin if it is infinite on the negative side of the   "Z Direction"; <br>
//! -   OpenZmax if it is infinite on the positive side of the "Z Direction"; <br>
//! -   WholeSpace if it is infinite in all six directions. In this <br>
//!   case, any point of the space is inside the box; <br>
//! -   Void if it is empty. In this case, there is no point included in the box. <br>
//!   A bounding box is defined by: <br>
//! -   six bounds (Xmin, Xmax, Ymin, Ymax, Zmin and <br>
//!   Zmax) which limit the bounding box if it is finite, <br>
//! -   eight flags (OpenXmin, OpenXmax, OpenYmin, <br>
//!   OpenYmax, OpenZmin, OpenZmax, <br>
//!   WholeSpace and Void) which describe the <br>
//!   bounding box if it is infinite or empty, and <br>
//! -   a gap, which is included on both sides in any direction <br>
//!   when consulting the finite bounds of the box. <br>
class LX_GEOM_EXPORT Bnd_Box
{
public:
    //! Creates an empty Box. <br>
    //! The constructed box is qualified Void. Its gap is null. <br>
    Bnd_Box();
    Bnd_Box(const Geom::Pnt& min, const Geom::Pnt& max);
    //! Sets this bounding box so that it  covers the whole of 3D space. <br>
    //!        It is infinitely  long in all directions. <br>
    void SetWhole();
    //! Sets this bounding box so that it is empty. All points are outside a void box. <br>
    void SetVoid();
    //! Sets this bounding box so that it bounds <br>
    //! -   the point P. This involves first setting this bounding box <br>
    //!   to be void and then adding the point P. <br>
    void Set(const Geom::Pnt& P);
    //! Sets this bounding box so that it bounds <br>
    //!   the half-line defined by point P and direction D, i.e. all <br>
    //!   points M defined by M=P+u*D, where u is greater than <br>
    //!   or equal to 0, are inside the bounding volume. This <br>
    //!   involves first setting this box to be void and then adding   the half-line. <br>
    void Set(const Geom::Pnt& P, const Geom::Dir& D);
    //! Enlarges this bounding box, if required, so that it <br>
    //!          contains at least: <br>
    //!   -   interval [ aXmin,aXmax ] in the "X Direction", <br>
    //!   -   interval [ aYmin,aYmax ] in the "Y Direction", <br>
    //!   -   interval [ aZmin,aZmax ] in the "Z Direction"; <br>
    void Update(const double aXmin, const double aYmin, const double aZmin, const double aXmax, const double aYmax, const double aZmax);
    //!  Adds a point of coordinates (X,Y,Z) to this bounding box. <br>
    void Update(const double X, const double Y, const double Z);
    //! Returns the gap of this bounding box. <br>
    // Standard_EXPORT     double GetGap() const;
    //! Set the gap of this bounding box to abs(Tol). <br>
    void SetGap(const double Tol);
    //! Enlarges the      box    with    a   tolerance   value. <br>
    //!          (minvalues-abs(<tol>) and maxvalues+abs(<tol>)) <br>
    //!	This means that the minimum values of its X, Y and Z <br>
    //! intervals of definition, when they are finite, are reduced by <br>
    //! the absolute value of Tol, while the maximum values are <br>
    //! increased by the same amount. <br>
    void Enlarge(const double Tol);
    //! Returns the bounds of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    void Get(double& aXmin, double& aYmin, double& aZmin, double& aXmax, double& aYmax, double& aZmax) const;

    //! Returns the X min of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetXmin() const;
    //! Returns the Y min of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetYmin() const;
    //! Returns the Z min of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetZmin() const;
    //! Returns the X max of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetXmax() const;
    //! Returns the Y max of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetYmax() const;
    //! Returns the Z max of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetZmax() const;

    //! Returns the X size of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetXsize() const;
    //! Returns the Y size of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetYsize() const;
    //! Returns the Z size of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const double GetZsize() const;

    //! Returns the min bound of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned value <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const Geom::Pnt GetMin() const;
    //! Returns the max bound of this bounding box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned value <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const Geom::Pnt GetMax() const;
    //! Returns corner points of the box. The gap is included. <br>
    //! If this bounding box is infinite (i.e. "open"), returned values <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    std::vector<Geom::Pnt> GetCornerPoints() const;
    //! Returns the center of this bounding box. <br>
    //! If this bounding box is infinite (i.e. "open"), returned value <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    const Geom::Pnt GetCenter() const;
    //! Returns the size of this bounding box. The gap is included.<br>
    //! If this bounding box is infinite (i.e. "open"), returned value <br>
    //! may be equal to +/- Precision::Infinite(). <br>
    //! if IsVoid() <br>
    void GetSize(double& length, double& width, double& height) const;
    //! The   Box will be   infinitely   long  in the Xmin <br>
    //!          direction. <br>
    void OpenXmin();
    //! The   Box will be   infinitely   long  in the Xmax <br>
    //!          direction. <br>
    void OpenXmax();
    //! The   Box will be   infinitely   long  in the Ymin <br>
    //!          direction. <br>
    void OpenYmin();
    //! The   Box will be   infinitely   long  in the Ymax <br>
    //!          direction. <br>
    void OpenYmax();
    //! The   Box will be   infinitely   long  in the Zmin <br>
    //!          direction. <br>
    void OpenZmin();
    //! The   Box will be   infinitely   long  in the Zmax <br>
    //!          direction. <br>
    void OpenZmax();
    //! Returns true if this bounding box is open in the  Xmin direction. <br>
    unsigned int IsOpenXmin() const;
    //! Returns true if this bounding box is open in the  Xmax direction. <br>
    unsigned int IsOpenXmax() const;
    //! Returns true if this bounding box is open in the  Ymix direction. <br>
    unsigned int IsOpenYmin() const;
    //! Returns true if this bounding box is open in the  Ymax direction. <br>
    unsigned int IsOpenYmax() const;
    //! Returns true if this bounding box is open in the  Zmin direction. <br>
    unsigned int IsOpenZmin() const;
    //! Returns true if this bounding box is open in the  Zmax  direction. <br>
    unsigned int IsOpenZmax() const;
    //! Returns true if this bounding box is infinite in all 6 directions (WholeSpace flag). <br>
    unsigned int IsWhole() const;
    //! Returns true if this bounding box is empty (Void flag). <br>
    unsigned int IsVoid() const;
    //! true if xmax-xmin < tol. <br>
    // Standard_EXPORT     bool IsXThin(const double tol) const;
    //! true if ymax-ymin < tol. <br>
    // Standard_EXPORT     bool IsYThin(const double tol) const;
    //! true if zmax-zmin < tol. <br>
    // Standard_EXPORT     bool IsZThin(const double tol) const;
    //! Returns true if IsXThin, IsYThin and IsZThin are all true, <br>
    //! i.e. if the box is thin in all three dimensions. <br>
    // Standard_EXPORT     bool IsThin(const double tol) const;
    //! Returns a bounding box which is the result of applying the <br>
    //! transformation T to this bounding box. <br>
    //! Warning <br>
    //! Applying a geometric transformation (for example, a <br>
    //! rotation) to a bounding box generally increases its <br>
    //! dimensions. This is not optimal for algorithms which use it. <br>
    Geom::Bnd_Box Transformed(const Geom::Trsf& T) const;
    //! Adds the box <Other> to <me>. <br>
    void Add(const Bnd_Box& Other);
    //! Adds a Pnt to the box. <br>
    void Add(const Geom::Pnt& P);
    //! Extends  <me> from the Pnt <P> in the direction <D>. <br>
    void Add(const Geom::Pnt& P, const Geom::Dir& D);
    //! Extends the Box  in the given Direction, i.e. adds <br>
    //!          an  half-line. The   box  may become   infinite in <br>
    //!          1,2 or 3 directions. <br>
    void Add(const Geom::Dir& D);
    //! Returns True if the Pnt is out the box. <br>
    unsigned int IsOut(const Geom::Pnt& P) const;
    //! Returns False if the line intersects the box. <br>
    unsigned int IsOut(const Geom::Lin& L) const;
    //! Returns False if the plane intersects the box. <br>
    unsigned int IsOut(const Geom::Pln& P) const;
    //! Returns False if the <Box> intersects or is inside <me>. <br>
    unsigned int IsOut(const Geom::Bnd_Box& Other) const;
    //! Returns False if  the transformed <Box> intersects <br>
    //!          or  is inside <me>. <br>
    unsigned int IsOut(const Geom::Bnd_Box& Other, const Geom::Trsf& T) const;
    //! Returns False  if the transformed <Box> intersects <br>
    //!          or  is inside the transformed box <me>. <br>
    unsigned int IsOut(const Geom::Trsf& T1, const Geom::Bnd_Box& Other, const Geom::Trsf& T2) const;
    //! Returns False  if the flat band lying between two parallel <br>
    //!    	    lines represented by their reference points <P1>, <P2> and <br>
    //!          direction <D> intersects the box. <br>
    unsigned int IsOut(const Geom::Pnt& P1, const Geom::Pnt& P2, const Geom::Dir& D) const;
    //! Computes the minimum distance between two boxes. <br>
    // Standard_EXPORT     double Distance(const Bnd_Box& Other) const;

    // Standard_EXPORT     void Dump() const;
    //! Computes the squared diagonal of me. <br>
    // double SquareExtent() const;


    // Return difference between min point of two bounding boxes
    Geom::Vec GetMinDifference(const Geom::Bnd_Box& Other) const;

protected:
private:
    double Xmin;
    double Xmax;
    double Ymin;
    double Ymax;
    double Zmin;
    double Zmax;
    double Gap;
    unsigned int Flags;
};

}  // namespace Geom
