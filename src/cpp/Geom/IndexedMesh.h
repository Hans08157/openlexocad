#pragma once

#include <Geom/Dir.h>
#include <Geom/GTrsf.h>
#include <Geom/Pnt.h>
#include <memory>

namespace Base
{
class AbstractWriter;
}

namespace Geom
{
class LX_GEOM_EXPORT IndexedMesh
{
public:
    IndexedMesh();
    IndexedMesh(const IndexedMesh& other);
    IndexedMesh(const std::vector<int>& model, const std::vector<Geom::Pnt>& points);
    virtual ~IndexedMesh();

    //  SoIndexedFaceSet-Format
    std::vector<Geom::Pnt> face_vertices;
    std::vector<long> face_coordinateIndices;
    // normals are obligatory, vbos!
    std::vector<Geom::Dir> face_per_vertex_normals;
    // color: 0xrrggbbaa
    std::vector<unsigned int> face_color_per_vertex;

    //  SoIndexedLineSet-Format
    std::vector<Geom::Pnt> wire_vertices;
    std::vector<long> wire_coordinateIndices;
    std::vector<unsigned int> wire_color_per_vertex;

    IndexedMesh& operator=(const IndexedMesh&);
    bool operator==(const IndexedMesh& c) const;

    virtual void transform(const Geom::Trsf& t);
    void transform(const Geom::GTrsf& t);
    void createEdges(const std::vector<int>& model, const std::vector<Geom::Pnt>& points);

    bool restore(const std::string& s);

    static bool setBinaryReadMode(bool on);
    static bool setBinaryWriteMode(bool on);
};



 LX_GEOM_EXPORT  std::istream& operator>>(std::istream& is, Geom::IndexedMesh& op);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& os, Geom::IndexedMesh& op);



}  // namespace Geom


 LX_GEOM_EXPORT  Base::AbstractWriter& operator<<(Base::AbstractWriter& os, Geom::IndexedMesh& op);

typedef std::shared_ptr<Geom::IndexedMesh> pIndexedMesh;
