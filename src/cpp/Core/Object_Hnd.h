#pragma once 

#include <string>

namespace Core
{
class DocObject;
class LX_CORE_EXPORT Object_Hnd
{
public:
    Object_Hnd();
    Object_Hnd(Core::DocObject* o, const std::string& internalName = "");

    enum Status
    {
        Valid,
        Unresolved
    };

    Core::DocObject* getObject() const;
    std::string getId() const;
    Status getStatus() const;
    void ref();
    void unref();

    std::string name;

    bool operator==(const Object_Hnd& rhs) const;

private:
    Core::DocObject* _object;
    int _id;
    Status _status;
};
}  // namespace Core