#pragma once

#include <Geom/Circ.h>
#include <Geom/Clothoid2d.h>
#include <Geom/Lin.h>
#include <Geom/Vec.h>
#include <Geom/GeomEnums.h>
#include <Topo/Types.h>

namespace Topo
{
/**
 * @brief Struct holding the return values from EdgeTool::projectPointOnEdge().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_ProjectPointOnEdge_Result1
{
    bool ok = false;
    Geom::Pnt nearest;
    Geom::Dir refDirection;
};

/**
 * @brief Struct holding the return values from EdgeTool::projectPointOnEdge2().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_ProjectPointOnEdge_Result2
{
    bool ok = false;
    double u;
};

/**
 * @brief Struct holding the return values from EdgeTool::calculateOffsetFromEdgeThruPoint().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_CalculateOffsetFromEdgeThruPoint_Result
{
    bool ok = false;
    double offset;
    Geom::Dir refDirection;
};

/**
 * @brief Struct holding the return values from EdgeTool::firstParameter().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_FirstParameter_Result
{
    bool ok = false;
    double u;
};

/**
 * @brief Struct holding the return values from EdgeTool::lastParameter().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_LastParameter_Result
{
    bool ok = false;
    double u;
};

/**
 * @brief Struct holding the return values from EdgeTool::value().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_Value_Result
{
    bool ok = false;
    Geom::Pnt p;
};

/**
 * @brief Struct holding the return values from EdgeTool::d0().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_D0_Result
{
    bool ok = false;
    Geom::Pnt p;
};

/**
 * @brief Struct holding the return values from EdgeTool::d1().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_D1_Result
{
    bool ok = false;
    Geom::Pnt p;
    Geom::Vec v1;
};

/**
 * @brief Struct holding the return values from EdgeTool::d2().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_D2_Result
{
    bool ok = false;
    Geom::Pnt p;
    Geom::Vec v1;
    Geom::Vec v2;
};

/**
 * @brief Struct holding the return values from EdgeTool::d3().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_D3_Result
{
    bool ok = false;
    Geom::Pnt p;
    Geom::Vec v1;
    Geom::Vec v2;
    Geom::Vec v3;
};

/**
 * @brief Struct holding the return values from EdgeTool::splitEdge().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_SplitEdge_Result
{
    bool ok = false;
    pEdge edge1;
    pEdge edge2;
};

/**
 * @brief Struct holding the return values from EdgeTool::getGeomCurveType().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_GeomCurveType_Result
{
    bool ok = false;
    Geom::CurveType type;
};

/**
 * @brief Struct holding the return values from EdgeTool::getArcParameters().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_ArcParameters_Result
{
    bool ok = false;
    Geom::Circ circle;
    double startParam;
    double endParam;
};

/**
 * @brief Struct holding the return values from EdgeTool::getLineParameters().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_LineParameters_Result
{
    bool ok = false;
    Geom::Lin line;
    double startParam;
    double endParam;
    double scale;
};

/**
 * @brief Struct holding the return values from EdgeTool::intersects().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_Intersects_Result
{
    bool ok = false;
    std::vector<Geom::Pnt> intersections;
};

/**
 * @brief Struct holding the return values from EdgeTool::discretizeNonLinearEdge().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_DiscretizeNonLinearEdge_Result
{
    bool ok = false;
    std::vector<Geom::Pnt> points;
};

/**
 * @brief Struct holding the return values from EdgeTool::bspline_facet().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_Bspline_facet_Result
{
    bool ok = false;
    std::vector<Geom::Pnt> faceted_pnts;
};

/**
 * @brief Struct holding the return values from EdgeTool::getClothoidParameters().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct ET_ClothoidParameters_Result
{
    bool ok = false;
    Geom::Ax2 ax2;
    Geom::Clothoid2d clothoid;
};

}  // namespace Topo