#pragma once
#include <Base/String.h>
#include <map>

namespace Base
{
class LX_BASE_EXPORT GlobalAttachment
{
public:
    virtual ~GlobalAttachment() = default;

    virtual bool hasID(const std::string& id) const
    {
        for (auto sub : m_subAttachments)
            if (sub.second->hasID(id))
                return true;
        return false;
    };

    std::map<Base::String, GlobalAttachment*> m_subAttachments;
};

}  // namespace Base