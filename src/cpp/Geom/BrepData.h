#pragma once

#include <Geom/PointMapWithTolerance.h>
#include <memory>

namespace Core
{
class PropertyBrepData;
class PropertyBrepDataSet;
}  // namespace Core

namespace Topo
{
class FaceTool;
}

namespace Geom
{
class BrepLoop;
class BrepFace;
class BrepData;
class Dir;
class Pnt;
class Vec;
class Trsf;
}  // namespace Geom

typedef std::shared_ptr<Geom::BrepData> pBrepData;
typedef std::shared_ptr<Geom::BrepFace> pBrepFace;
typedef std::shared_ptr<Geom::BrepFace> pBrepLoop;
typedef std::shared_ptr<const Geom::BrepData> pConstBrepData;
typedef std::shared_ptr<const Geom::BrepFace> pConstBrepFace;
typedef std::shared_ptr<const Geom::BrepLoop> pConstBrepLoop;

LX_GEOM_EXTERN template class LX_GEOM_EXPORT std::weak_ptr<const Geom::BrepData>;
LX_GEOM_EXTERN template class LX_GEOM_EXPORT std::weak_ptr<const Geom::BrepFace>;
LX_GEOM_EXTERN template class LX_GEOM_EXPORT std::enable_shared_from_this<const Geom::BrepData>;
LX_GEOM_EXTERN template class LX_GEOM_EXPORT std::enable_shared_from_this<const Geom::BrepFace>;

namespace Geom
{
class BrepFaceP;
class BrepLoopP;
class BrepDataP;

class LX_GEOM_EXPORT BrepEdge : public std::enable_shared_from_this<const Geom::BrepEdge>
{
public:
};

class LX_GEOM_EXPORT BrepStraight : public Geom::BrepEdge
{
public:
    int from = -1;
    int to = -1;
};

class LX_GEOM_EXPORT BrepArc : public Geom::BrepEdge
{
public:
    int center = -1;
    double radius = 0;
    double trim1 = 0;
    double trim2 = 0;
    bool sense = true;
};

class LX_GEOM_EXPORT BrepFace : public std::enable_shared_from_this<const Geom::BrepFace>
{
public:
    BrepFace(pConstBrepData elem, int idx, size_t itPos);
    virtual ~BrepFace();
    std::vector<int> getModel() const;
    bool getFaceNormal(Geom::Dir& normal, Geom::Pnt& pntOnFace) const;
    pConstBrepLoop getOuterLoop() const;
    std::vector<pConstBrepLoop> getInnerLoops() const;
    pConstBrepData getElement() const;

private:
    BrepFaceP* _pimpl = nullptr;
    BrepFace() {}
};

class LX_GEOM_EXPORT BrepLoop
{
public:
    BrepLoop(pConstBrepFace face, const std::vector<int>& model);
    virtual ~BrepLoop();
    void getPolygon(std::vector<Geom::Pnt>& poly) const;
    std::vector<const Geom::Pnt*> getPolygonPtr() const;
    const std::vector<int>& getModel() const;

private:
    BrepLoop() {}
    BrepLoopP* _pimpl = nullptr;
};

/**
 * @brief The BrepData class holds the boundary representation of a FacetedBrep
 * in the form of a model description and unique points.
 * Each added point has an index. The model is formed by using the indices
 * where '-1' indicates the end of a face and '-2' indicates the end of a loop.
 *
 * Example:
 * model = { 0, 1, 2, 3, -2, -1 }
 *
 * In the BrepData class all points are unique within a given tolerance.
 * The face normals and the outer loop normals must always point outwards
 * (away from the material) while inner loops point inwards.
 * The FacetedBrep can be open or closed.
 *
 * @ingroup
 * @since    24.0
 */

class LX_GEOM_EXPORT BrepData : public std::enable_shared_from_this<const Geom::BrepData>
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    friend class Core::PropertyBrepData;
    friend class Core::PropertyBrepDataSet;
    friend class BrepFace;
    friend class BrepLoop;
    friend class Topo::FaceTool;


    BrepData();
    BrepData(double tolerance);
    ~BrepData(void);

    BrepData(const BrepData& p);
    BrepData(const std::vector<Geom::Pnt>& baseFace, const Geom::Vec& extrude);

    std::vector<Geom::Pnt> getPoints() const;
    int64_t getUniquePointsCnt() const;
    std::vector<int> getModel() const;
    void setModel(const std::vector<int>& model);

    bool checkLoop(const std::vector<int>& model) const;
    bool hasDegeneratedLoops() const;

    /// Adds BrepData to this BrepData
    void add(pConstBrepData data);
    /// Adds a unique point and returns the position of the point
    int addUniquePoint(const Geom::Pnt& p);
    /// Adds a model index and returns the position of the point
    int addModelIndex(int idx);
    /// Throws Base::OutOfRange if index is out of range
    int getModelIndexAt(int idx) const;
    /// Throws Base::OutOfRange if index is out of range
    const Geom::Pnt* getPointAt(int idx) const;
    /// Checks if a point is already in BrepData
    bool hasPoint(const Geom::Pnt& p);
    /// Sets the data structure empty
    void setEmpty();

    /// Checks if the data structure is empty
    bool isEmpty() const;
    /// Returns the number of faces in the Brep
    int getFaceCount() const;

    /// Returns all faces
    std::vector<pConstBrepFace> getFaces() const;
    /// Returns the modeling tolerance of the Brep
    double getModelingTolerance() const { return _tolerance; }
    /// Checks if the BrepData has voids (holes)
    bool hasVoids() const;
    /// Reverses the orientation of all faces
    void reverse();
    /// Lock mutex
    void lock();
    /// Unlock mutex
    void unlock();

    Geom::BrepData& operator=(const Geom::BrepData& rhs);
    bool operator==(const Geom::BrepData& other) const;
    bool operator!=(const Geom::BrepData& other) const;

    void addFace(std::vector<int> index);

    size_t getHash() const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    int64_t addUniquePointCheckIsNew(const Geom::Pnt& p, bool& r_is_new);

    void transform(const Geom::Trsf& T);
    //! Transforms a vector with the transformation T. <br>
    Geom::BrepData transformed(const Geom::Trsf& T) const;

    void dump();
    /// Adds a point at position 'idx'. This is only for fast restoring of saved data. For internal use.
    void _addPointAtIndex(const Geom::Pnt& p, int idx);

private:
    Geom::PointMapWithTolerance uniquePoints;
    std::vector<int> model;
    int highestIndex;
    double _tolerance;

    BrepDataP* _pimpl;
};



}  // namespace Geom
