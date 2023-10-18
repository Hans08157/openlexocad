/***************************************************************************
 *   Copyright (c) 2019 Abdullah Tahiri <abdullah.tahiri.yo@gmail.com>     *
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

#include <Base/Base.h>
#include <memory>

namespace Base
{
class PersistenceVersion;
class AbstractWriter;
class AbstractXMLReader;
}

namespace Geom {

    class Geometry;
    class LX_GEOM_EXPORT GeometryExtension : public Base::BaseClass
{
    TYPESYSTEM_HEADER();

public:
    virtual ~GeometryExtension() = default;

    virtual std::unique_ptr<GeometryExtension> copy(void) const = 0;

    inline void setName(const std::string& str) { name = str; }
    inline const std::string& getName() const { return name; }

    // Default method to notify an extension that it has been attached
    // to a given geometry
    virtual void notifyAttachment(Geom::Geometry*) {}

protected:
    GeometryExtension();
    GeometryExtension(const GeometryExtension& obj) = default;
    GeometryExtension& operator=(const GeometryExtension& obj) = default;

    virtual void copyAttributes(Geom::GeometryExtension* cpy) const;

private:
    std::string name;
};



class LX_GEOM_EXPORT GeometryPersistenceExtension : public Geom::GeometryExtension
{
    TYPESYSTEM_HEADER();

public:
    virtual ~GeometryPersistenceExtension() = default;

    // Own Persistence implementer - Not Base::Persistence - managed by Geom::Geometry
    virtual void save(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/);
    virtual void restore(Base::AbstractXMLReader& /*reader*/, Base::PersistenceVersion& /*version*/);

protected:
    virtual void restoreAttributes(Base::AbstractXMLReader& /*reader*/);
    virtual void saveAttributes(Base::AbstractWriter& /*writer*/) const;
};
}

