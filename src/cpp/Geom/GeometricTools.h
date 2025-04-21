#pragma once

#include <Geom/Dir.h>

namespace Geom { class Ax2; }
namespace Geom { class Trsf; }
namespace Geom { class Vec; }


namespace Geom
{
class Pnt;
class Pln;
class Vec2d;

class LX_GEOM_EXPORT GeometricTools
{
public:
    GeometricTools();
    ~GeometricTools();

    /// Throws Base::ConstructionError if construction fails
    static Geom::Dir getFaceNormal(const COORDS& face);
    static Geom::Dir getFaceNormal(const std::vector<Geom::Pnt>& face);

    /// Implements robust Newell's method. Throws Base::ConstructionError if construction fails.
    static Geom::Dir getNFaceNormal(const std::vector<Geom::Pnt>& face);
    static Geom::Dir getNFaceNormal(const COORDS& face);
    // Newell's method without exceptions
    static bool getNFaceNormalNoExc(const std::vector<Geom::Pnt>& face, Geom::Dir& dir);

    /*!
     * Get normal vector for non-convex faces in XY plane.
     * Should be more reliable than getFaceNormal but still do not cover every case.
     * Throws Base::ConstructionError if construction fails.
     */
    static Geom::Dir getConcaveFaceNormalXY(const std::vector<Geom::Pnt>& face);

    static bool getNonColinearEdges(const COORDS& face, Geom::Vec& edge1, Geom::Vec& edge2);
    static int savePoint(const Geom::XYZ& p, COORDS& points);
    static bool isEqual(double d1, double d2, double tolerance = 1E-06);
    static bool isEqual(const Geom::XYZ& v1, const Geom::XYZ& v2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Dir& d1, const Geom::Dir& d2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Vec& v1, const Geom::Vec& v2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Pnt& p1, const Geom::Pnt& p2, double tolerance = 1E-06);
    static double roundValue(double value, double roundValue);
#ifndef LXAPI  // NOT PART OF THE LEXOCAD API (FOR LXSDK AND SWIG)
    static float roundfValue(float value, float roundValue);
#endif
    static double round(double value, int digits);
    static double roundValueOffset(const double& coord, const double& valueToRound, const double& roundToValue);
    static bool isEven(const int Value) { return Value % 2 == 0; }
    static bool isOdd(const int Value) { return Value % 2 == 1; }
    static int factorial(int x) { return x > 1 ? x * factorial(x - 1) : 1; }
    static bool getMedianPlaneFromPoints(const std::vector<Geom::Pnt>& points, Geom::Pln& pln);

private:
    static bool _calculateNonColinearEdges(const COORDS& face, Geom::Vec& edge1, Geom::Vec& edge2);
    static Geom::Dir _getNewellNormal(const COORDS& face);
    static bool _getPredominantEdgesDirXY(const COORDS& face, Geom::Dir& normal);

    // To get the face normal
    static int _checkFaceCounter;
    static unsigned int _checkEdgeIndex;
};

}  // namespace Geom


 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Vec& vec);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Dir& dir);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Pln& dir);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Pnt& pnt);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Vec2d& pnt);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::XYZ& xyz);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Ax2& placement);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const Geom::Trsf& t);
