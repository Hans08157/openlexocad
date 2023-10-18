#pragma once
#include <Topo/Types.h>
#include <Geom/Precision.h>
#include <vector>

namespace Geom
{
class Pln;
class Pnt;
class Dir;
class Trsf;
}

namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Wires.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT WireTool
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Projects a wire onto a plane (projection along Plane normal). Returns the new projected wire.
    static pWire projectWireOnPlane(const Geom::Pln& pln, pConstWire wire, double precision = Geom::Precision::linear_Resolution());
    /// Projects a wire onto a plane (projection along given Direction). Returns the new projected wire.
    static pWire projectWireOnPlane(pConstWire wire, const Geom::Dir& dir, const Geom::Pln& pln);
    /// Projects point 'p' on 'wire'. Returns the nearest solution point.
    static bool projectPointOnWire(const Geom::Pnt& p, pConstWire wire, Geom::Pnt& nearest);
    /// Projects point 'p' on 'wire'. Returns the nearest solution point and the reference (up)  direction at that point
    static bool projectPointOnWire(const Geom::Pnt& p, pConstWire wire, Geom::Pnt& nearest, Geom::Dir& refDirection);
    /// Checks if the wire is planar
    static bool isPlanar(pConstWire wire, Geom::Pln& plane);
    /// Checks if the wire is closed
    static bool isClosed(pConstWire wire);
    /// Closes the wire
    static bool close(pWire wire, double precision = Geom::Precision::linear_Resolution());
    /// Returns the closed wire
    static pWire closed(pConstWire wire, double precision = Geom::Precision::linear_Resolution());
    /// Adds an edge to the wire
    static bool addEdge(pWire wire, pEdge edge, double precision = Geom::Precision::linear_Resolution());
    /// Adds a vector of edges to a wire
    static bool addEdge(pWire wire, const std::vector<pEdge>& edges, double precision = Geom::Precision::linear_Resolution());
    /// Takes a const edge and copies it. The copy is added to the wire.
    static bool addConstEdge(pWire wire, pConstEdge edge, double precision = Geom::Precision::linear_Resolution());
    /// Takes a vector of const edges and copies them. The copies are added to the wire.
    static bool addConstEdge(pWire wire, const std::vector<pEdge>& edges, double precision = Geom::Precision::linear_Resolution());
    /// Returns the new wire with the added edge
    static pWire addedEdge(pConstWire wire, pConstEdge edge, double precision = Geom::Precision::linear_Resolution());
    /// Returns the new wire with the added edges
    static pWire addedEdge(pConstWire wire, const std::vector<pConstEdge>& edges, double precision = Geom::Precision::linear_Resolution());
    /// Returns the closest vertex from a point on a wire. Returns nullptr on failure.
    static pConstVertex getClosestVertexToPoint(const Geom::Pnt& p, pConstWire wire);
    /// Returns the closest edges from a point on a wire.
    static std::vector<pConstEdge> getClosestEdgesToPoint(const Geom::Pnt& p, pConstWire wire, double& distance, double tolerance = 1E-06);
    /// Returns the adjacent edges from a vertex on a wire.
    static std::vector<pConstEdge> getAdjacentEdgesToVertexOnWire(pConstVertex vertex, pConstWire wire);
    /// Get the adjacent edges from a point on a wire.
    static void getAdjacentEdgesToPointOnWire(const Geom::Pnt& point, pConstWire wire, std::vector<pConstEdge>& adjacentEdges);
    /// Makes a wire from edges
    static pWire makeWire(const std::vector<pEdge>& edges, double precision = Geom::Precision::linear_Resolution());
    /// Makes a wire one edges
    static pWire makeWire(pEdge edges);
    /// Makes a wire one vertex - SB please note that in Acis this is perfectly legal (some Acis functions work with wires, for example, and a wire
    /// can be created from a vertex too).
    static pWire makeWire(pConstVertex vertex);
    /// Makes (possibly sevaral) wires from edges
    static std::vector<pWire> makeWires(const std::vector<pEdge>& edges, double precision = Geom::Precision::linear_Resolution());
    /// Copies a wire
    static pWire copy(pConstWire wire);
    /// Makes an polygonal wire
    static pWire makePolygon(const std::vector<Geom::Pnt>& points);
    /// Makes a polyline wire (as opposed to makePoligon, the wire is not forced to be closed)
    static pWire makePolyline(const std::vector<Geom::Pnt>& points);
    /// Returns the edges of a wire in a connection order.
    static std::vector<pConstEdge> getEdges(pConstWire wire);
    /// Returns copy of the edges of a wire in a connection order.
    static std::vector<pEdge> getEdgesCopy(pConstWire wire);
    /// Returns the vertices of a wire in a connection order.
    static std::vector<pConstVertex> getVertices(pConstWire wire);
    /// Returns the points of a wire in a connection order.
    static void getPoints(pConstWire wire, std::vector<Geom::Pnt>& pnts);
    /// Checks if all edges of the wire are lines
    static bool hasOnlyLines(pConstWire wire);
    /// Checks if wire has at least one helix edge
    static bool hasHelix(pConstWire wire);
    /// Performs an analysis and reorders edges in the wire
    static bool fixReorder(pWire wire);
    /// Writes debug information of wire to stdout
    static void writeDbgInfo(pConstWire wire);
    /// Returns centre of mass (centre of gravity) of the wire
    static Geom::Pnt getCentre(pConstWire wire);
    /// Fillets a wire at the given vertex with the given radius. The give wire is modified in place. Returns TRUE if the operation is successful.
    static bool filletWireAtVertex(pWire wire, const Geom::Pnt& p, double radius, double precision = Geom::Precision::linear_Resolution());
    /// Chamfers a wire at the given vertex with the given offset. The give wire is modified in place. Returns TRUE if the operation is successful.
    static bool chamferWireAtVertex(pWire wire, const Geom::Pnt& p, double offset, double precision = Geom::Precision::linear_Resolution());
    /// Remove edges from a wire. The neighboring edges are extended naturally to fill the gap caused to the removal of wire edges. The edges must
    /// belong to the wire.
    static bool removeEdgesFromWire(pWire wire,
                                    std::vector<pConstEdge> edges,
                                    double precision = Geom::Precision::linear_Resolution(),
                                    bool stayInBndBox = false);
    /// Replace consecutive collinear edges with a single edge: returns False if the wire has not been modified
    static pWire replaceCollinearEdges(pConstWire wire, double precision);
    /// Creates a copy of the wire and transforms the copy
    static pWire transformed(pConstWire base, const Geom::Trsf& t);
    /// Check if the wire is self-intersecting
    static bool isSelfIntersecting(pConstWire wire);
    /// Create offset of wire
    static pWire createOffset(pConstWire wire, const Geom::Dir& refDirection, double offset);
    /// Returns a reversed wire
    static pWire reversed(pConstWire wire);
    /// Joins two wires at coincident vertices.	Returns the joined wire.
    static pWire joined(pConstWire wire1, pConstWire wire2);
    /// Gets the plane of a 3D wire.
    static bool getWirePlane(pConstWire wire, Geom::Pln& plane);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
    /// @cond INTERNAL

    /// Sets the default WireTool. For internal use only.
    static void __setDefaultWireTool__(Topo::WireTool* tool) { _defaultTool = tool; }
    /// Returns new wire with reversed order of vertices, so the normal will have opposite orientation.
    static pWire reverseWirePointsConnection(pConstWire wire, double precision = Geom::Precision::linear_Resolution());
    /// Combines the first wire with the second wire according to the x, y, z parameters and the start, end parameters. The result is a wire or a null
    /// wire in case of failure.
    static pWire
    combineWireWithWire(pConstWire hWire, pConstWire vWire, const uint& x, const uint& y, const uint& z, const double& start, const double& end);

