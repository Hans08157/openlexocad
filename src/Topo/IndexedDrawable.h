#pragma once

#include <Geom/Ax2.h>
#include <Geom/GeomEnums.h>
#include <memory>

namespace Geom { class IndexedMesh; }
namespace Geom { class Trsf; }



namespace Topo
{
struct SpecialFaceInfo
{
    virtual ~SpecialFaceInfo() = default;
    virtual Geom::SurfaceType getSurfaceType() const = 0;
};

class SpecialFaceInfo_Cylinder : public SpecialFaceInfo
{
public:
    Geom::SurfaceType getSurfaceType() const { return Geom::SurfaceType::CYLINDER; }
    Geom::Ax2 position;
    double radius;
};

class SpecialFaceInfo_Cone : public SpecialFaceInfo
{
public:
    Geom::SurfaceType getSurfaceType() const { return Geom::SurfaceType::CONE; }
    Geom::Ax2 position;
    double angle;
    double radius;
};

class LX_TOPO_EXPORT IndexedFace
{
public:
    IndexedFace();
    IndexedFace(const IndexedFace& rhs);
    std::vector<Geom::Pnt> vertices;
    std::vector<Geom::Dir> verticesNormals;
    std::vector<int> coordinateIndices;
    int index;
    std::shared_ptr<Topo::SpecialFaceInfo> info;
    void dump() const;
};

class LX_TOPO_EXPORT IndexedEdge
{
public:
    IndexedEdge();
    IndexedEdge(const IndexedEdge& rhs);
    std::vector<Geom::Pnt> vertices;
    std::vector<int> edge_coordinateIndices;
    int index;
    void dump() const;
};


class LX_TOPO_EXPORT IndexedDrawable
{
public:
    IndexedDrawable(void);
    IndexedDrawable(const IndexedDrawable& rhs);
    virtual ~IndexedDrawable(void);
    std::vector<IndexedFace> faces;
    std::vector<IndexedEdge> edges;
    void clean();
    std::string createMD5();
    void create_IndexedMesh(Geom::IndexedMesh& mesh);
    virtual void transform(const Geom::Trsf& t);
    void dump();
};
}
