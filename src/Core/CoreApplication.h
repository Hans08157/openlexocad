#pragma once

#include <Base/Observer.h>
#include <Base/String.h>
#include <Core/CA_CommandObserver.h>

#include <functional>                 // for function, _Func_class
namespace Core { class Command; }


typedef std::vector<CA_CommandObserver*> ca_CommandObserver_Vector;
typedef std::vector<CA_TransactionObserver*> CA_TransactionObserver_Vector;


namespace Core
{
class CoreApplicationP;
class CoreDocument;
class DocObject;
class Property;
class CommandFactory;


/**
 * Data holder for application notify
 */
class LX_CORE_EXPORT AppChanges
{
public:
    enum why
    {
        NewDocument,
        CloseDocument,
        SetActiveDocument
    } Why;

    bool operator==(const AppChanges& m) const
    {
        return ((this->Why == m.Why) && (this->Doc == m.Doc) && (this->CreateGui == m.CreateGui) &&
                (this->SetAsActiveDocument == m.SetAsActiveDocument));
    }

    Core::CoreDocument* Doc = nullptr;
    bool CreateGui;                   // If true a corresponding GuiDocument gets created
    bool SetAsActiveDocument = true;  // If true when NewDocument is notified, the document will become active
};


class LX_CORE_EXPORT LoadedDll
{
public:
    LoadedDll(void){};
    virtual ~LoadedDll(void){};
    virtual Base::String getInfo() = 0;
    virtual void init() = 0;
    virtual void release() = 0;
};

class LX_CORE_EXPORT PartAcis : public Core::LoadedDll
{
public:
    PartAcis(void){};
    virtual ~PartAcis(void){};
    virtual Base::String getInfo() = 0;
    virtual void init() = 0;
    virtual void release() = 0;
    virtual Core::DocObject* create_PartGeometry(Core::CoreDocument* doc, const std::string& type) = 0;
};

class LX_CORE_EXPORT CoreApplication : public Base::Subject<Core::AppChanges>
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    CoreApplication(int argc, char** argv);
    ~CoreApplication();

    /// Returns the Singleton
    static CoreApplication* instance(void);
    /// Deletes the Singleton
    static void destroy();
    /// Resets the Singleton
    static void reset();

    /// Returns the name of the application.
    Base::String getApplicationName() const;
    /// Sets the application name
    void setApplicationName(const Base::String& name);

    /// Creates a new document without Gui. The new document becomes NOT the active document. The document has default objects.
    Core::CoreDocument* newCoreDocument(const std::string& typeName, const Base::String& name = Base::String());
    /// Creates a new document. If 'createGui = true' a GUI is created. If 'setAsActiveDocument = true' the new document becomes the active document.
    /// If 'createDefaultObjects = true' default objects are created.
    Core::CoreDocument* newDocument(const std::string& typeName,
                                    const Base::String& name = Base::String(),
                                    bool createGui = true,
                                    bool setAsActiveDocument = true,
                                    bool createDefaultObjects = true);
    /// Opens a document without Gui. The document path is not saved. The new document becomes NOT the active document.
    Core::CoreDocument* openCoreDocument(const std::string& typeName, const Base::String& path);
    /// Opens a document. If no path is provided and the application has a Gui the user is prompted with a file selection dialog.
    Core::CoreDocument* openDocument(const std::string& typeName,
                                     const Base::String& path = Base::String(),
                                     bool createGui = true,
                                     bool savepath = true,
                                     bool setAsActiveDocument = true);
    /// Closes the document. Returns 'true' if successful, 'false' if canceled.
    bool closeDocument(Core::CoreDocument* doc);
    /// Returns the active document. Returns Null if there is no active document
    Core::CoreDocument* getActiveDocument() const;
    /// Sets the active document
    bool setActiveDocument(Core::CoreDocument* doc);
    /// Returns the document by name
    Core::CoreDocument* getDocumentByName(const Base::String& name);
    /// get a list of all documents in the application
    std::vector<Core::CoreDocument*> getDocuments() const;
    /// Closes the application
    void closeApplication();
    /// Get the Application-Path
    Base::String getApplicationPath() const;
    /// Gets the TempDir of the specified document. If doc = 0 takes the active document
    Base::String getTmpDirectory(Core::CoreDocument* doc);

