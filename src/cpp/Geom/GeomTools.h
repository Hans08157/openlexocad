#pragma once
#include <Geom/ToolResults.h>
#include <Geom/Trsf.h>
#include <Geom/Vec.h>
#include <Geom/Dir2d.h>        // for Dir2d
#include <Geom/Pnt2d.h>        // for Pnt2d
namespace Geom { class Ax22d; }
namespace Geom { class Ax2d; }
namespace Geom { class Bnd_Box; }
namespace Geom { class Circ; }
namespace Geom { class GTrsf; }
namespace Geom { class Vec2d; }
namespace Geom { class XY; }

namespace Geom
{
enum Qualifier
{
    ENCLOSING,
    ENCLOSED,
    OUTSIDE,
    UNQUALIFIED
};

class LX_GEOM_EXPORT GeomTools
{
public:
    GeomTools(void);
    ~GeomTools(void);

    /// Throws Base::ConstructionError if construction fails
    static Geom::Pln makePlaneFrom3Points(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& p3, Geom::Ax2& coordSystem);
    /// Throws Base::ConstructionError if construction fails
    static Geom::Lin makeLineFrom2Points(const Geom::Pnt& p1, const Geom::Pnt& p2);

    /// Throws Base::FailedNotDone if projection fails
    static Geom::Pnt projectPointOnPlane(const Geom::Pnt& p, const Geom::Pln& plane);
    static Geom::Pnt projectPointOnPlane(const Geom::Pnt& p, const Geom::Pln& plane, double& U, double& V);
    static bool isPointOnPlane(const Geom::Pnt& p, const Geom::Pln& plane, double tolerance = 1E-06);

    /// Throws Base::FailedNotDone if projection fails
    static Geom::Pnt projectPointOnLine(const Geom::Pnt& p, const Geom::Lin& line);
    static Geom::Pnt projectPointOnLine(const Geom::Pnt& p, const Geom::Lin& line, double& U);

    /// Throws Base::FailedNotDone if projection fails
    static Geom::Pnt projectPointOnCircle(const Geom::Pnt& p, const Geom::Circ& circle);

    /// Never throws
    static Geom::Pnt midpoint(const Geom::Pnt& p1, const Geom::Pnt& p2);
    static Geom::Pnt2d midpoint(const Geom::Pnt2d& p1, const Geom::Pnt2d& p2);

    static double getAngleWithPlane(const Geom::Vec& v, const Geom::Pln& plane);
    static double getAngleBetweenVectors(const Geom::Vec& v1, const Geom::Vec& v2);
    static void angleBetween(const Geom::Vec& v1, const Geom::Vec& v2, Geom::Vec& axis, double& angle);

    struct AngleParams
    {
        Geom::Pnt e1p1;
        Geom::Pnt e1p2;
        Geom::Pnt e2p1;
        Geom::Pnt e2p2;
        Geom::Pnt pntOnEdge1;
        Geom::Pnt pntOnEdge2;
        Geom::Pln plane;
        bool secondViewerMode;
    };
    struct Angle3Points
    {
        Geom::Pnt startPoint;
        Geom::Pnt endPoint;
        Geom::Pnt apexPoint;
        bool pointsFound;
    };
    static Angle3Points get3AnglePoints(AngleParams ap);

    /// Throws Base::ConstructionError if points are identical fails
    static Geom::Ax2 makeAxisPlacementFrom2Points(const Geom::Pnt& p1, const Geom::Pnt& p2, double& xLength, double& angleXYPlane);
    static double getDistanceBetween2Points(const Geom::Pnt& p1, const Geom::Pnt& p2);
    static Geom::Pnt findClosestPointToPoints(const Geom::Pnt& pnt, const std::vector<Geom::Pnt>& pnts);

