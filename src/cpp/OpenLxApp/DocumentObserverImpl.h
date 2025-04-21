#pragma once

#include <App/Document.h>
#include <Core/CoreApplication.h>
#include <Gui/PickedPoint.h>
#include <Gui/Selection.h>

namespace OpenLxApp
{
class Document;
class DocumentObserver;

class DocumentObserverImpl : public Core::CoreApplication::ObserverType,
                             public App::Document::ObserverType,
                             public Gui::Selection::ObserverType,
                             public Gui::PickedPoint::ObserverType
{
public:
    friend class DocumentObserver;

    DocumentObserverImpl(std::shared_ptr<DocumentObserver> aParent, Document* aDoc);
    ~DocumentObserverImpl();

    void onChange(Core::CoreApplication::SubjectType* rCaller, Core::CoreApplication::MessageType Reason);
    void onChange(Gui::Selection::SubjectType* rCaller, Gui::Selection::MessageType Reason);
    void onChange(App::Document::SubjectType* rCaller, App::Document::MessageType Reason);
    void onChange(Gui::PickedPoint::SubjectType* rCaller, Gui::PickedPoint::MessageType Reason);
    virtual const char* name(void) override { return "DocumentObserverImpl"; }
private:
    DocumentObserverImpl() {}
    Core::CoreApplication* _theApp = nullptr;
    Core::CoreDocument* _theDoc = nullptr;
    Gui::Selection* _theSelection = nullptr;
    Gui::PickedPoint* _thePickedPoint = nullptr;
    std::shared_ptr<DocumentObserver> _parent;
    Document* _openlxDoc;
};

}  // namespace OpenLxApp