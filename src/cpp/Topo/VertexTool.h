#pragma once

#include <Topo/Types.h>

namespace Geom
{
class Trsf;
class Pnt;
}

namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Vertices.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT VertexTool
{
public:
    VertexTool() {}
    ~VertexTool() {}

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Makes a Vertex from a point.
    static pVertex makeVertex(const Geom::Pnt& p);
    /// Creates a copy of the vertex and transforms the copy
    static pVertex transformed(pConstVertex base, const Geom::Trsf& t);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
               /// @cond INTERNAL

    /// Sets the default VertexTool. For internal use only.
    static void __setDefaultVertexTool__(Topo::VertexTool* tool) { _defaultTool = tool; }

protected:
    virtual pVertex _makeVertex(const Geom::Pnt& p);
    static Topo::VertexTool* _defaultTool;
    /// @endcond
#endif
};

}  // namespace Topo