    static bool isEqual(double v1, double v2, double tolerance = 1E-06);
    static bool isEqual(const Geom::XYZ& v1, const Geom::XYZ& v2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Pnt& p1, const Geom::Pnt& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Vec& v1, const Geom::Vec& v2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Dir& d1, const Geom::Dir& d2, double tolerance = 1E-06);
    static bool isEqual(const Geom::XY& p1, const Geom::XY& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Pnt2d& p1, const Geom::Pnt2d& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Vec2d& p1, const Geom::Vec2d& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Dir2d& p1, const Geom::Dir2d& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Ax1& a1, const Geom::Ax1& a2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Ax2& a1, const Geom::Ax2& a2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Ax2d& a1, const Geom::Ax2d& a2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Ax3& a1, const Geom::Ax3& a2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Trsf& t1, const Geom::Trsf& t2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Ax22d& a1, const Geom::Ax22d& a2, double tolerance = 1E-06);
    static bool isEqual(const Geom::GTrsf& t1, const Geom::GTrsf& t2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Pln& p1, const Geom::Pln& p2, double tolerance = 1E-06);
    static bool isEqual(const Geom::Bnd_Box& b1, const Geom::Bnd_Box& b2, double tolerance = 1E-06);

    static bool intersectLineWithLine(const Geom::Lin& lin1, const Geom::Lin& lin2, Geom::Pnt& intersectPnt, double tolerance = 1E-06);
    static bool intersectDirWithDir(const Geom::Dir& dir1,
                                    const Geom::Pnt& pnt1,
                                    const Geom::Dir& dir2,
                                    const Geom::Pnt& pnt2,
                                    Geom::Pnt& intersection);
    static Geom::Pnt intersectLineWithPlane(const Geom::Lin& lin, const Geom::Pln& plane);
    static bool intersectLineWithPlane(const Geom::Lin& lin, const Geom::Pln& plane, Geom::Pnt& intersection);  // no exception version
    static bool intersectBBoxWithPlane(const Geom::Bnd_Box& box, const Geom::Pln& plane);
    static bool intersectLineWithBoundedRect(const Geom::Lin& lin, const Geom::Pnt& rectPoint1, const Geom::Pnt& rectPoint2, Geom::Pnt& result);
    static bool intersectPlaneWithPlane(const Geom::Pln& plnA, const Geom::Pln& plnB, Geom::Lin& line, double tolerance = 1e-6);
    static bool intersectLineWithBBox(const Geom::Lin& lin, const Geom::Bnd_Box& bbox, Geom::Pnt& pnear, Geom::Pnt& pfar, double epsilon = 0.0);
    static bool makePlaneFrom2Lines(const Geom::Lin& lin1, const Geom::Lin& lin2, Geom::Pln& plane);
    static bool makeCircleFrom3Points(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& p3, Geom::Circ& circle);
    static bool makeCirclesFrom2TangentsAndRadius(const Geom::Lin& lin1,
                                                  const Geom::Lin& lin2,
                                                  double radius,
                                                  std::vector<Geom::Circ>& circles,
                                                  std::vector<Geom::Pnt>& pnt1,
                                                  std::vector<Geom::Pnt>& pnt2,
                                                  std::vector<double>& paramOnLin1,
                                                  std::vector<double>& paramOnLin2,
                                                  std::vector<double>& paramOnCirclesFromLin1,
                                                  std::vector<double>& paramOnCirclesFromLin2,
                                                  Geom::Qualifier qualif1 = Geom::UNQUALIFIED,
                                                  Geom::Qualifier qualif2 = Geom::UNQUALIFIED,
                                                  double tolerance = 1E-06);
    static bool makeCirclesFrom2TangentsAndCenterOnLine(const Geom::Lin& lin1,
                                                        const Geom::Lin& lin2,
                                                        const Geom::Lin& lin3,
                                                        std::vector<Geom::Circ>& circles,
                                                        std::vector<Geom::Pnt>& pnt1,
                                                        std::vector<Geom::Pnt>& pnt2,
                                                        std::vector<double>& paramOnLin1,
                                                        std::vector<double>& paramOnLin2,
                                                        std::vector<double>& paramOnCirclesFromLin1,
                                                        std::vector<double>& paramOnCirclesFromLin2,
                                                        Geom::Qualifier qualif1 = Geom::UNQUALIFIED,
                                                        Geom::Qualifier qualif2 = Geom::UNQUALIFIED,
                                                        double tolerance = 1E-06);
    static bool makeLinePerpendicularToLineThroughPoint(const Geom::Pln& plane,
                                                        const Geom::Pnt& thruPnt,
                                                        const Geom::Lin& line,
                                                        Geom::Lin& solution,
                                                        Geom::Pnt& point,
                                                        double& paramOnLine,
                                                        double& paramOnSolution);
    static bool make2DLines_Tangent2Circles(const Geom::Circ& circle1,
                                            const Geom::Circ& circle2,
                                            std::vector<Geom::Lin>& lines,
                                            std::vector<Geom::Pnt>& tangentPoints1,
                                            std::vector<Geom::Pnt>& tangentPoints2);
    static bool make2DLines_TangentCirclePoint(const Geom::Circ& circle,
                                               const Geom::Pnt& point,
                                               std::vector<Geom::Lin>& lines,
                                               std::vector<Geom::Pnt>& tangentPoints);
    static bool makeLines_BisLineLine(const Geom::Lin l1, const Geom::Lin l2, std::vector<Geom::Lin>& result);
    static bool make2DCircles_RadiusPointPoint(double radius, const Geom::Pnt& point1, const Geom::Pnt& point2, std::vector<Geom::Circ>& result);
    static bool makeCircles_RadiusLinePoint(double radius, const Geom::Lin& line, const Geom::Pnt& point, std::vector<Geom::Circ>& result);
    static bool makeCircles_RadiusCirclePoint(double radius, const Geom::Circ& circle, const Geom::Pnt& point, std::vector<Geom::Circ>& result);
    static bool makeCircles_RadiusLineLine(double radius, const Geom::Lin& line1, const Geom::Lin& line2, std::vector<Geom::Circ>& result);
    static bool makeCircles_RadiusLineCircle(double radius, const Geom::Lin& line, const Geom::Circ& circle, std::vector<Geom::Circ>& result);
    static bool makeCircles_RadiusCircleCircle(double radius, const Geom::Circ& circle1, const Geom::Circ& circle2, std::vector<Geom::Circ>& result);
    static double calculateAngleFrom3Points(const Geom::Pnt& first, const Geom::Pnt& center, const Geom::Pnt& second, const Geom::Vec& refVec);
    static double getSignedDistanceFromPointToPlane(const Geom::Pnt& p, const Geom::Pln& plane);
    static double convertRadianToDegree(double radValue);
    static double convertDegreeToRadian(double degValue);
    static double convertPercentToRadian(double percentValue);
    static double convertRadianToPercent(double radValue);
    static Geom::Pnt getNormalizedCoordinatesRelativeToBndBox(const Geom::Bnd_Box& box, const Geom::Pnt& p);
    static Geom::Pnt getCoordinatesFromNormalizedRelativeToBndBox(const Geom::Bnd_Box& box, const Geom::Pnt& p);
    static void getAnglesFromPosition(const Geom::Ax2& position, double& rotx, double& roty, double& rotz);
    static bool pointsOnSamePlane(const std::vector<Geom::Pnt>& inVector, Geom::Pln& outPlane);
    static bool pointsAreCollinear(const std::vector<Geom::Pnt>& inVector);
    static void debugOccTransform(const Geom::GTrsf& transform, const std::string& msg = "");
    static void debugOccTransform(const Geom::Trsf& transform, const std::string& msg = "");
    static bool getUnitCylinderLineIntersection(const Geom::Pnt& lineStart,
                                                                 const Geom::Pnt& lineEnd,
                                                                 Geom::Pnt& isectFront,
                                                                 Geom::Pnt& isectBack);
    static bool getCylinderLineIntersection(Geom::Ax2& cylinder_ax,
                                                             const double& cylinder_radius,
                                                             const Geom::Pnt& lineStart,
                                                             const Geom::Pnt& lineEnd,
                                                             Geom::Pnt& isectFront,
                                                             Geom::Pnt& isectBack);
    static Geom::Vec getClosestAxis(const Geom::Vec& vec);
    static int gcd(int a, int b);
    static void circumscribeSphereAroundBox(Geom::Bnd_Box box, Geom::Vec& center, double& radius);
    static bool getIntersectionWithTriangle(const Geom::Pnt& p1,
                                            const Geom::Pnt& p2,
                                            const Geom::Pnt& p3,
                                            const Geom::Pnt& pickedPnt,
                                            Geom::Pnt& intersection);
    static void calculatePositionToViewBoundingBoxForDefaultView(Geom::Bnd_Box bbox,
                                                                 Geom::Vec direction,
                                                                 float aspectRatio,
                                                                 double heightAngle,
                                                                 Geom::Vec& position,
                                                                 Geom::Vec& center);
    static Geom::Pnt lineValue(const double& u, const Geom::Ax1& ax1);
    static bool computeComplemetaryAngle(const Geom::Pnt& P1, const Geom::Pnt& S, const Geom::Pnt& P2, double& radians);
    static bool computeClothoidMaxR(const double& radians, const double& TG, double& R);  ///
    static Geom::Trsf computeTrsfFromAx2(const Geom::Ax2& worldAxis);
    static bool isConvexPolyon(const std::vector<Geom::Pnt>& inVector);
    static bool isConvexPolyon(const std::vector<int>& inModel, const std::vector<Geom::Pnt>& inVector);
    static bool rayTriangleIntersect(const Geom::Vec& orig,
                                     const Geom::Vec& dir,
                                     const Geom::Vec& v0,
                                     const Geom::Vec& v1,
                                     const Geom::Vec& v2,
                                     float& t,
                                     float& u,
                                     float& v);
    static bool centroid(Geom::Pnt& ret_centroid, std::vector<Geom::Pnt>& pnts);
    static bool testRayThruTriangle(const Geom::Pnt& P1,
                                    const Geom::Pnt& P2,
                                    const Geom::Pnt& P3,
                                    const Geom::Dir& normal,
                                    const Geom::Lin& ray,
                                    Geom::Pnt& PIP);

