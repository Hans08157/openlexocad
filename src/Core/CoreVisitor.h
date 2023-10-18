#pragma once

namespace Core
{
class DocObject;
class Property;

class CoreVisitor
{
public:
    virtual void visit(Core::DocObject*) = 0;
    virtual void visit(Core::Property*) = 0;
};

}  // namespace Core