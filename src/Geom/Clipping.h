#pragma once

#include <Geom/Bnd_Box.h>
#include <Geom/Pln.h>

namespace Geom
{
class LX_GEOM_EXPORT Clipping
{
public:
    Clipping();
    Clipping(const std::vector<Geom::Pln>& planes);
    
    bool isClipped(const Geom::Pnt& p) const;
    bool isOutSide(const Geom::Bnd_Box& b) const;
    bool isClipped(const Geom::Bnd_Box& b) const;
    void clear();

    void setGap(double e);

    std::vector<Geom::Pln> getPlanes() const;

    void transform(Geom::Trsf tr);
    std::vector<std::pair<Geom::Pnt, Geom::Pnt>> asLines();
    std::vector<Geom::Pnt> asPoints();
    Geom::Bnd_Box asBBox();

private:
	Clipping(Geom::Pln pl0, Geom::Pln pl1, Geom::Pln pl2, Geom::Pln pl3, Geom::Pln pl4, Geom::Pln pl5);
    std::vector<Geom::Pln> _planes;
    double _gap;
};

}  // namespace Geom
