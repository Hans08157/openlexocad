#pragma once

#include <Geom/Bnd_Box.h>
#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Globals.h>

namespace App
{
class Geometry;
}

namespace OpenLxApp
{
class Document;


/**
 * @brief Super-class of all Geometries (aka GeometricRepresentationItems)
 *
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT Geometry : public DocObject
{
    PROXY_HEADER_ABSTRACT(Geometry, App::Geometry, IFCGEOMETRICREPRESENTATIONITEM)

public:
    virtual ~Geometry(void);

    pShape computeShape(bool checkShape = false);
    pConstShape getShape(void) const;
    double getPrecision() const;
    void setPrecision(double p);
    Geom::Bnd_Box getBoundingBox() const;

protected:
    Geometry() = default;
};

}  // namespace OpenLxApp
