#pragma once 

#include <Core/DocObject.h>

namespace Core
{
class LX_CORE_EXPORT PostSolver : public Core::DocObject
{
    TYPESYSTEM_HEADER();
    LX_NODE_HEADER();

public:
    PostSolver();

    enum class RecomputePass
    {
        FirstPass,
        SecondPass
    };

    /// The object should not added to the graph
    bool ignoreInGraph() const override { return true; }

    bool mustBeSaved() const override { return true; }

    virtual void initPostSolver() {}
    virtual void finalize() {}

    virtual bool solve(std::vector<Core::DocObject*>& newObjects,
                       std::vector<Core::DocObject*>& updatedObjects,
                       std::vector<Core::DocObject*>& deletedObjects) = 0;

    /// Indicates whether the solver is recomputed in the first or second pass.
    virtual Core::PostSolver::RecomputePass getRecomputePass() const = 0;
    
};


}  // namespace Core
