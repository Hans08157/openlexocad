#pragma once

#include <QObject>



namespace Core
{
class Property;
class DocObject;
class CoreDocument;
class Command;
}  // namespace Core


class LX_CORE_EXPORT CA_Transaction
{
public:
    CA_Transaction() = default;

    enum why
    {
        DocumentCreate,
        DocumentChange,
        DocumentDelete,
        DocumentRenamed,
        DocumentOpen,
        DocumentFinishedRead,
        DocumentClose,
        DocumentSaved,
        DocumentSetActive,

        PropertyCreate,
        PropertyDelete,
        PropertyChange,

        ObjectCreate,
        ObjectChange,
        ObjectDelete,
        ObjectAdd,
        ObjectHasError,

        RecomputeSuccess,
        RecomputeFailure

    } Why;

    Core::CoreDocument* doc = nullptr;
    Core::DocObject* object = nullptr;
    Core::Property* property = nullptr;
};



class LX_CORE_EXPORT CA_TransactionObserver
{
public:
    CA_TransactionObserver() {}
    virtual void onChange(const CA_Transaction& tr) = 0;
    virtual std::string getName() = 0;

protected:
    virtual ~CA_TransactionObserver(void){};
};


class LX_CORE_EXPORT CA_CommandObserver : public QObject
{
public:
    CA_CommandObserver(void){};
    virtual ~CA_CommandObserver(void){};

    virtual void notifyRedo(Core::Command* const /*command*/){};
    virtual void notifyUndo(Core::Command* const /*command*/){};
    virtual void info(const std::string&){};

    virtual void notifyStart(){};
    virtual void notifyStop(){};
    virtual void notifyReset(){};

    virtual void notifySelectionAdd(Core::CoreDocument const*, const std::vector<Core::DocObject*>& /*objs*/){};
    virtual void notifySelectionRemove(Core::CoreDocument const*, const std::vector<Core::DocObject*>& /*objs*/){};
    virtual void notifySelectionClear(Core::CoreDocument const*){};


    virtual void notifyPlayLastEvents(){};

    virtual void notifyDocumentNewFile(Core::CoreDocument const*){};
    virtual void notifyDocumentOpenFile(Core::CoreDocument const*){};
    virtual void notifyDocumentSaveFile(Core::CoreDocument const*){};
    virtual void notifyDocumentSaveAsFile(Core::CoreDocument const*){};
    virtual void notifyDocumentClose(Core::CoreDocument const*){};
    virtual void notifySetActiveDocument(Core::CoreDocument const*){};

    virtual std::string getName() { return "NoName"; };

protected:
    virtual void setName(std::string&){};
};

typedef std::vector<CA_CommandObserver*> ca_CommandObserver_Vector;
typedef std::vector<CA_TransactionObserver*> CA_TransactionObserver_Vector;