#pragma once

namespace Core
{
enum class ViewerType
{
    _3D_VIEWER = 0,             // 3D_VIEWER
    _2D_TOP_VIEWER = 1,         // 2D_TOP_VIEWER
    _2D_NONTOP_VIEWER = 2       // 2D_VIEWER //all other 2D views
};

enum class ViewType
{
    _3D_VIEW = 0,               // 
    _2D_PLAN_VIEW = 1,          // aka Top View
    _2D_ELEVATION_VIEW = 2,     // aka Vertical View
    _2D_SECTION_VIEW = 3,       // aka Cross Section View
    _2D_FLOOR_PLAN_VIEW = 4,    // Floor plan with special 2d behavior
};
}  // namespace Core
