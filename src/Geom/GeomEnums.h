#pragma once 

namespace Geom
{
enum class CoordSpace
{
    WCS,  // World  coordinate system
    LCS,  // Local  coordinate system
};

enum class CurveType
{
    LINE,
    CIRCLE,
    ELLIPSE,
    PARABOLA,
    BEZIERCURVE,
    BSPLINECURVE,
    HELIX,
    OTHERCURVE
};

enum class SurfaceType
{
    PLANE,
    CYLINDER,
    CONE,
    SPHERE,
    TORUS,
    BEZIERSURFACE,
    BSPLINESURFACE,
    SURFACEOFREVOLUTION,
    SURFACEOFEXTRUSION,
    OFFSETSURFACE,
    OTHERSURFACE
};

enum class IfcBSplineCurveForm
{
    POLYLINE_FORM,
    CIRCULAR_ARC,
    ELLIPTIC_ARC,
    PARABOLIC_ARC,
    HYPERBOLIC_ARC,
    UNSPECIFIED_CURVE_FORM
};

enum class IfcBSplineSurfaceForm
{
    PLANE_SURF,
    CYLINDRICAL_SURF,
    CONICAL_SURF,
    SPHERICAL_SURF,
    TOROIDAL_SURF,
    SURF_OF_REVOLUTION,
    RULED_SURF,
    GENERALISED_CONE,
    QUADRIC_SURF,
    SURF_OF_LINEAR_EXTRUSION,
    UNSPECIFIED_SURFACE_FORM
};
}  // namespace Geom