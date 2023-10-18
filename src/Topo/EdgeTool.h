///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2017   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once


#include <Topo/ToolResults.h>
namespace Base { struct Double; }
namespace Core { class DocObject; }
namespace Geom { class Trsf; }
namespace Geom { enum class CurveType; }


namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Edges.
 *
 * @ingroup TOPO_SHAPETOOLS
 */
class LX_TOPO_EXPORT EdgeTool
{
public:
    static pEdge copy(pConstEdge e);
    static pEdge makeEdge(const Geom::Pnt& p1, const Geom::Pnt& p2);
    static pEdge makeEdge(Core::DocObject* curve, double startParam, double endParam);
    static pEdge makeArcOfCircle(const Geom::Pnt& p1, const Geom::Pnt& pp, const Geom::Pnt& p2);
    static pEdge makeArcOfCircle(const Geom::Circ& circ, double param1, double param2, bool sameSense = true);
    static pEdge makeArcOfCircle(const Geom::Circ& circ, const Geom::Pnt& p1, const Geom::Pnt& p2, bool sameSense = true);
    static bool projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge, Geom::Pnt& nearest, Geom::Dir& refDirection);
    static bool projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge, double& u);
    static bool projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge, Base::Double& u);
    static bool calculateOffsetFromEdgeThruPoint(pConstEdge edge, const Geom::Pnt& p, double& offset, Geom::Dir& refDirection);
    static bool calculateOffsetFromEdgeThruPoint(pConstEdge edge, const Geom::Pnt& p, Base::Double& offset, Geom::Dir& refDirection);
    static bool sense(pConstEdge edge, bool& sense);
    static bool firstParameter(pConstEdge edge, double& u);
    static bool firstParameter(pConstEdge edge, Base::Double& u);
    static bool lastParameter(pConstEdge edge, double& u);
    static bool lastParameter(pConstEdge edge, Base::Double& u);
    static bool value(pConstEdge edge, double u, Geom::Pnt& p);
    static bool d0(pConstEdge edge, double u, Geom::Pnt& p);
    static bool d1(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1);
    static bool d2(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1, Geom::Vec& v2);
    static bool d3(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1, Geom::Vec& v2, Geom::Vec& v3);
    static bool splitEdge(pConstEdge edge, double u, pEdge& edge1, pEdge& edge2);
    static bool getGeomCurveType(pConstEdge edge, Geom::CurveType& type);
    static double getLength(pConstEdge edge);
    static bool isPointOnEdge(pConstEdge edge, const Geom::Pnt& pnt);
    static bool isStraight(pConstEdge edge);
    static bool isCircular(pConstEdge edge);
    static bool getArcParameters(pConstEdge edge, Geom::Circ& circle, double& startParam, double& endParam);
    static bool getLineParameters(pConstEdge edge, Geom::Lin& line, double& startParam, double& endParam, double& scale);
    static Topo::OrientationType getOrientation(pConstCoedge edge);
    static bool intersects(pConstEdge edge1, pConstEdge edge2, std::vector<Geom::Pnt>& intersections, double tolerance);
    static pEdge reversed(pConstEdge edge);
    static Geom::Pnt getCentre(pConstEdge edge);
    static pShape extrudeEdge(pConstEdge edge, const Geom::Dir& extrudedDirection, double depth);
    static bool discretizeNonLinearEdge(pConstEdge edge, std::vector<Geom::Pnt>& points, double deflection);
    static pEdge transformed(pConstEdge base, const Geom::Trsf& t);
    static bool areTheSameInstance(pConstEdge edge1, pConstEdge edge2);
    static const void* getInstancePointer(pConstEdge edge);
    static bool bspline_facet(const std::vector<Geom::Pnt>& pnts, const bool& periodic, std::vector<Geom::Pnt>& faceted_pnts, double tolerance);
    static pEdge makeClothoidSegment(const Geom::Clothoid2d& clothoid);
    static bool getClothoidParameters(pConstEdge edge, Geom::Ax2& ax2, Geom::Clothoid2d& clothoid);
    static std::pair<std::vector<double>, std::vector<Geom::Pnt>> getKnotsAndControlPointsFromEdge(pConstEdge edge);
    static pEdge join(const std::vector<pConstEdge>& edges);

    /** @name Interfaces modified for Python Bindings */
    //@{


    static ET_ProjectPointOnEdge_Result1 projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge);
    static ET_ProjectPointOnEdge_Result2 projectPointOnEdge2(const Geom::Pnt& p, pConstEdge edge);

    static ET_CalculateOffsetFromEdgeThruPoint_Result calculateOffsetFromEdgeThruPoint(pConstEdge edge, const Geom::Pnt& p);
    static ET_FirstParameter_Result firstParameter(pConstEdge edge);
    static ET_LastParameter_Result lastParameter(pConstEdge edge);
    static ET_Value_Result value(pConstEdge edge, double u);
    static ET_D0_Result d0(pConstEdge edge, double u);
    static ET_D1_Result d1(pConstEdge edge, double u);
    static ET_D2_Result d2(pConstEdge edge, double u);
    static ET_D3_Result d3(pConstEdge edge, double u);
    static ET_SplitEdge_Result splitEdge(pConstEdge edge, double u);
    static ET_GeomCurveType_Result getGeomCurveType(pConstEdge edge);

    static ET_ArcParameters_Result getArcParameters(pConstEdge edge);
    static ET_LineParameters_Result getLineParameters(pConstEdge edge);
    static ET_Intersects_Result intersects(pConstEdge edge1, pConstEdge edge2, double tolerance);
    static ET_DiscretizeNonLinearEdge_Result discretizeNonLinearEdge(pConstEdge edge, double deflection);
    static ET_Bspline_facet_Result bspline_facet(const std::vector<Geom::Pnt>& pnts, bool periodic, double tolerance);
    static ET_ClothoidParameters_Result getClothoidParameters(pConstEdge edge);


    //@}

