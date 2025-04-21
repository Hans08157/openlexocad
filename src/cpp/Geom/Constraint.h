#pragma once

#include <Geom/AbstractConstraint.h>
#include <Geom/Lin.h>
#include <Geom/Lin2d.h>
#include <Geom/Pln.h>
#include <Geom/Trsf.h>
#include <Geom/Trsf2d.h>
#include <Geom/Vec.h>


namespace Geom
{

class Dir;

class LX_GEOM_EXPORT PointConstraintSolver : public Geom::AbstractPointConstraintSolver
{
public:
    PointConstraintSolver();
    ~PointConstraintSolver();

    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    const Geom::Pnt& getSolution() const;
    bool hasSolution() const;

    const std::list<Geom::AbstractPointConstraint*>& getConstraints() const;
    void addPointConstraint(Geom::AbstractPointConstraint* constraint);
    void removeAllConstraints(bool deleting = true);
    void removePointConstraint(Geom::AbstractPointConstraint* constraint, bool deleting = true);

private:
    std::list<Geom::AbstractPointConstraint*> _constraints;
    Geom::Pnt _pnt;
    bool _hasSolution;
};

class LX_GEOM_EXPORT PointOnLineConstraint : public Geom::AbstractPointConstraint
{
public:
    PointOnLineConstraint(const Geom::Lin& line);
    ~PointOnLineConstraint(void);

    /// Throws Base::FailedNotDone
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }
    const Geom::Lin& getLine() const;
    Geom::Lin getTransformedLine() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new PointOnLineConstraint(*this); };

private:
    PointOnLineConstraint() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Lin _line;
};

class LX_GEOM_EXPORT PointOnTwoLinesConstraint : public Geom::AbstractPointConstraint
{
public:
    PointOnTwoLinesConstraint(const Geom::Lin& line1, const Geom::Lin& line2);
    ~PointOnTwoLinesConstraint(void);

    /// Throws Base::FailedNotDone
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }
    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new PointOnTwoLinesConstraint(*this); };


private:
    PointOnTwoLinesConstraint() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Lin _line1, _line2;
};

class LX_GEOM_EXPORT PointOnPlaneConstraint : public Geom::AbstractPointConstraint
{
public:
    PointOnPlaneConstraint(const Geom::Pln& plane);
    ~PointOnPlaneConstraint(void);

    /// Throws Base::FailedNotDone
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }
    const Geom::Pln& getPlane() const;
    Geom::Pln getTransformedPlane() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new PointOnPlaneConstraint(*this); };

private:
    PointOnPlaneConstraint() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Pln _plane;
};

class LX_GEOM_EXPORT PointOnRadius : public Geom::AbstractPointConstraint
{
public:
    PointOnRadius(Geom::Pnt firstPoint, Geom::Vec tangent, double radius) : _firstPnt(firstPoint), _tangent(tangent), _radius(radius){};
    ~PointOnRadius(void);

    /// Throws Base::FailedNotDone
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }


    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new PointOnRadius(*this); };

private:
    PointOnRadius() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Pnt _firstPnt;
    Geom::Vec _tangent;
    double _radius;
};

class LX_GEOM_EXPORT MidpointConstraint : public Geom::AbstractPointConstraint
{
public:
    MidpointConstraint(const Geom::Pnt& secondPnt);
    ~MidpointConstraint(void);

    /// Never throws
    void setPoint(const Geom::Pnt& firstPnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }
    const Geom::Pnt& getSecondPoint() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new MidpointConstraint(*this); };

private:
    MidpointConstraint() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Pnt _secondPnt;
};

// Returns the static point, setPoint doesn't modify the point.
// This is used to force the snapping to fixed user defined point
class LX_GEOM_EXPORT StaticPointConstraint : public Geom::AbstractPointConstraint
{
public:
    StaticPointConstraint(const Geom::Pnt& staticPnt);
    ~StaticPointConstraint(void);

    /// Never throws
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const { return _pnt; }
    const Geom::Pnt& getStaticPoint() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPointConstraint* clone() { return new StaticPointConstraint(*this); };

private:
    StaticPointConstraint() {}
    Geom::Pnt _staticPnt;
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
};



// 2d

class LX_GEOM_EXPORT Point2dConstraintSolver : public Geom::AbstractPoint2dConstraintSolver
{
public:
    Point2dConstraintSolver();
    ~Point2dConstraintSolver();

