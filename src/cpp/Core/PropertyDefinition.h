#pragma once

#include <Base/Type.h>

namespace Core
{
class PropertyContainer;

class LX_CORE_EXPORT PropertyDefinition
{
public:
    void setName(const std::string& name, Core::PropertyContainer* pc);
    void setType(Base::Type t);
    const std::string& getName() const;
    Base::Type getType() const;

private:
    std::string _name;
    Base::Type _type;
};

}  // namespace Core