#ifndef SWIG  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
    /// @cond INTERNAL
    /// Sets the default EdgeTool. For internal use only.
    static void __setDefaultEdgeTool__(Topo::EdgeTool* tool) { _defaultTool = tool; }

protected:
    virtual pEdge _copy(pConstEdge e);
    virtual pEdge _makeEdge(const Geom::Pnt& p1, const Geom::Pnt& p2);
    virtual pEdge _makeEdge(Core::DocObject* curve, double startParam, double endParam);
    virtual pEdge _makeArcOfCircle(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& pp);
    virtual pEdge _makeArcOfCircle(const Geom::Circ& circ, double param1, double param2, bool sameSense);
    virtual pEdge _makeArcOfCircle(const Geom::Circ& circ, const Geom::Pnt& p1, const Geom::Pnt& p2, bool sameSense);
    virtual bool _projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge, Geom::Pnt& nearest, Geom::Dir& refDirection);
    virtual bool _projectPointOnEdge(const Geom::Pnt& p, pConstEdge edge, double& u);
    virtual bool _calculateOffsetFromEdgeThruPoint(pConstEdge edge, const Geom::Pnt& p, double& offset, Geom::Dir& refDirection);
    virtual bool _sense(pConstEdge edge, bool& sense);
    virtual bool _firstParameter(pConstEdge edge, double& u);
    virtual bool _lastParameter(pConstEdge edge, double& u);
    virtual bool _value(pConstEdge edge, double u, Geom::Pnt& p);
    virtual bool _d0(pConstEdge edge, double u, Geom::Pnt& p);
    virtual bool _d1(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1);
    virtual bool _d2(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1, Geom::Vec& v2);
    virtual bool _d3(pConstEdge edge, double u, Geom::Pnt& p, Geom::Vec& v1, Geom::Vec& v2, Geom::Vec& v3);
    virtual bool _splitEdge(pConstEdge edge, double u, pEdge& edge1, pEdge& edge2);
    virtual bool _getGeomCurveType(pConstEdge edge, Geom::CurveType& type);
    virtual double _getLength(pConstEdge edge);
    virtual bool _isPointOnEdge(pConstEdge edge, const Geom::Pnt& pnt);
    virtual bool _isCircular(pConstEdge edge);
    virtual bool _isStraight(pConstEdge edge);
    virtual bool _getArcParameters(pConstEdge edge, Geom::Circ& circle, double& startParam, double& endParam);
    virtual bool _getLineParameters(pConstEdge edge, Geom::Lin& line, double& startParam, double& endParam, double& scale);
    virtual Topo::OrientationType _getOrientation(pConstCoedge edge);
    virtual bool _intersects(pConstEdge edge1, pConstEdge edge2, std::vector<Geom::Pnt>& intersections, double tolerance);
    virtual pEdge _reversed(pConstEdge edge);
    virtual Geom::Pnt _getCentre(pConstEdge edge);
    virtual pShape _extrudeEdge(pConstEdge edge, const Geom::Dir& extrudedDirection, double depth);
    virtual bool _discretizeNonLinearEdge(pConstEdge edge, std::vector<Geom::Pnt>& points, double deflection);
    virtual bool _areTheSameInstance(pConstEdge edge1, pConstEdge edge2);
    virtual const void* _getInstancePointer(pConstEdge edge);
    virtual bool _bspline_facet(const std::vector<Geom::Pnt>& pnts, const bool& periodic, std::vector<Geom::Pnt>& faceted_pnts, double tolerance);

    virtual pEdge _makeClothoidSegment(const Geom::Clothoid2d& clothoid);
    virtual bool _getClothoidParameters(pConstEdge edge, Geom::Ax2& ax2, Geom::Clothoid2d& clothoid);
    virtual std::pair<std::vector<double>, std::vector<Geom::Pnt>> _getKnotsAndControlPointsFromEdge(pConstEdge edge);
    virtual pEdge _join(const std::vector<pConstEdge>& edges);

    static Topo::EdgeTool* _defaultTool;
    /// @endcond
#endif
};



}  // namespace Topo