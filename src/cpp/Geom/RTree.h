#pragma once

#include <Geom/Bnd_Box.h>
#include <boost/geometry/index/rtree.hpp>


namespace Geom
{
class Pnt;
class Pnt2d;

namespace RTree
{
    // Convenient namespaces
    namespace bg = boost::geometry;
    namespace bgm = boost::geometry::model;
    namespace bgi = boost::geometry::index;

    // Convenient types 3d
    typedef bgm::point<double, 3, bg::cs::cartesian> Point;
    typedef bgm::segment<Point> Segment;
    typedef bg::model::box<Point> Box;

    typedef std::pair<Segment, uintptr_t> SegmentValue;
    typedef bgi::rtree<SegmentValue, bgi::rstar<16> > SegmentRTree;

    typedef std::pair<Point, uintptr_t> PointValue;
    typedef bgi::rtree<PointValue, bgi::rstar<16> > PointRTree;

    typedef std::pair<Box, uintptr_t> BoxValue;
    typedef bgi::rtree<BoxValue, bgi::rstar<16> > BoxRTree;

    LX_GEOM_EXPORT Point getPoint(const Geom::Pnt& p);
    LX_GEOM_EXPORT Box getBox(const Geom::Pnt& p, const double& radius);
    LX_GEOM_EXPORT Box getBox(const Geom::Bnd_Box& bbox);

    LX_GEOM_EXPORT PointValue getPointValue(const Geom::Pnt& p, uintptr_t userData);
    LX_GEOM_EXPORT BoxValue getBoxValue(const Bnd_Box& bbox, uintptr_t userData);

    // Convenient types 2d
    typedef bgm::point<double, 2, bg::cs::cartesian> Point2d;
    typedef bgm::segment<Point2d> Segment2d;
    typedef bg::model::box<Point2d> Box2d;

    typedef std::pair<Segment2d, uintptr_t> Segment2dValue;
    typedef bgi::rtree<Segment2dValue, bgi::rstar<16> > Segment2dRTree;

    typedef std::pair<Point2d, uintptr_t> Point2dValue;
    typedef bgi::rtree<Point2dValue, bgi::rstar<16> > Point2dRTree;

    typedef std::pair<Box2d, uintptr_t> Box2dValue;
    typedef bgi::rtree<Box2dValue, bgi::rstar<16> > Box2dRTree;

    LX_GEOM_EXPORT Box2d getBox2d(const double& minx, const double& miny, const double& maxx, const double& maxy);
    LX_GEOM_EXPORT Box2d getBox2d(const Geom::Pnt2d& p, const double& radius);
    LX_GEOM_EXPORT Box2d getBox2d(const Geom::Bnd_Box& bbox);

    LX_GEOM_EXPORT Box2dValue getBox2dValue(const double& minx, const double& miny, const double& maxx, const double& maxy, uintptr_t userData);
    LX_GEOM_EXPORT Box2dValue getBox2dValue(const Geom::Bnd_Box& bbox, uintptr_t userData);
}  // namespace RTree


class LX_GEOM_EXPORT BoxRTree
{
public:
    struct Value
    {
        Geom::Bnd_Box bbox;
        uintptr_t userData;
    };

    BoxRTree();
    BoxRTree(const std::vector<Value>& values);  // building of tree is faster with this constructor
    BoxRTree(const BoxRTree& other);             // copy constructor
    ~BoxRTree();

    void insert(const Bnd_Box& bbox, uintptr_t userData);
    void insert(const Value& value);
    bool remove(const Bnd_Box& bbox, uintptr_t userData);  // removes only one value from the container
    bool remove(const Value& value);                       // removes only one value from the container

    void queryIntersects(const Bnd_Box& bbox, std::vector<uintptr_t>& userDataVec) const;

private:
    RTree::BoxRTree* _tree;
};


class LX_GEOM_EXPORT Box2dRTree
{
public:
    struct Value
    {
        Geom::Bnd_Box bbox;
        uintptr_t userData;
    };

    Box2dRTree();
    Box2dRTree(const std::vector<Value>& values);  // building of tree is faster with this constructor
    Box2dRTree(const Box2dRTree& other);           // copy constructor
    ~Box2dRTree();

    void insert(const Bnd_Box& bbox, uintptr_t userData);
    void insert(const Value& value);
    bool remove(const Bnd_Box& bbox, uintptr_t userData);  // removes only one value from the container
    bool remove(const Value& value);                       // removes only one value from the container

    void queryIntersects(const Bnd_Box& bbox, std::vector<uintptr_t>& userDataVec) const;
    void queryIntersects(const RTree::Box2d& bbox, std::vector<uintptr_t>& userDataVec) const;
    bool hasIntersection(const Bnd_Box& bbox) const;       // has at least one intersection
    bool hasIntersection(const RTree::Box2d& bbox) const;  // has at least one intersection

private:
    RTree::Box2dRTree* _tree;
};
}  // namespace Geom
