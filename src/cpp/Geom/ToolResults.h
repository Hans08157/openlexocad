#pragma once

#include <Geom/Ax2.h>
#include <Geom/Lin.h>
#include <Geom/Pln.h>


namespace Geom
{
/**
 * @brief Struct holding the return values from GeomTools::makePlaneFrom3Points().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_MakePlaneFrom3Points_Result
{
    bool ok = false;
    Geom::Pln plane;
    Geom::Ax2 coordSystem;
};

/**
 * @brief Struct holding the return values from GeomTools::makeLineFrom2Points1().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_MakeLineFrom2Points1_Result
{
    bool ok = false;
    Geom::Lin line;
};

/**
 * @brief Struct holding the return values from GeomTools::projectPointOnPlane1().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_ProjectPointOnPlane1_Result
{
    bool ok = false;
    Geom::Pnt point;
};

/**
 * @brief Struct holding the return values from GeomTools::projectPointOnPlane2().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_ProjectPointOnPlane2_Result
{
    bool ok = false;
    Geom::Pnt point;
    double U;
    double V;
};

/**
 * @brief Struct holding the return values from GeomTools::projectPointOnLine1().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_ProjectPointOnLine1_Result
{
    bool ok = false;
    Geom::Pnt point;
};

/**
 * @brief Struct holding the return values from GeomTools::projectPointOnLine2().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_ProjectPointOnLine2_Result
{
    bool ok = false;
    Geom::Pnt point;
    double U;
};

/**
 * @brief Struct holding the return values from GeomTools::projectPointOnCircle1().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_ProjectPointOnCircle1_Result
{
    bool ok = false;
    Geom::Pnt point;
};

/**
 * @brief Struct holding the return values from GeomTools::makeAxisPlacementFrom2Points().
 * Returns ok=true if the operation was successful.
 * Otherwise returns ok=false.
 * For Python Bindings.
 *
 * @since    24.0
 */
struct LX_GEOM_EXPORT GT_MakeAxisPlacementFrom2Points_Result
{
    bool ok = false;
    Geom::Ax2 ax2;
    double xLength;
    double angleXYPlane;
};
}  // namespace Geom