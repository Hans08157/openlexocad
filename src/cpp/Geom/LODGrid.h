#pragma once

#include <Geom/Pnt.h>
#include <Geom/Vec.h>
#ifndef Q_MOC_RUN
#include <mutex>
#endif

namespace Base
{
class MColor;
}

#undef min
#undef max

namespace Geom
{

struct LODPoint
{
    LODPoint(const double lcoordinates[3])
    {
        coordinates[0] = lcoordinates[0];
        coordinates[1] = lcoordinates[1];
        coordinates[2] = lcoordinates[2];
    }
    float coordinates[3];
};


struct LX_GEOM_EXPORT LODNode
{
public:
    std::string id = "";
    int64_t level = 0;
    int64_t x = 0;
    int64_t y = 0;
    int64_t z = 0;
    int64_t size;
    int64_t numPoints;
    std::vector<LODPoint> points;
    std::vector<uint32_t> colors;

    LODNode(std::string id, int numPoints);
    LODNode(const LODNode& origin);
    LODNode(const LODNode&& origin);
    ~LODNode();

    void addPoint(const double coordinates[3], const uint32_t c);

private:
    std::mutex mutex;
};

class LX_GEOM_EXPORT LODGrid
{
public:
    LODGrid(uint64_t lgridsize, Geom::Vec lmin, Geom::Vec lmax);
    LODGrid(const LODGrid& origin) = delete;
    LODGrid(const LODGrid&& origin) = delete;
    ~LODGrid();

    uint64_t toIndex(const double coordinates[3]);
    void addCoordinate_Pass1(const double coordinates[3]);
    void addCoordinate_Pass1(const Geom::Pnt& p);
    void addCoordinate_Pass2(const double coordinates[3], uint32_t color);
    void addCoordinate_Pass2(const Geom::Pnt& p, const Base::MColor& color);
    void shuffle();
    void createLUT();

    Geom::Vec min_bbox;
    Geom::Vec max_bbox;
    Geom::Vec cube_min;
    Geom::Vec cube_max;
    uint64_t gridSize;
    double dGridSize;
    Geom::Vec cubeSize;
    std::vector<int32_t> grid{0};
    std::vector<int32_t> lut{0};
    int64_t maxPointsPerChunk = 1'000'000;
    std::vector<LODNode*> nodes;
};
}  // namespace Geom
