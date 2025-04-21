#pragma once 

#include <Core/DocObject.h>


namespace Core
{
class LX_CORE_EXPORT PreSolver : public Core::DocObject
{
    TYPESYSTEM_HEADER();
    LX_NODE_HEADER();

public:
    PreSolver();

    /// The object should not added to the graph
    virtual bool ignoreInGraph() const { return true; }
    bool mustBeSaved() const override { return true; }
};


}  // namespace Core
