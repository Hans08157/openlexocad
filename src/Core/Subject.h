#pragma once 

#include <set>


namespace Core
{
class DocObjectObserver;
class DocObject;
struct DocObjectObserverMsg;
class LX_CORE_EXPORT Subject
{
public:
    void attach(Core::DocObjectObserver* aObserver);
    void detach(Core::DocObjectObserver* aObserver);
    void notify(Core::DocObject* aCaller, const Core::DocObjectObserverMsg& aReason);

private:
    std::set<Core::DocObjectObserver*> _observer;
};
}  // namespace Core