    /** @name Interfaces modified for Python Bindings */
    //@{
    static GT_MakePlaneFrom3Points_Result makePlaneFrom3Points(const Geom::Pnt& p1, const Geom::Pnt& p2, const Geom::Pnt& p3);
    static GT_MakeLineFrom2Points1_Result makeLineFrom2Points1(const Geom::Pnt& p1, const Geom::Pnt& p2);
    static GT_ProjectPointOnPlane1_Result projectPointOnPlane1(const Geom::Pnt& p, const Geom::Pln& plane);
    static GT_ProjectPointOnPlane2_Result projectPointOnPlane2(const Geom::Pnt& p, const Geom::Pln& plane);
    static GT_ProjectPointOnLine1_Result projectPointOnLine1(const Geom::Pnt& p, const Geom::Lin& line);
    static GT_ProjectPointOnLine2_Result projectPointOnLine2(const Geom::Pnt& p, const Geom::Lin& line);
    static GT_ProjectPointOnCircle1_Result projectPointOnCircle1(const Geom::Pnt& p, const Geom::Circ& circle);
    static GT_MakeAxisPlacementFrom2Points_Result makeAxisPlacementFrom2Points(const Geom::Pnt& p1, const Geom::Pnt& p2);
    //@}
};

}  // namespace Geom
