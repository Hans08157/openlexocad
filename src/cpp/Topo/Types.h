#pragma once
#include <memory>

namespace Base
{
class BaseClass;
}
namespace Geom
{
class IndexedMesh;
class BrepData;
}

namespace Topo
{
class TopologicalItem;
class Shape;
class LazyFacetedBrepShape;
class MeshShape;
class Compound;
class ShapeSet;
class Solid;
class Shell;
class Face;
class Wire;
class Edge;
class Coedge;
class Vertex;
class Geometry;
class ShapeAttributes;

class FacetedShape;
class IndexedDrawable;
struct GeometricInformation;
enum class OrientationType
{
    UNDEFINED,
    FORWARD,
    REVERSED,
    INTERNAL,
    EXTERNAL
};
}  // namespace Topo

typedef std::shared_ptr<Base::BaseClass> pBaseClass;
typedef std::shared_ptr<Topo::TopologicalItem> pTopologicalItem;
typedef std::shared_ptr<Topo::Shape> pShape;
typedef std::shared_ptr<Topo::LazyFacetedBrepShape> pLazyFacetedBrepShape;
typedef std::shared_ptr<Topo::MeshShape> pMesh;
typedef std::shared_ptr<Topo::Compound> pCompound;
typedef std::shared_ptr<Topo::Solid> pSolid;
typedef std::shared_ptr<Topo::Shell> pShell;
typedef std::shared_ptr<Topo::Face> pFace;
typedef std::shared_ptr<Topo::Wire> pWire;
typedef std::shared_ptr<Topo::Edge> pEdge;
typedef std::shared_ptr<Topo::Coedge> pCoedge;
typedef std::shared_ptr<Topo::Vertex> pVertex;
typedef std::shared_ptr<Topo::IndexedDrawable> pIndexedDrawable;
typedef std::shared_ptr<Geom::IndexedMesh> pIndexedMesh;
typedef std::shared_ptr<Geom::BrepData> pBrepData;

typedef std::shared_ptr<Base::BaseClass const> pConstBaseClass;
typedef std::shared_ptr<Topo::TopologicalItem const> pConstTopologicalItem;
typedef std::shared_ptr<Topo::Shape const> pConstShape;
typedef std::shared_ptr<Topo::LazyFacetedBrepShape const> pConstLazyFacetedBrepShape;
typedef std::shared_ptr<Topo::MeshShape const> pConstMesh;
typedef std::shared_ptr<Topo::Compound const> pConstCompound;
typedef std::shared_ptr<Topo::Solid const> pConstSolid;
typedef std::shared_ptr<Topo::Shell const> pConstShell;
typedef std::shared_ptr<Topo::Face const> pConstFace;
typedef std::shared_ptr<Topo::Wire const> pConstWire;
typedef std::shared_ptr<Topo::Edge const> pConstEdge;
typedef std::shared_ptr<Topo::Coedge const> pConstCoedge;
typedef std::shared_ptr<Topo::Vertex const> pConstVertex;
typedef std::shared_ptr<const Geom::BrepData> pConstBrepData;

typedef std::unique_ptr<Base::BaseClass> uniqueBaseClass;
typedef std::unique_ptr<Topo::TopologicalItem> uniqueTopologicalItem;
typedef std::unique_ptr<Topo::Shape> uniqueShape;
typedef std::unique_ptr<Topo::MeshShape> uniqueMesh;
typedef std::unique_ptr<Topo::Compound> uniqueCompound;
typedef std::unique_ptr<Topo::ShapeSet> uniqueShapeSet;
typedef std::unique_ptr<Topo::Solid> uniqueSolid;
typedef std::unique_ptr<Topo::Shell> uniqueShell;
typedef std::unique_ptr<Topo::Face> uniqueFace;
typedef std::unique_ptr<Topo::Wire> uniqueWire;
typedef std::unique_ptr<Topo::Edge> uniqueEdge;
typedef std::unique_ptr<Topo::Coedge> uniqueCoedge;
typedef std::unique_ptr<Topo::Vertex> uniqueVertex;
typedef std::unique_ptr<Topo::FacetedShape> uniqueFacetedShape;


