#pragma once
#include <Base/String.h>

namespace Base
{
class LX_BASE_EXPORT GlobalId_Policy
{
public:
    /// The policy that is a applied if a GlobalId
    /// is already in use.
    enum Policy
    {
        COPY,     // A copy of the object is created with a new GlobalId
        REPLACE,  // The object with this GlobalId is replaced
        REJECT    // No replacement and no copying is done. The operation is rejected.
    };

    GlobalId_Policy() { on_GUID_conflict = GlobalId_Policy::REJECT; }

    GlobalId_Policy(GlobalId_Policy::Policy aPolicy) : on_GUID_conflict(aPolicy) {}


    bool saveSettingsForThisSession = false;
    GlobalId_Policy::Policy on_GUID_conflict;
};

template <typename T>
class GlobalId_Policy_scoped
{
public:
    GlobalId_Policy_scoped(T* aDoc, const GlobalId_Policy& aPolicy, const Base::String& aSuffix = L"") : doc(aDoc), scoped_policy(aPolicy), suffix(aSuffix)
    {
        if (suffix == L"")
        {
            old_policy = doc->getGuidPolicy();
            doc->setGuidPolicy(scoped_policy);
        }
        else
        {
            bool ok = doc->getGuidPolicy(suffix, old_policy);
            if (ok)
                doc->setGuidPolicy(suffix, scoped_policy);
        }
    }
    ~GlobalId_Policy_scoped()
    {
        // Setting old policy
        if (suffix == L"")
            doc->setGuidPolicy(old_policy);
        else
            doc->setGuidPolicy(suffix, old_policy);
    }

    T* doc;
    GlobalId_Policy scoped_policy;
    GlobalId_Policy old_policy;
    Base::String suffix;
};
}  // namespace Base