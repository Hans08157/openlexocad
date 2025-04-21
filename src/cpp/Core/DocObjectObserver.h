#pragma once 

#include <Core/Variant.h>


namespace Core
{
struct LX_CORE_EXPORT DocObjectObserverMsg
{
    enum class MessageId
    {
        Undefined,
        PropertyChanged,
        Scaling
    };

    MessageId msgId = MessageId::Undefined;
    Core::Variant value1;
    Core::Variant value2;
    Core::Variant value3;
};

class LX_CORE_EXPORT DocObjectObserver
{
public:
    virtual void onChange(Core::DocObject* aCaller, const Core::DocObjectObserverMsg& aReason);
};
}  // namespace Core