    void setPoint2d(const Geom::Pnt2d& pnt);
    const Geom::Pnt2d& getSolution() const;
    bool hasSolution() const { return true; };

    const std::list<Geom::AbstractPoint2dConstraint*>& getConstraints() const;
    void addPoint2dConstraint(Geom::AbstractPoint2dConstraint* constraint);
    void removeAllConstraints(bool deleting = true);

private:
    std::list<Geom::AbstractPoint2dConstraint*> _constraints;
    Geom::Pnt2d _pnt;
};

class LX_GEOM_EXPORT Point2dOnLine2dConstraint : public Geom::AbstractPoint2dConstraint
{
public:
    Point2dOnLine2dConstraint(const Geom::Lin2d& line);
    ~Point2dOnLine2dConstraint(void);

    /// Throws Base::FailedNotDone
    void setPoint2d(const Geom::Pnt2d& pnt);
    void setTransformation(const Geom::Trsf2d& t) { _trsf = t; }
    const Geom::Pnt2d& getConstraintPoint2d() const { return _pnt; }
    const Geom::Lin2d& getLine2d() const;
    Geom::Lin2d getTransformedLine2d() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPoint2dConstraint* clone() { return new Point2dOnLine2dConstraint(*this); };

private:
    Point2dOnLine2dConstraint() {}
    Geom::Pnt2d _pnt;
    Geom::Trsf2d _trsf;
    Geom::Lin2d _line;
};

class LX_GEOM_EXPORT Midpoint2dConstraint : public Geom::AbstractPoint2dConstraint
{
public:
    Midpoint2dConstraint(const Geom::Pnt2d& secondPnt);
    ~Midpoint2dConstraint(void);

    /// Never throws
    void setPoint2d(const Geom::Pnt2d& firstPnt);
    void setTransformation(const Geom::Trsf2d& t) { _trsf = t; }
    const Geom::Pnt2d& getConstraintPoint2d() const { return _pnt; }
    const Geom::Pnt2d& getSecondPoint2d() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPoint2dConstraint* clone() { return new Midpoint2dConstraint(*this); };

private:
    Midpoint2dConstraint() {}
    Geom::Pnt2d _pnt;
    Geom::Trsf2d _trsf;
    Geom::Pnt2d _secondPnt;
};

// Returns the static point, setPoint doesn't modify the point.
// This is used to force the snapping to fixed user defined point
class LX_GEOM_EXPORT StaticPoint2dConstraint : public Geom::AbstractPoint2dConstraint
{
public:
    StaticPoint2dConstraint(const Geom::Pnt2d& staticPnt);
    ~StaticPoint2dConstraint(void);

    /// Never throws
    void setPoint2d(const Geom::Pnt2d& pnt);
    void setTransformation(const Geom::Trsf2d& t) { _trsf = t; }
    const Geom::Pnt2d& getConstraintPoint2d() const { return _pnt; }
    const Geom::Pnt2d& getStaticPoint2d() const;
    bool hasPoint() const { return true; };
    Geom::AbstractPoint2dConstraint* clone() { return new StaticPoint2dConstraint(*this); };

private:
    StaticPoint2dConstraint() {}
    Geom::Pnt2d _staticPnt;
    Geom::Pnt2d _pnt;
    Geom::Trsf2d _trsf;
};

// This Class checks that the Point is located in a Rectangle.
// There is no Projection or something, the Point must be in Rectangle
class LX_GEOM_EXPORT PointMustBeInRectangleConstraint : public Geom::AbstractPointConstraint
{
public:
    PointMustBeInRectangleConstraint(const Geom::Pln& plane, double u, double v);
    virtual ~PointMustBeInRectangleConstraint(void);

    /// Throws Base::FailedNotDone
    void setPoint(const Geom::Pnt& pnt);
    void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir);
    void setTransformation(const Geom::Trsf& t) { _trsf = t; }
    const Geom::Pnt& getConstraintPoint() const;
    bool hasPoint() const;
    void setValues(const Geom::Pln& plane, double u, double v);
    Geom::AbstractPointConstraint* clone() { return new PointMustBeInRectangleConstraint(*this); };

private:
    PointMustBeInRectangleConstraint() {}
    Geom::Pnt _pnt;
    Geom::Trsf _trsf;
    Geom::Pln _plane;
    double _u, _v;
};


}  // namespace Geom
