#pragma once

#include <Topo/Types.h>

namespace Topo
{
class VisibleEdge
{
public:
    enum class VisibleEdgeInfo
    {
        EDGE_VIS,         // visible segment
        EDGE_HID,         // hidden segment
        EDGE_OCC,         // occluded segment
        EDGE_UND,         // undefined visibility
        EDGE_VIS_SMOOTH,  // smooth but calculated as visible
        EDGE_HID_SMOOTH   // smooth but calculated as hidden
    };

    VisibleEdge(pConstEdge e, pConstShape s_shape, VisibleEdgeInfo vis) : edge(e), source_shape(s_shape), visibility(vis){};

    pConstEdge getEdge() const { return edge; };
    pConstShape getSourceShape() const { return source_shape; };
    VisibleEdgeInfo getVisibility() const { return visibility; };

private:
    pConstEdge edge;
    VisibleEdgeInfo visibility;
    pConstShape source_shape;
};
}  // namespace Topo