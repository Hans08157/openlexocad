#pragma once


namespace Topo
{
struct GeometricInformation
{
    GeometricInformation() = default;
    GeometricInformation operator+=(GeometricInformation gi)
    {
        ShapeVolume += gi.ShapeVolume;
        ShapeSurfaceArea += gi.ShapeSurfaceArea;
        ShapeEdgeLength += gi.ShapeEdgeLength;
        ShapeVertexCount += gi.ShapeVertexCount;
        return *this;
    }

    double ShapeVolume = 0.;
    double ShapeSurfaceArea = 0.;
    double ShapeEdgeLength = 0.;
    unsigned int ShapeVertexCount = 0;
};

}  // namespace Topo