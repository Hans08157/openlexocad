#pragma once

#include <list>

namespace Geom
{
class Trsf2d;
class Trsf;
class AbstractPoint2dConstraint;
class AbstractPointConstraint;
class Pnt;
class Dir;
class Pnt2d;

class LX_GEOM_EXPORT AbstractConstraintSolver
{
public:
    virtual ~AbstractConstraintSolver() = default;
};

class LX_GEOM_EXPORT AbstractPointConstraintSolver : public AbstractConstraintSolver
{
public:
    virtual ~AbstractPointConstraintSolver() = default;

    virtual void setPoint(const Geom::Pnt& pnt) = 0;
    virtual void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir) = 0;
    virtual const Geom::Pnt& getSolution() const = 0;
    virtual bool hasSolution() const = 0;

    virtual const std::list<Geom::AbstractPointConstraint*>& getConstraints() const = 0;
    virtual void addPointConstraint(Geom::AbstractPointConstraint* constraint) = 0;
    virtual void removeAllConstraints(bool deleting = true) = 0;
};

class LX_GEOM_EXPORT AbstractPoint2dConstraintSolver : public AbstractConstraintSolver
{
public:
    virtual ~AbstractPoint2dConstraintSolver() = default;

    virtual void setPoint2d(const Geom::Pnt2d& pnt) = 0;
    virtual const Geom::Pnt2d& getSolution() const = 0;
    virtual bool hasSolution() const = 0;

    virtual const std::list<Geom::AbstractPoint2dConstraint*>& getConstraints() const = 0;
    virtual void addPoint2dConstraint(Geom::AbstractPoint2dConstraint* constraint) = 0;
    virtual void removeAllConstraints(bool deleting = true) = 0;
};

/// Base class of all point constraints
class LX_GEOM_EXPORT AbstractPointConstraint
{
public:
    virtual ~AbstractPointConstraint() = default;

    virtual void setPoint(const Geom::Pnt& pnt) = 0;
    virtual void setPointAndDir(const Geom::Pnt& pnt, const Geom::Dir& dir) = 0;
    virtual void setTransformation(const Geom::Trsf& t) = 0;
    /// Returns the point based on the applied constraint
    virtual const Geom::Pnt& getConstraintPoint() const = 0;
    virtual bool hasPoint() const = 0;
    virtual AbstractPointConstraint* clone() = 0;
};

/// Base class of all 2d point constraints
class LX_GEOM_EXPORT AbstractPoint2dConstraint
{
public:
    virtual ~AbstractPoint2dConstraint() = default;
    virtual void setPoint2d(const Geom::Pnt2d& pnt) = 0;
    virtual void setTransformation(const Geom::Trsf2d& t) = 0;
    /// Returns the point based on the applied constraint
    virtual const Geom::Pnt2d& getConstraintPoint2d() const = 0;
    virtual bool hasPoint() const = 0;
    virtual AbstractPoint2dConstraint* clone() = 0;
};

}  // namespace Geom
