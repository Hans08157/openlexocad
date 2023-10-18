#pragma once

#include <Core/CdwkAttributeData.h>

class BODY;

namespace Topo
{
class LX_TOPO_EXPORT ShapeAttributes
{
public:
    ShapeAttributes() = default;
    virtual Topo::ShapeAttributes* getCopy() const = 0;
};


/* @brief: This class is needed and used to attach attributes to a shape. This is p.e. the case when
           importing SAT files which have user defined attributes attached to an ENTITY. */
class LX_TOPO_EXPORT Cdwk_SAT_Attributes : public Topo::ShapeAttributes
{
public:
    Cdwk_SAT_Attributes() = default;

    Topo::ShapeAttributes* getCopy() const;

    Core::CdwkAttributeData attribute;
    BODY* shapeBody;  // The BODY this shape attribute belongs to
    std::vector<BODY*> openings;
};
}  // namespace Topo
