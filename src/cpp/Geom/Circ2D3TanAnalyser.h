#pragma once

#include <Geom/Circ2d.h>


class GccAna_Circ2d3Tan;

namespace Geom
{
class Lin2d;
class LX_GEOM_EXPORT Circ2D3TanAnalyser
{
public:
    Circ2D3TanAnalyser(const Geom::Lin2d& line1, const Geom::Lin2d& line2, const Geom::Lin2d& line3);
    Circ2D3TanAnalyser(const Geom::Circ2d& circ1, const Geom::Circ2d& circ2, const Geom::Circ2d& circ3);
    Circ2D3TanAnalyser(const Geom::Lin2d& line1, const Geom::Lin2d& line2, const Geom::Circ2d& circle);
    Circ2D3TanAnalyser(const Geom::Lin2d& line1, const Geom::Lin2d& line2, const Geom::Pnt2d& point);
    Circ2D3TanAnalyser(const Geom::Lin2d& line, const Geom::Circ2d& circ1, const Geom::Circ2d& circ2);
    Circ2D3TanAnalyser(const Geom::Lin2d& line, const Geom::Circ2d& circ, const Geom::Pnt2d& poinjt);
    Circ2D3TanAnalyser(const Geom::Lin2d& line, const Geom::Pnt2d& point1, const Geom::Pnt2d& point2);
    Circ2D3TanAnalyser(const Geom::Circ2d& circ1, const Geom::Circ2d& circ2, const Geom::Pnt2d& point);
    Circ2D3TanAnalyser(const Geom::Circ2d& circ, const Geom::Pnt2d& point1, const Geom::Pnt2d& point2);
    ~Circ2D3TanAnalyser();

    bool isDone() const;
    int numberSulutions() const;

    Geom::Circ2d getSolution(int index) const;
    bool tangentPoint1(int index, Geom::Pnt2d& result) const;
    bool tangentPoint2(int index, Geom::Pnt2d& result) const;
    bool tangentPoint3(int index, Geom::Pnt2d& result) const;

private:
    GccAna_Circ2d3Tan* _analyser;

    bool _extFail;
};

}  // namespace Geom