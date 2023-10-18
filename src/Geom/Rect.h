
/**
 * @file
 * Rect class header.
 *
 * @author Tomáš Pafèo
 */
#pragma once
#include <Geom/Pnt2d.h>
#include <cmath> 

namespace Geom

{
class Pnt;


/**
 * An axis-aligned 2D rectangle
 *
 */
class LX_GEOM_EXPORT Rect
{
public:
    Rect();
    Rect(const Pnt2d& bottomleft, const Pnt2d& topright);
    Rect(double left, double bottom, double width, double height);


    bool isNull(void) const;
    bool isEmpty(void) const;
    bool isValid(void) const;

    void setNull(void);
    void makeSingular(void);

    void getRect(double* x, double* y, double* w, double* h) const;

    double left(void) const { return _x1; }
    double right(void) const { return _x2; }
    double bottom(void) const { return _y1; }
    double top(void) const { return _y2; }

    double width(void) const { return std::abs(_x2 - _x1); }
    double height(void) const { return std::abs(_y2 - _y1); }

    Geom::Pnt2d bottomLeft(void) const { return Pnt2d(_x1, _y1); }
    Geom::Pnt2d bottomRight(void) const { return Pnt2d(_x2, _y1); }
    Geom::Pnt2d topLeft(void) const { return Pnt2d(_x1, _y2); }
    Geom::Pnt2d topRight(void) const { return Pnt2d(_x2, _y2); }
    Geom::Pnt2d center(void) const { return Pnt2d((_x1 + _x2) / 2, (_y1 + _y2) / 2); }

    void setLeft(double left);
    void setRight(double right);
    void setBottom(double bottom);
    void setTop(double top);

    void setWidth(double w) { _x2 = _x1 + w; }
    void setHeight(double h) { _y2 = _y1 + h; }
    void setSize(double width, double height);

    void moveCenter(const Pnt& p);
    void moveCenter(double x, double y);
    void grow(double value);
    void shrink(double value);
    void translate(double dx, double dy);


    Rect operator|(const Rect& r) const;
    Rect& operator|=(const Rect& r);

    void unite(const Rect& t);
    Rect united(const Rect& r) const;
    Rect normalized(void) const;

    bool contains(const Geom::Pnt& point) const;
    bool intersects(const Geom::Rect& r) const;

    /*
                void dump(void)
                {
                    printf("Base Rectangle:\n");
                    printf(" . x1: %f\n", _x1);
                    printf(" . y1: %f\n", _y1);
                    printf(" . x2: %f\n", _x2);
                    printf(" . y2: %f\n", _y2);
                    printf(" . w: %f\n", width());
                    printf(" . h: %f\n", height());

                }
    */

private:
    double _x1;
    double _y1;
    double _x2;
    double _y2;
};



}  // namespace Geom
