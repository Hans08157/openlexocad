#pragma once

#include <Geom/BSPTree.h>
#include <Geom/Pnt2d.h>

namespace Geom { class Pnt; }

namespace Geom
{
class LX_GEOM_EXPORT PointMapWithTolerance
{
public:
    PointMapWithTolerance(const double& tol = 1E-06);
    PointMapWithTolerance(const PointMapWithTolerance& other);  // copy constructor

    int64_t numPoints() const;
    void clear();
    int64_t find(const Geom::Pnt& p) const;
    const Geom::Pnt& getPoint(const int64_t idx) const;
    int64_t getUserData(int64_t idx) const;
    void setUserData(int64_t idx, int64_t userData);
    void* getUserDataVoidPtr(int64_t idx) const;
    void setUserDataVoidPtr(int64_t idx, void* userData);
    int64_t addPoint(const Geom::Pnt& p, int64_t userData);       // it doesn't check if point exists with tolerance
    int64_t addPointVoidPtr(const Geom::Pnt& p, void* userData);  // it doesn't check if point exists with tolerance
    int64_t addPointIfNotExists(const Geom::Pnt& p, int64_t userData);
    int64_t addPointIfNotExistsVoidPtr(const Geom::Pnt& p, void* userData);
    void removePoint(const int64_t idx);

    bool operator==(const PointMapWithTolerance& other) const;

private:
    Geom::BSPTree _bsptree;
    double _tol;
};


// for convenience
class LX_GEOM_EXPORT Point2dMapWithTolerance
{
public:
    Point2dMapWithTolerance(const double& tol = 1E-06);

    int64_t numPoints();
    void clear();
    int64_t find(const Geom::Pnt2d& p);
    const Geom::Pnt2d getPoint(const int64_t idx) const;
    int64_t getUserData(int64_t idx);
    void setUserData(int64_t idx, int64_t userData);
    void addPoint(const Geom::Pnt2d& p, int64_t userData);  // it doesn't check if point exists with tolerance
    void addPointIfNotExists(const Geom::Pnt2d& p, int64_t userData);

private:
    Geom::BSPTree _bsptree;
    double _tol;
};

}  // namespace Geom
