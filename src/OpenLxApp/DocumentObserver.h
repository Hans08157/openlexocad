#pragma once

#include <Core/Variant.h>

#include <memory>
#include <vector>

namespace OpenLxApp
{
class Document;
class DocObject;

struct LX_OPENLXAPP_EXPORT DocumentChanges
{
public:
    enum
    {
        RECOMPUTED,
        MESSAGE_BY_NAME,
        MESSAGE_BY_ID
    } Why;

    std::string MsgName;
    int MsgId;
    Core::Variant Value;
    std::vector<std::shared_ptr<OpenLxApp::DocObject>> NewObjects;
    std::vector<std::shared_ptr<OpenLxApp::DocObject>> ModifiedObjects;
    std::vector<std::shared_ptr<OpenLxApp::DocObject>> DeletedObjects;
    std::map<std::shared_ptr<OpenLxApp::DocObject>, std::vector<std::string>>
        ErroneousObjects;  // Objects that caused an error in recompute with its error messages
};

/**
 * @brief DocumentObserver observes the Document.
 * This class has to be overridden to get messages from the observer.
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT DocumentObserver
#ifndef SWIG
    : public std::enable_shared_from_this<DocumentObserver>
#endif

{
public:
    friend class Document;
    friend class DocumentObserverImpl;

    DocumentObserver();
    virtual ~DocumentObserver();
    virtual void onChange(std::shared_ptr<OpenLxApp::Document> aCaller, std::shared_ptr<OpenLxApp::DocumentChanges> aSubject) = 0;

private:
    DocumentObserverImpl* _pimpl = nullptr;
};
}  // namespace OpenLxApp