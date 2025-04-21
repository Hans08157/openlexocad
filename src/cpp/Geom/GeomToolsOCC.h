#pragma once

#include <gp_Ax22d.hxx>
#include <gp_Circ.hxx>
#include <gp_Circ2d.hxx>
#include <gp_GTrsf.hxx>
#include <gp_Lin.hxx>
#include <gp_Lin2d.hxx>
#include <gp_Pln.hxx>
#include <gp_Vec.hxx>
#include <gp_Vec2d.hxx>

#include <Geom/Circ.h>
#include <Geom/Circ2d.h>
#include <Geom/Lin.h>
#include <Geom/Lin2d.h>
#include <Geom/Pln.h>
#include <Geom/Trsf.h>
#include <Geom/Vec.h>

namespace Geom
{
class LX_GEOM_EXPORT GeomToolsOCC
{
public:
    static bool isEqual(const gp_XYZ& v1, const gp_XYZ& v2, double tolerance = 1E-06);
    static bool isEqual(const gp_XY& v1, const gp_XY& v2, double tolerance = 1E-06);
    static bool isEqual(const gp_Dir& d1, const gp_Dir& d2, double tolerance = 1E-06);
    static bool isEqual(const gp_Dir2d& d1, const gp_Dir2d& d2, double tolerance = 1E-06);
    static bool isEqual(const gp_Vec& v1, const gp_Vec& v2, double tolerance = 1E-06);
    static bool isEqual(const gp_Vec2d& v1, const gp_Vec2d& v2, double tolerance = 1E-06);
    static bool isEqual(const gp_Pnt& p1, const gp_Pnt& p2, double tolerance = 1E-06);
    static bool isEqual(const gp_Pnt2d& p1, const gp_Pnt2d& p2, double tolerance = 1E-06);
    static bool isEqual(const gp_Ax1& a1, const gp_Ax1& a2, double tolerance = 1E-06);
    static bool isEqual(const gp_Ax2& a1, const gp_Ax2& a2, double tolerance = 1E-06);
    static bool isEqual(const gp_Ax3& a1, const gp_Ax3& a2, double tolerance = 1E-06);
    static bool isEqual(const gp_Ax22d& a1, const gp_Ax22d& a2, double tolerance = 1E-06);
    static bool isEqual(const gp_Trsf& t1, const gp_Trsf& t2, double tolerance = 1E-06);
    static bool isEqual(const gp_GTrsf& t1, const gp_GTrsf& t2, double tolerance = 1E-06);



    static Geom::Ax1 to_CA_Axis1(const gp_Ax1& value);
    static gp_Ax2 to_gp_Ax2(const Geom::Ax2& value);
    static Geom::Ax2 to_CA_Axis2(const gp_Ax2& value);
    static Geom::Ax22d to_CA_Ax22d(const gp_Ax22d& value);
    static gp_Ax2d to_gp_Ax2d(const Geom::Ax2d& value);
    static gp_Ax22d to_gp_Ax22d(const Geom::Ax22d& value);
    static gp_Pnt to_gp_Pnt(const Geom::Pnt& value);
    static gp_Pnt to_gp_Pnt(const Geom::XYZ& value);
    static Geom::Pnt to_CA_Point(const gp_Pnt& value);
    static Geom::Pnt to_CA_Point(const gp_Pnt2d& value, const Geom::Pln& pln);
    static gp_Vec to_gp_Vec(const Geom::Vec& value);
    static gp_Vec to_gp_Vec(const Geom::XYZ& value);
    static Geom::Vec to_CA_Vector(const gp_Vec& value);
    static gp_Dir to_gp_Dir(const Geom::Dir& value);
    static gp_Pnt2d to_gp_Pnt2d(const Geom::Pnt2d& value);
    static Geom::Pnt2d to_CA_Pnt2d(const gp_Pnt2d& value);
    static gp_Vec2d to_gp_Vec2d(const Geom::Vec2d& value);
    static gp_Dir2d to_gp_Dir2d(const Geom::Dir2d& value);
    static gp_Lin2d to_gp_Lin2d(const Geom::Lin2d& value);
    static Geom::Dir to_CA_Direction(const gp_Dir& value);
    static gp_Trsf to_gp_Trsf(const Geom::Trsf& value);
    static gp_GTrsf to_gp_GTrsf(const Geom::GTrsf& value);
    static gp_Mat to_gp_Mat(const Geom::Mat& value);
    static Geom::Trsf to_CA_Transform(const gp_Trsf& value);
    static gp_Pln to_gp_Pln(const Geom::Pln& value);
    static Geom::Pln to_CA_Plane(const gp_Pln& value);
    static gp_Lin to_gp_Lin(const Geom::Lin& value);
    static Geom::Lin to_CA_Line(const gp_Lin& value);
    static Geom::Circ to_CA_Circle(const gp_Circ& value);
    static Geom::Circ2d to_CA_Circle2d(const gp_Circ2d& value);
    static gp_Ax1 to_gp_Ax1(const Geom::Ax1& value);
    static gp_Circ to_gp_Circ(const Geom::Circ& value);
    static gp_Circ2d to_gp_Circ2d(const Geom::Circ2d& value);
    static gp_Lin2d to_gp_Lin2d(const Geom::Lin& lin, const Geom::Pln& pln);
    static gp_Lin to_gp_Lin(const gp_Lin2d& gpLin2d, const gp_Pln& gpPln);
    static gp_Pnt2d to_gp_Pnt2d(const Geom::Pnt& pnt, const Geom::Pln& pln);
    static gp_Circ to_gp_Circ(const gp_Circ2d& gpCirc2d, const gp_Pln& gpPln);
    static gp_Circ to_gp_Circ(const gp_Circ2d& gpCirc2d, const Geom::Pln& pln);
    static void debugOccTransform(const gp_Trsf& transform, const std::string& msg = "");
    static void debugOccTransform(const gp_GTrsf& transform, const std::string& msg = "");

private:
};

}  // namespace Geom


 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Vec& vec);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Dir& dir);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Pln& dir);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Pnt& pnt);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_XYZ& xyz);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Ax2& placement);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Vec2d& vec);
 LX_GEOM_EXPORT  std::ostream& operator<<(std::ostream& o, const gp_Trsf& t);
