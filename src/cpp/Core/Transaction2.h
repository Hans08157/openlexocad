#pragma once

#include <memory>
#include <string>
#include <map>
#include <vector>

namespace Core { class CoreDocument; }
namespace Core { class DocObject; }

namespace Core
{
class Transaction2P;

class LX_CORE_EXPORT Transaction2
{
public:
    Transaction2(Core::CoreDocument* aDoc);
    ~Transaction2();

    /// Commits the transaction
    void commit();

    const std::vector<Core::DocObject*>& getNewObjects() const;
    const std::vector<Core::DocObject*>& getUpdatedObjects() const;
    const std::vector<Core::DocObject*>& getDeletedObjects() const;
    const std::map<Core::DocObject*, std::vector<std::string>>& getErroneousObjects() const;

private:
    std::unique_ptr<Transaction2P> _pimpl;
};
}  // namespace Core