protected:
    virtual pWire _projectWireOnPlane(const Geom::Pln& pln, pConstWire wire, double precision);
    virtual pWire _projectWireOnPlane(pConstWire wire, const Geom::Dir& dir, const Geom::Pln& pln, double dist);
    virtual bool _projectPointOnWire(const Geom::Pnt& p, pConstWire wire, Geom::Pnt& nearest);
    virtual bool _projectPointOnWire(const Geom::Pnt& p, pConstWire wire, Geom::Pnt& nearest, Geom::Dir& refDirection);
    virtual bool _isPlanar(pConstWire wire, Geom::Pln& plane);
    virtual bool _isClosed(pConstWire wire);
    virtual pWire _closed(pConstWire wire, double precision);
    virtual pWire _addedEdge(pConstWire wire, pConstEdge edge, double precision);
    virtual pWire _addedEdge(pConstWire wire, const std::vector<pConstEdge>& edges, double precision);
    virtual pConstVertex _getClosestVertexToPoint(const Geom::Pnt& p, pConstWire wire);
    virtual std::vector<pConstEdge> _getClosestEdgesToPoint(const Geom::Pnt& p, pConstWire wire, double& distance, double precision = 1E-06);
    virtual std::vector<pConstEdge> _getAdjacentEdgesToVertexOnWire(pConstVertex vertex, pConstWire wire);
    virtual void _getAdjacentEdgesToPointOnWire(const Geom::Pnt& point, pConstWire wire, std::vector<pConstEdge>& adjacentEdges);
    virtual pWire _makeWire(const std::vector<pEdge>& edges, double precision);
    virtual pWire _makeWire(pConstVertex vertex);
    virtual std::vector<pWire> _makeWires(const std::vector<pEdge>& edges, double precision);
    virtual pWire _copy(pConstWire wire);
    virtual pWire _makePolygon(const std::vector<Geom::Pnt>& points);
    virtual pWire _makePolyline(const std::vector<Geom::Pnt>& points);
    virtual std::vector<pConstEdge> _getEdges(pConstWire wire);
    virtual std::vector<pConstVertex> _getVertices(pConstWire wire);
    virtual void _getPoints(pConstWire wire, std::vector<Geom::Pnt>& pnts);
    virtual pWire _reverseWirePointsConnection(pConstWire wire, double precision);
    virtual pWire _createOffset(pConstWire wire, const Geom::Dir& refDirection, double offset);
    virtual bool _fixReorder(pWire wire);
    virtual void _writeDbgInfo(pConstWire wire);
    virtual Geom::Pnt _getCentre(pConstWire wire);
    virtual bool _filletWireAtVertex(pWire wire, const Geom::Pnt& p, double radius, double precision);
    virtual bool _chamferWireAtVertex(pWire wire, const Geom::Pnt& p, double offset, double precision);
    virtual bool _removeEdgesFromWire(pWire wire, std::vector<pConstEdge> edges, double precision, bool stayInBndBox = false);
    virtual pWire _replaceCollinearEdges(pConstWire wire, double precision);
    virtual bool _isSelfIntersecting(pConstWire wire);
    virtual pWire _reversed(pConstWire wire);
    virtual pWire _joined(pConstWire wire1, pConstWire wire2);
    virtual bool _getWirePlane(pConstWire& wire, Geom::Pln& pln);
    virtual pWire
    _combineWireWithWire(pConstWire hWire, pConstWire vWire, const uint& x, const uint& y, const uint& z, const double& start, const double& end);
    static Topo::WireTool* _defaultTool;
    /// @endcond
#endif
};

}  // namespace Topo
