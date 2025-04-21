#pragma once
#include <string>
#include <map>

namespace Base
{
class LX_BASE_EXPORT GlobalSave
{
public:
    GlobalSave() {}

    virtual bool save(FILE* f)
    {
        for (auto it = mySave.begin(); it != mySave.end(); ++it)
        {
            if (!it->second->save(f))
                return false;
        }
        return true;
    };

    virtual const char* getName() { return ""; };
    virtual const char* getNameForID() { return ""; }

    std::map<std::string, GlobalSave*> mySave;
};

}  // namespace Base