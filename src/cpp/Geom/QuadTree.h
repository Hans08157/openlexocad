#pragma once

#include <Base/Color.h>
#include <Geom/Pnt.h>
#include <Geom/Rect.h>
#include <Geom/Bnd_Box.h>

#include <deque>
#include <concurrent_vector.h>

struct FloatPoint
{
    FloatPoint(const float v[3]) { vec[0] = v[0]; vec[1] = v[1]; vec[2] = v[2]; }
    FloatPoint(float x, float y, float z) { vec[0] = x; vec[1] = y; vec[2] = z; }    
    float vec[3];
    float x() const { return vec[0]; }
    float y() const { return vec[1]; }
    float z() const { return vec[2]; }
};

namespace Geom
{
class QuadTree;

class QuadTreeIterator
{
    QuadTreeIterator(QuadTree* q) : _start(q), _current(q){};

    bool operator==(const QuadTreeIterator& b) const { return (b._current == _current); }

    QuadTreeIterator& operator++() { return *this; }


    QuadTree* _current;
    const QuadTree* _start;
};

class LX_GEOM_EXPORT ColorPoint
{
public:
    ColorPoint(){};
    ColorPoint(const Geom::Pnt& p, const Base::MColor& c) : p(p), c(c){};
    Geom::Pnt p;
    Base::MColor c;
};


class PointStorage
{
public:
    using container = std::deque<ColorPoint>;
    using iterator = typename container::iterator;
    using const_iterator = typename container::const_iterator;

    void addPoint(const ColorPoint& p) { mData.emplace_back(p); };
    iterator begin() { return mData.begin(); }
    iterator end() { return mData.end(); }
    const_iterator begin() const { return mData.begin(); }
    const_iterator end() const { return mData.end(); }
    const_iterator cbegin() const { return mData.cbegin(); }
    const_iterator cend() const { return mData.cend(); }

    void clear() { mData.clear(); };
    bool empty() const  { return mData.empty(); };

    const container& getData() const { return mData; }


private:

    container mData;


};

class LX_GEOM_EXPORT QuadTree
{
public:
    QuadTree(Geom::Rect boundary, size_t capacity, int myDeep = 1);
    virtual ~QuadTree();

    bool insert(const Geom::ColorPoint& cp);

    const Geom::Rect& getBoundary() const;
    const std::deque<Geom::ColorPoint>& getPoints() const;
    const bool hasPoints() const;
    const size_t getPointCount() const;
    std::vector<QuadTree*> getChildren() const;

    void getPointsRecursive(std::deque<Geom::ColorPoint>& points);
    const size_t getPointCountRecursive() const;
    std::vector<QuadTree*> getChildrenRecursive() const;
    void removePointsRecursive();

    void setAutoSplit(bool on);
    void split();
    void setDeep(int deep);
    int getDeep();


    // Children
    QuadTree* northWest;
    QuadTree* northEast;
    QuadTree* southWest;
    QuadTree* southEast;

    QuadTreeIterator begin();
    QuadTreeIterator end();


private:
    void getDeep(int& deep);

    QuadTree();

    // Arbitrary constant to indicate how many elements can be stored in this quad tree node capacity
    size_t _capacity;

    int m_myDeep;
    int m_maxDeep;

    // Axis-aligned bounding box stored as a center with half-dimensions
    // to represent the boundaries of this quad tree
    Geom::Rect _boundary;

    // Points in this quad tree node
    PointStorage _points;

    size_t _pointCount;

    bool _autoSplit;
};


class PointStorageMT
{
public:
    using container = concurrency::concurrent_vector<ColorPoint>;
    using iterator = typename container::iterator;
    using const_iterator = typename container::const_iterator;

    const_iterator begin() const { return mData.begin(); }
    const_iterator end() const { return mData.end(); }
    const_iterator cbegin() const { return mData.cbegin(); }
    const_iterator cend() const { return mData.cend(); }

    void addPoint(const ColorPoint& p) { mData.push_back(p); };        

    void clear() { mData.clear(); };
    bool empty() const  { return mData.empty(); };

    const container& getData() const { return mData; }


private:

    container mData;


};

class LX_GEOM_EXPORT QuadTreeMT
{
public:
    struct LOD_Data
    {
        std::vector<FloatPoint> points_level_1_0;
        std::vector<FloatPoint> points_level_0_5;
        std::vector<FloatPoint> points_level_0_1;

        std::vector<uint32_t> colors_level_1_0;
        std::vector<uint32_t> colors_level_0_5;
        std::vector<uint32_t> colors_level_0_1;
        
    };

    QuadTreeMT(Geom::Rect boundary, size_t capacity);
    QuadTreeMT* findQuadTree(const FloatPoint& cp);
    QuadTreeMT* findQuadTree(const Geom::Pnt &p);
    virtual ~QuadTreeMT();

    bool insert(const FloatPoint& fp, const uint32_t color );

    const Geom::Rect& getBoundary() const;
    std::vector<FloatPoint> getPoints() const;
    std::vector<uint32_t>   getColors() const;
    const bool hasPoints() const;
    const size_t getPointCount() const;
    std::vector<QuadTreeMT*> getChildren() const;

    const size_t getPointCountRecursive() const;
    std::vector<QuadTreeMT*> getChildrenRecursive() const;
    void removePointsRecursive();
        
    void setBBox( Geom::Bnd_Box b ) { _bbox = b; }
    Geom::Bnd_Box getBBox(  ) { return _bbox; }
    std::vector<QuadTreeMT*> setDeep(int deep);
    int getDeep();


    // Children
    QuadTreeMT* northWest;
    QuadTreeMT* northEast;
    QuadTreeMT* southWest;
    QuadTreeMT* southEast;


    void putInQuadTree(const std::vector<FloatPoint>& points, const std::vector<uint32_t>& colors );
    void countsInQuadTree(const std::vector<FloatPoint>& points, const std::vector<uint32_t>& colors);

    const std::vector<LOD_Data>& createLOD_Data();
    const std::vector<LOD_Data>& getLOD_Data() {  return mLOD_Data; };

    std::atomic<uint64_t> mCountOfPoints = 0;
    

private:

    std::vector<LOD_Data> mLOD_Data;

    void getDeep(int& deep);
    void split();
    void setDeep(int deep, std::vector<QuadTreeMT*>& leafNodes);
    QuadTreeMT();

    // Arbitrary constant to indicate how many elements can be stored in this quad tree node capacity
    size_t _capacity;

    int m_myDeep;
    int m_maxDeep;

    // Axis-aligned bounding box stored as a center with half-dimensions
    // to represent the boundaries of this quad tree
    Geom::Rect _boundary;
    Geom::Bnd_Box _bbox;

    // Points in this quad tree node
    concurrency::concurrent_vector<FloatPoint> _points;
    concurrency::concurrent_vector<uint32_t>   _colors;
    
    
};




}  // namespace Geom
