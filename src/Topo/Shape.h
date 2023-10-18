#pragma once

#include <Base/Base.h>
#include <Core/Variant.h>
#include <Geom/Bnd_Box.h>
#include <Topo/Types.h>


class CA_Detail;
class CA_Snap;
class ENTITY;

namespace Core
{
class DbgInfo;
}  // namespace Core

namespace Acis
{
class AcisWireTool;
}  // namespace Acis


namespace Topo
{
class ShapeTool;
class MeshTool;
class CompoundTool;
class SolidTool;
class ShellTool;
class FaceTool;
class WireTool;
class EdgeTool;
class VertexTool;
class ShapeVariantHandler;

enum class ShapeType
{
    MESH,
    COMPOUND,
    COMPSOLID,
    NCOMPOUND,
    SOLID,
    SHELL,
    FACE,
    WIRE,
    EDGE,
    VERTEX,
    SHAPE,
    UNDEFINED
};



class LX_TOPO_EXPORT ShapeFactory
{
public:
    friend class Shape;
    static std::map<std::string, ShapeFactory*> registry;
    static pShape read(const std::string& format, const std::string& data, int version);
    static pShape read(const std::string& format, std::istream& reader);
    static pShape read(const std::string& format, const Base::String& fileName);

private:
    virtual pShape read(const std::string& data, int version) = 0;
    virtual pShape read(std::istream& reader) = 0;
    virtual pShape read(const Base::String& fileName) = 0;
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */
class LX_TOPO_EXPORT TopologicalItem
#ifndef SWIG
    : public Base::BaseClass
#endif
{
    TYPESYSTEM_HEADER();

public:
    TopologicalItem() = default;
    virtual ~TopologicalItem() = default;

    enum class MesherType
    {
        Default_Mesher,
        Acis_Mesher,
        Compound_Mesher
    };

    enum class ModelingKernel
    {
        OCC,
        ACIS,
        CARVE,
        MIXED,  // -> for compound
        UNKNOWN
    };

    virtual MesherType getMesherType() const = 0;
    virtual ModelingKernel getModelingKernel() const = 0;
    /// Returns top-level owner. Returns this if item is top-level.
    virtual pConstTopologicalItem getOwner() const = 0;
    virtual Topo::ShapeTool* getShapeTool() const = 0;
    virtual bool getGeometricInformation(Topo::GeometricInformation&) const;

    virtual ENTITY* getEntity() const { return 0; }  // why do we return ACIS class in common interface?
    // It should be in Acis class, or we can directly store ENTITY here and have the necessary interface -> not polluting Acis classes

protected:
    TopologicalItem(ENTITY* /*ent*/){};

    pConstTopologicalItem source{};
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */
class LX_TOPO_EXPORT Shape : public Topo::TopologicalItem
#ifndef SWIG
    ,
                             public std::enable_shared_from_this<Topo::Shape>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Shape() = default;
    Shape(pConstShape rhs);
    virtual ~Shape() = default;

    friend class ShapeTool;
    friend class FaceTool;

    enum CheckShape
    {
        CheckShapeIsValidAndThrowException,
        CheckShapeIsValid,
        Unchecked
    };

    bool getGeometricInformation(Topo::GeometricInformation&) const override { return false; }

    virtual void transform(const Geom::Trsf& t);
    virtual Geom::Trsf getTransform() const;
    virtual Topo::ShapeType getShapeType() const = 0;

    /// Variant operator
    operator Core::Variant() const;
    pConstTopologicalItem getOwner() const override;

    /// Checks if this shape has ShapeAttributes.
    bool hasShapeAttributes() const;
    /// Returns the ShapeAttributes of this shape.
    Topo::ShapeAttributes* getShapeAttributes() const;
    /// Adds ShapeAttributes to this shape. If shape already had some attributes they are released.
    void addShapeAttributes(Topo::ShapeAttributes* atts);
    /// Deletes the ShapeAttributes associated with this shape
    void releaseShapesAttributes();
    /// Get BoundingBox
    virtual Geom::Bnd_Box getBoundingBox() const = 0;

    virtual void setIndexMesh(pIndexedMesh m);
    virtual pIndexedMesh getIndexedMesh() const;
    virtual bool createIndexedMesh(pIndexedMesh m) const;

    virtual void setIndexedDrawable(pIndexedDrawable);
    virtual pIndexedDrawable getIndexedDrawable() const;

    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const;
    virtual Topo::Shape* clone(bool deepcopy) const = 0;

    virtual bool wasCreatedWithProblems() const { return false; }
    virtual void setWasCreatedWithProblems(bool) {}

    mutable std::set<Core::DocObject*> m_appGeometryBackLinks{};

protected:
    Shape(ENTITY* ent);

    virtual void copyFrom(pConstShape rhs, bool deepCopy = true) = 0;

    virtual bool isSingleFace() const;
    virtual bool isSingleWire() const;
    virtual bool isSingleEdge() const;
    virtual bool isSingleVertex() const;
    virtual bool isSolid() const;
    virtual bool isClosedSolid() const;
    virtual bool isWire() const;
    virtual bool isCompound() const;
    virtual bool isMesh() const { return false; }

    bool _copy(const Topo::Shape* rhs, bool deepCopy = true);

private:
    /// Handler for Shape as Variant
    static Topo::ShapeVariantHandler* _vHnd;
    Topo::ShapeAttributes* _myAtts = nullptr;
    pIndexedMesh _indexedMesh{};
    pIndexedDrawable _indexedDrawable{};
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */
class LX_TOPO_EXPORT MeshShape : public Topo::Shape
{
    TYPESYSTEM_HEADER();

public:
    typedef std::vector<int> MeshModel;
    typedef std::vector<MeshModel> SubMeshModels;

    MeshShape() = default;
    MeshShape(pConstMesh rhs, bool deepCopy = true);
    virtual ~MeshShape() = default;

    friend class MeshTool;

    virtual void copyFrom(pConstMesh rhs, bool deepCopy = true) = 0;
    virtual pConstBrepData getMeshAsBrepData() const = 0;
    virtual void getTextureCoordinates(std::vector<Geom::Pnt2d>& textureCoordinates, std::vector<int>& textureIndices) const = 0;
    virtual bool calculateDetail(CA_Detail& detail, const CA_Snap& theSnap) = 0;
    virtual void getEdges(std::vector<std::pair<Geom::Pnt, Geom::Pnt> >& lines) const = 0;
    virtual bool getEdge(int idx, std::pair<Geom::Pnt, Geom::Pnt>& line) const = 0;
    virtual void getPoints(std::vector<Geom::Pnt>& points) const = 0;
    virtual void getModel(MeshModel& model) const = 0;
    virtual std::vector<Geom::Pnt> getNormals() const = 0;
    virtual void getOuterBoundaries(std::vector<Geom::Pnt>& points, std::vector<int>& edges) const = 0;
    virtual void getFacePoints(int index, std::vector<Geom::Pnt>& points) const = 0;

protected:
    void copyFrom(pConstShape rhs, bool deepCopy = true) override;
    virtual Topo::MeshTool* getMeshTool() const = 0;
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Compound : public Topo::Shape
{
    TYPESYSTEM_HEADER();

public:
    Compound() = default;
    Compound(pConstCompound rhs, bool deepCopy = true);
    virtual ~Compound() = default;

    friend class CompoundTool;

    virtual void copyFrom(pConstCompound rhs, bool deepCopy = true) = 0;

protected:
    Compound(ENTITY* ent) : Shape(ent) {}
    virtual Topo::CompoundTool* getCompoundTool() const = 0;
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Solid : public Topo::Shape
{
    TYPESYSTEM_HEADER();

public:
    Solid() = default;
    Solid(pConstSolid rhs, bool deepCopy = true);
    virtual ~Solid() = default;

    friend class SolidTool;

    virtual void copyFrom(pConstSolid rhs, bool deepCopy = true) = 0;

protected:
    Solid(ENTITY* ent) : Shape(ent) {}
    virtual Topo::SolidTool* getSolidTool() const = 0;
};

/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Shell : public Topo::TopologicalItem
#ifndef SWIG
    ,
                             public std::enable_shared_from_this<Topo::Shell>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Shell() = default;
    Shell(pConstShell rhs, bool deepCopy = true);
    virtual ~Shell() = default;

    friend class ShellTool;

    virtual void copyFrom(pConstShell rhs, bool deepCopy = true) = 0;
    virtual void transform(const Geom::Trsf&) {}

protected:
    Shell(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::ShellTool* getShellTool() const = 0;
};


/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Face : public Topo::TopologicalItem
#ifndef SWIG
    ,
                            public std::enable_shared_from_this<Topo::Face>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Face() = default;
    Face(pConstFace rhs, bool deepCopy = false);
    virtual ~Face() = default;

    friend class FaceTool;

    /// Projects pnt on the face. Returns normal for this point and the calculated pointOnFace
    virtual bool getFaceNormal(const Geom::Pnt& pnt, Geom::Dir& dir, Geom::Pnt& pointOnFace) const = 0;
    virtual Core::DocObject* getGeometry() const { return nullptr; }
    virtual void transform(const Geom::Trsf&) {}

protected:
    Face(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::FaceTool* getFaceTool() const = 0;
};


/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Wire : public Topo::TopologicalItem
#ifndef SWIG
    ,
                            public std::enable_shared_from_this<Topo::Wire>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Wire() = default;
    // Wire(pConstWire rhs, bool deepCopy = false); // AB 11.5.2022 do we need it? It is not used
    virtual ~Wire() = default;

    friend class WireTool;
    friend class Acis::AcisWireTool;

    virtual void copyFrom(pConstWire rhs, bool deepCopy = true) = 0;
    virtual int getEdgeCount() const = 0;
    virtual pConstEdge getEdgeByIndex(int idx) const = 0;
    virtual void transform(const Geom::Trsf&) {}
    virtual bool isLoop() const { return false; }

protected:
    Wire(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::WireTool* getWireTool() const = 0;
};



/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */
class LX_TOPO_EXPORT Edge : public Topo::TopologicalItem
#ifndef SWIG
    ,
                            public std::enable_shared_from_this<Topo::Edge>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Edge() = default;
    Edge(pConstEdge rhs, bool deepCopy = true);
    virtual ~Edge() = default;

    friend class EdgeTool;

    virtual void copyFrom(pConstEdge rhs, bool deepCopy = true) = 0;
    /// Variant operator
    // operator Core::Variant() const;
    virtual void transform(const Geom::Trsf&) {}

protected:
    Edge(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::EdgeTool* getEdgeTool() const = 0;

private:
    double _passagePntParam = 0.;
    bool _hasPassagePntParam = false;
};

/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Coedge : public Topo::TopologicalItem
#ifndef SWIG
    ,
                              public std::enable_shared_from_this<Topo::Coedge>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Coedge() = default;
    Coedge(pConstCoedge rhs, bool deepCopy = true);
    virtual ~Coedge() = default;

    friend class EdgeTool;

    virtual void copyFrom(pConstCoedge rhs, bool deepCopy = true) = 0;
    /// Variant operator
    // operator Core::Variant() const;
    virtual void transform(const Geom::Trsf&) {}
    virtual pConstEdge getEdge() const = 0;

protected:
    Coedge(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::EdgeTool* getEdgeTool() const = 0;

private:
    double _passagePntParam = 0.;
    bool _hasPassagePntParam = false;
};

/**
 * @brief
 *
 * @ingroup TOPO_SHAPES
 */

class LX_TOPO_EXPORT Vertex : public Topo::TopologicalItem
#ifndef SWIG
    ,
                              public std::enable_shared_from_this<Topo::Vertex>
#endif
{
    TYPESYSTEM_HEADER();

public:
    Vertex() = default;
    Vertex(pConstVertex rhs, bool deepCopy = true);
    virtual ~Vertex() = default;

    friend class VertexTool;

    virtual void copyFrom(pConstVertex rhs, bool deepCopy = true) = 0;
    virtual Geom::Pnt getPoint() const = 0;
    virtual void transform(const Geom::Trsf&) {}

protected:
    Vertex(ENTITY* ent) : TopologicalItem(ent) {}
    virtual Topo::VertexTool* getVertexTool() const = 0;
};



class LX_TOPO_EXPORT LazyFacetedBrepShape : public Topo::Shape
{
    TYPESYSTEM_HEADER();

public:
    LazyFacetedBrepShape() = default;
    LazyFacetedBrepShape(pConstShape rhs) {}
    virtual ~LazyFacetedBrepShape() = default;
};



class LX_TOPO_EXPORT FacetedShape
{
public:
    FacetedShape() = default;
    virtual ~FacetedShape() = default;

    std::vector<Geom::Pnt> face_vertices;
    std::vector<long> face_coordinateIndices;
    std::vector<Geom::Dir> face_per_vertex_normals;

    std::vector<Geom::Pnt> wire_vertices;
    std::vector<long> wire_coordinateIndices;
};



class LX_TOPO_EXPORT ShapeVariantHandler : public Core::VariantHandler
{
public:
    Core::Variant create();
    bool isEqual(const Core::Variant& v1, const Core::Variant& v2, double /*tolerance*/ = 1E-06) const
    {
        bool ok1, ok2;
        if (v1.getValue<pShape>(&ok1) == v2.getValue<pShape>(&ok2) && ok1 && ok2)
            return true;
        else
            return false;
    }
    int getType() { return (int)Core::Variant::Shape; }
    Base::String getAsString(const Core::Variant& v) const;
};

class LX_TOPO_EXPORT ConstShapeVariantHandler : public Core::VariantHandler
{
public:
    Core::Variant create();
    bool isEqual(const Core::Variant& v1, const Core::Variant& v2, double /*tolerance*/ = 1E-06) const
    {
        bool ok1, ok2;
        if (v1.getValue<pConstShape>(&ok1) == v2.getValue<pConstShape>(&ok2) && ok1 && ok2)
            return true;
        else
            return false;
    }
    int getType() { return (int)Core::Variant::ConstShape; }
    Base::String getAsString(const Core::Variant& v) const;
};

}  // namespace Topo

#define REGISTER_SHAPE_FACTORY(_factoryName_, _shapeFormat_) Topo::ShapeFactory::registry[_shapeFormat_] = (Topo::ShapeFactory*)new _factoryName_();
