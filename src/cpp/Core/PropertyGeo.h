/***************************************************************************
 *   Copyright (c) 2002 Jürgen Riegel <juergen.riegel@web.de>              *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/

#pragma once

#include <Base/BoundBox.h>
#include <Core/Property.h>

namespace Data {
class ComplexGeoData;
}

namespace Core
{


/** The base class for all basic geometry properties.
 * @author Werner Mayer
 */
class LX_CORE_EXPORT PropertyFcGeometry : public Property
{
    TYPESYSTEM_HEADER();

public:
    /** @name Modification */
    //@{
    /// Applies a transformation on the real geometric data type
    virtual void transformGeometry(const Base::Matrix4D &rclMat) = 0;
    /// Retrieve bounding box information
    virtual Base::BoundBox3d getBoundingBox() const = 0;
    //@}
};

/** The base class for all complex data properties.
 * @author Werner Mayer
 */
class LX_CORE_EXPORT PropertyFcComplexGeoData : public PropertyFcGeometry
{
    TYPESYSTEM_HEADER();

public:
    /** @name Modification */
    //@{
    /// Applies a transformation on the real geometric data type
    virtual void transformGeometry(const Base::Matrix4D &rclMat) = 0;
    //@}

    /** @name Getting basic geometric entities */
    //@{
    virtual const Data::ComplexGeoData* getComplexData() const = 0;
    virtual Base::BoundBox3d getBoundingBox() const = 0;
    //@}
};

} // namespace Core


