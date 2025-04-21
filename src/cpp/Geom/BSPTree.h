#pragma once

#include <vector>



namespace Geom
{
class Pnt;
class Sphr;
class base_bspnode;

// *************************************************************************

class LX_GEOM_EXPORT BSPTree
{
public:
    BSPTree(const int64_t maxnodepts = 64, const int64_t initsize = 4);
    BSPTree(const BSPTree& other);  // Copy constructor
    ~BSPTree();

    int64_t numPoints() const;
    const Geom::Pnt& getPoint(const int64_t idx) const;
    void getPoint(const int64_t idx, Geom::Pnt& pt) const;
    void* getUserData(const int64_t idx) const;
    void setUserData(const int64_t idx, void* const data);

    int64_t addPoint(const Geom::Pnt& pt, void* const userdata = nullptr);
    int64_t removePoint(const Geom::Pnt& pt);
    void removePoint(const int64_t idx);
    int64_t findPoint(const Geom::Pnt& pos) const;
    void clear();
    void findPoints(const Geom::Sphr& sphere, std::vector<int64_t>& array) const;
    int64_t findClosest(const Geom::Sphr& sphere, std::vector<int64_t>& array) const;
    void findPoints(const Geom::Pnt& pnt, const double& tol, std::vector<int64_t>& array) const;
    int64_t findClosest(const Geom::Pnt& pnt, const double& tol, std::vector<int64_t>& array) const;
    int64_t findClosest(const Geom::Pnt& pnt, const double& tol) const;

    static void removeFast(std::vector<int64_t>& array, int64_t idx);
    static void removeFast(std::vector<Geom::Pnt>& array, int64_t idx);
    static void removeFast(std::vector<void*>& array, int64_t idx);

    bool operator==(const BSPTree& other) const;
    BSPTree& operator=(const BSPTree& rhs);

private:
    friend class base_bspnode;
    std::vector<Geom::Pnt> pointsArray;
    std::vector<void*> userdataArray;
    base_bspnode* topnode;
    int64_t maxnodepoints;
};

}  // namespace Geom