    /// Sets a persistent preference key and value for a module. On Windows the key and value are stored in the registry.
    void setModulePreferenceValue(const std::string& moduleName, const std::string& key, const std::string& value);
    /// Returns the persistent value of a preference key for a module. Returns empty string if key or module was not found.
    std::string getModulePreferenceValue(const std::string& moduleName, const std::string& key);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API

    /// Register an Observer for Commands
    bool registerCommandObserver(CA_CommandObserver* observer);
    ///  Unregister an Observer for Commands
    bool unregisterCommandObserver(CA_CommandObserver* observer);
    /// Returns a List of CA_CommandObserver
    ca_CommandObserver_Vector getCommandObserver();

    bool add_TransactionObserver(CA_TransactionObserver* observer);
    bool remove_TransactionObserver(CA_TransactionObserver* observer);
    CA_TransactionObserver_Vector getTransactionObservers();

    // Notifications
    void notifyObject(Core::CoreDocument* doc, Core::DocObject* obj, Core::Property* pro, CA_Transaction::why transaction);
    void notifyDocumentCreated(Core::CoreDocument* doc);
    void notifyDocumentDeleted(Core::CoreDocument* doc);
    void notifyDocumentRenamed(Core::CoreDocument* doc);
    void notifyDocumentOpened(Core::CoreDocument* doc);
    void notifyDocumentClosed(Core::CoreDocument* doc);
    void notifyDocumentSaved(Core::CoreDocument* doc);
    void notifyDocumentFinishedRead(Core::CoreDocument* doc);
    void notifyDocumentChanged(Core::CoreDocument* doc, Core::Property* pro);
    void notifyDocumentSetActive(Core::CoreDocument* doc);

    void notifyObjectCreated(Core::CoreDocument* doc, Core::DocObject* obj);
    void notifyObjectDeleted(Core::CoreDocument* doc, Core::DocObject* obj);
    void notifyObjectAdded(Core::CoreDocument* doc, Core::DocObject* obj);
    void notifyObjectChanged(Core::CoreDocument* doc, Core::DocObject* obj, Core::Property* pro);
    void notifyObjectHasError(Core::CoreDocument* doc, Core::DocObject* obj);

    void notifyPropertyCreate(Core::CoreDocument* doc, Core::DocObject* obj, Core::Property* pro);
    void notifyPropertyChanged(Core::CoreDocument* doc, Core::DocObject* obj, Core::Property* pro);
    void notifyPropertyDeleted(Core::CoreDocument* doc, Core::DocObject* obj, Core::Property* pro);

    void notifyRecomputeSuccess(Core::CoreDocument* doc);
    void notifyRecomputeFailed(Core::CoreDocument* doc);

    void notifyApp(Core::CoreDocument* doc, AppChanges::why why, bool createGui, bool setAsActiveDocument = true);
    void notifyCmdObservers(Core::CoreDocument* doc, bool createGui);

    /// Closes a document
    bool closeDocument(Core::CoreDocument* doc, bool forceClose /*=false*/, bool dontNotify = false);

    // Look through the opened documents map for the tested document;
    // this could happen when the document was closed and we just have still the pointer to removed document
    // which is invalid
    bool isDocumentValid(Core::CoreDocument* testedDocument) const;

    /// Gets the version number of the application
    bool onClose(bool forceClose, bool dontNotify, bool& hardClose);
    bool closeApplication(bool forceClose, bool dontNotify, bool& hardClose);
    Base::String getUniqueDocumentName(const Base::String& s) const;
    int getOpenDocuments(std::vector<Core::CoreDocument*>& vec);

