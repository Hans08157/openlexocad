#pragma once
#error DEPRECATED GUID.h
#include <Base/String.h>

class QUuid;

namespace Base
{
///////////////////////////////////////////////////////////
//                                                       //
// --------------------- BEGIN API --------------------- //
//                                                       //
// ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
//                                                       //
///////////////////////////////////////////////////////////

class LX_BASE_EXPORT GUID_Policy
{
public:
    /// The policy that is a applied if a GUID
    /// is already in use.
    enum Policy
    {
        COPY,     // A copy of the object is created with a new GUID
        REPLACE,  // The object with this GUID is replaced
        REJECT    // No replacement and no copying is done. The operation is rejected.
    };

    GUID_Policy() { on_GUID_conflict = GUID_Policy::REJECT; }
    GUID_Policy(Policy aPolicy) : on_GUID_conflict(aPolicy) {}


    bool saveSettingsForThisSession = false;
    GUID_Policy::Policy on_GUID_conflict;
};

template <typename T>
class GUID_Policy_scoped
{
public:
    GUID_Policy_scoped(T* aDoc, const GUID_Policy& aPolicy, const Base::String& aSuffix = L"") : doc(aDoc), scoped_policy(aPolicy), suffix(aSuffix)
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
    ~GUID_Policy_scoped()
    {
        // Setting old policy
        if (suffix == L"")
            doc->setGuidPolicy(old_policy);
        else
            doc->setGuidPolicy(suffix, old_policy);
    }

    T* doc;
    GUID_Policy scoped_policy;
    GUID_Policy old_policy;
    Base::String suffix;
};

class LX_BASE_EXPORT GUID
{
public:
    GUID()
    {
        data1 = 0;
        data2 = 0;
        data3 = 0;
        for (int i = 0; i < 8; i++)
            data4[i] = 0;
    }

    /// Create GUID from Base64 String (aka IFC GUID)
    GUID(const Base::String& base64);

    /// Create GUID from const char*. Expected format is '{F40650C2-4ACE-4606-89B1-DF4200C40E23}'
    GUID(const char* aGUID);

    bool isNull() const
    {
        return (data1 == 0 && data2 == 0 && data3 == 0 && data4[0] == 0 && data4[1] == 0 && data4[2] == 0 && data4[3] == 0 && data4[4] == 0 &&
                data4[5] == 0 && data4[6] == 0 && data4[7] == 0);
    }

    /// Creates a new GUID
    static GUID createGUID();
    ///	Creates a CA::GUID from a QUuid
    static GUID fromQUuid(const QUuid& uuid);
    /// Converts a CA::GUID into a QUuid
    static void toQUuid(const GUID& in, QUuid& uuid);
    /// Returns a QUuid from this.
    void toQUuid(QUuid& uuid) const;


    Base::String toBase64() const;
    Base::String toString() const;

    unsigned int data1;
    unsigned short data2;
    unsigned short data3;
    unsigned char data4[8];

    bool operator==(const GUID& rhs) const
    {
        unsigned int i;
        if (data1 != rhs.data1 || data2 != rhs.data2 || data3 != rhs.data3)
            return false;

        for (i = 0; i < 8; i++)
            if (data4[i] != rhs.data4[i])
                return false;

        return true;
    }

    bool operator!=(const GUID& rhs) const { return !(*this == rhs); }

    bool operator<(const GUID& rhs) const;
    bool operator>(const GUID& rhs) const;
};
}  // namespace Base