    /// Initialize the Python interpreter (if not already initialized). Call it before using any other Python/C API functions.
    void initPython() const;
    /// Undo all initializations made in initPython() and subsequent use of Python/C API functions.  Useful to restart Python without having to
    /// restart the application itself.
    void finalizePython() const;

    bool runPythonString(const Base::String& str) const;
    bool runPythonString(const Base::String& str, Base::String& err) const;
    bool runPythonScript(const Base::String& scr, Base::String& err) const;
    bool runPythonScript(const Base::String& scr) const;

    bool isClosing() const;
    bool hasGui() const;
    void sethasGui(bool on);

    static unsigned int getVersionYear();
    static std::string getBuildDateTime();
    static std::string getDocumentVersion();
    static int getDocumentVersionAsInteger();
    /// Returns the reference count of the Application
    static long getRefCount();
    /// Increments the reference count by one
    void ref(void);
    /// Decrements the reference count by one
    void unref(void);

    LoadedDll* loadDllByName(const Base::String& name);

    void setCommandFactory(Core::CommandFactory* commandFactory) { _commandFactory = commandFactory; }
    Core::CommandFactory* getCommandFactory() const { return _commandFactory; }


    Core::Command* createCommand(const std::string& commandName) { return _createCommand(commandName); };
    void setCreateCommandFunction(std::function < Core::Command * (const std::string&)> f) { _createCommand = f; }

    virtual const char* subject_name(void) { return "CoreApplication"; };


    /** @name Application-wide trandaction setting */
    //@{
    /** Setup a pending application-wide active transaction
     *
     * @param name: new transaction name
     * @param persist: by default, if the calling code is inside any invocation
     * of a command, it will be auto closed once all command within the current
     * stack exists. To disable auto closing, set persist=true
     *
     * @return The new transaction ID.
     *
     * Call this function to setup an application-wide transaction. All current
     * pending transactions of opening documents will be committed first.
     * However, no new transaction is created by this call. Any subsequent
     * changes in any current opening document will auto create a transaction
     * with the given name and ID. If more than one document is changed, the
     * transactions will share the same ID, and will be undo/redo together.
     */
    int setActiveTransaction(const char* name, bool persist = false);
    /// Return the current active transaction name and ID
    const char* getActiveTransaction(int* tid = nullptr) const;
    /** Commit/abort current active transactions
     *
     * @param abort: whether to abort or commit the transactions
     *
     * Bsides calling this function directly, it will be called by automatically
     * if 1) any new transaction is created with a different ID, or 2) any
     * transaction with the current active transaction ID is either committed or
     * aborted
     */
    void closeActiveTransaction(bool abort = false, int id = 0);
    //@}

#endif

protected:
    Core::CoreDocument* _newDocument(const std::string& typeName, const Base::String& name, bool createGui);

    /// Physically deletes a document. The maps are not effected
    void deleteDocument(Core::CoreDocument* doc);

    /// Map of all documents
    std::map<Base::String, Core::CoreDocument*> _documentMap;

private:
    static void cleanOldTempDirectories();
    //CoreApplication() {}
    bool maybeSave(Core::CoreDocument* doc);
    bool closeDocumentP(Core::CoreDocument* doc, bool forceClose, bool dontNotify);

    CoreApplicationP* _pimpl = nullptr;
    static CoreApplication* _instance;
    Base::String _applicationName;
    std::set<CA_CommandObserver*> _commandObserverRegistry;
    std::set<CA_TransactionObserver*> _transactionObserverRegistry;
    static long _refcnt;
    Core::PartAcis* _partTool = nullptr;
    Core::CommandFactory* _commandFactory = nullptr;
    std::function<Core::Command*(const std::string&)> _createCommand;

    friend class AutoTransaction;

    std::string _activeTransactionName = "";
    int _activeTransactionID = 0;
    int _activeTransactionGuard = 0;
    bool _activeTransactionTmpName = false;

};

}  // namespace Core
