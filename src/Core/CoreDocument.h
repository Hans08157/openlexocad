#pragma once

#include <Base/Observer.h>
#include <Core/DocObject.h>
#include <Core/PropertyBundle.h>
#include <Core/PropertyInteger.h> // Core::PropertyIndex
#include <Core/PropertyText.h>
#include <Core/PropertyTextList.h>

#include <QDateTime>

#ifndef SWIG
#include <boost/signals2/signal.hpp>  // for signal
#endif

#define DIR_NAME_INTERNAL_CATALOG "__internalCatalog__"
#define DIR_NAME_USER_CATALOG "UserCatalog"
#define DIR_NAME_WEBGL_GT "webgl"
#define DIR_NAME_GEOID "geoid"
#define DIR_NAME_BCF "Bcf"
#define FILE_NAME_CAMERA_ANIMATION "CameraAnimation.ivc"

typedef std::vector<Core::DocObject*> DOCOBJECTS;
typedef std::map<Core::DocObject*, std::vector<std::string>> DOCOBJECTS_ERROR_MAP;

namespace Base
{
class XMLReader;
class GlobalAttachment;
}

namespace App
{
class ElementTool;
}

namespace Core
{
class ObjectGraph;
class ExecObject;
class PropertyLinkBase;
class CoreDocumentImpl;
class Transaction;
class RelGraph;
class PropertyLinkBaseBase;

typedef std::vector<Core::DocObject*> ObjectVector;
typedef std::unordered_set<Core::DocObject*> ObjectSet;
typedef std::unordered_map<DocObject::IdType, Core::DocObject*> ObjectMap;
typedef std::vector<Core::ExecObject*> ExecObjectVector;
typedef std::unordered_set<Core::ExecObject*> ExecObjectSet;
typedef std::unordered_map<DocObject::IdType, Core::ExecObject*> ExecObjectMap;
typedef std::map<Base::Type, ObjectSet> ObjectTypeMap;


class LX_CORE_EXPORT Link : public std::vector<std::pair<Core::PropertyLinkBaseBase*,Core::DocObject*>>
{
public:
    bool isSameAs(const Link& rhs ) const;
};



struct LX_CORE_EXPORT LinkError
{
    Core::DocObject* source = nullptr;
    Core::DocObject* target = nullptr;    
    Core::PropertyLinkBaseBase* property = nullptr;    

};

struct LX_CORE_EXPORT LinkStore
{
    LinkStore(Core::DocObject* s,Core::PropertyLinkBaseBase* p, Core::DocObject* t): source(s),target(t),property(p){}
    Core::DocObject* source;
    Core::DocObject* target;    
    Core::PropertyLinkBaseBase* property;    
};


struct AttachmentEntry
{
    Base::String FileName;
    Base::String FeatName;
    Base::String Info;
};
typedef std::multimap<Base::String, Core::AttachmentEntry> Attachments;

/*
Core::DocChanges
This class notifies the observers about a recompute of the document.
It can also be used to send messages to the Observers:
1. Example:

Core::ExecObject* o = ...

Core::DocChanges docChanges;
docChanges.Why      = Core::DocChanges::MESSAGE_BY_NAME
docChanges.MsgName  = "MsgObjectAdded";
docChanges.Value	= Core::Variant(o);
emitAndNotify(docChanges);

2. Example:

enum DocMessage
{
    MSG_OBJECT_ADDED = 1,
    ...
}

Core::ExecObject* o = ...

Core::DocChanges docChanges;
docChanges.Why      = Core::DocChanges::MESSAGE_BY_ID
docChanges.MsgId    = DocMessage::MSG_OBJECT_ADDED;
docChanges.Value	= Core::Variant(o);
emitAndNotify(docChanges);
*/

class LX_CORE_EXPORT DocChanges
{
public:
    DocChanges(Core::CoreDocument* doc) : Value(0), Document(doc) {}

    enum why
    {
        RECOMPUTED,
        MESSAGE_BY_NAME,
        MESSAGE_BY_ID
    } Why = RECOMPUTED;

    bool mustNotify() const
    {
        if (Why != RECOMPUTED) return true;

        // Notify if there is at least one new object or at least one deleted object. Otherwise e.g. Layer window doesn't react on deleted or added
        // layers (CmdDeleteEmptyLayers redo and undo). Or ViewProviderProxyElement is not removed when App::ProxyElement is removed removed by
        // removeObjectFinal (problem in 35617).
        if (!NewObjects.empty() || !DeletedObjects.empty())
            return true;

        for (auto lObj : UpdatedObjects)
        {
            if (lObj->mustNotify())
            {
                return true;
            }
        }

        return false;
    }

    bool hasVisibilityChanges(std::vector<Core::DocObject*>& aDocObjects) const
    {
        for (auto lObj : UpdatedObjects)
        {
            if (lObj->hasVisiblityChanged())
            {
                aDocObjects.emplace_back(lObj);
            }
        }
        return (bool)aDocObjects.size();
    }

    bool hasOnlyVisibilityChanges() const
    {
        for (auto lObj : UpdatedObjects)
        {
            if (!lObj->hasOnlyVisibilityChanged())
            {
                return false;
            }
        }

        return true;  
    }

    std::string MsgName = "";
    int MsgId = -1;
    Core::Variant Value;
    Core::CoreDocument* Document;

    std::vector<Core::DocObject*> NewObjects;
    std::vector<Core::DocObject*> UpdatedObjects;
    std::vector<Core::DocObject*> DeletedObjects;
    std::map<Core::DocObject*, std::vector<std::string>> ErroneousObjects;  // Objects that caused an error in recompute with its error messages

private:
    DocChanges() : MsgId(0), Document(nullptr){};
};

// All Lexocad Core message Ids are in the range 1000 - 1999
const int LEXOCAD_CORE_MSGID = 1000;

enum LX_CORE_EXPORT DocMessage
{
    RecomputeError = LEXOCAD_CORE_MSGID,
    Rename = LEXOCAD_CORE_MSGID + 1,
    NewFile = LEXOCAD_CORE_MSGID + 2,
    FileOpened = LEXOCAD_CORE_MSGID + 3,
    BeforeSave = LEXOCAD_CORE_MSGID + 4,
    AfterSave = LEXOCAD_CORE_MSGID + 5,
    CleanAll = LEXOCAD_CORE_MSGID + 6,
    AddDirectoryPath = LEXOCAD_CORE_MSGID + 7,
    RecomputeFinished = LEXOCAD_CORE_MSGID + 8,
    ErrorCanNotOpenFile = LEXOCAD_CORE_MSGID + 9,
    ChangeToDefaultUser = LEXOCAD_CORE_MSGID + 10,
    GUID_Conflict = LEXOCAD_CORE_MSGID + 11,
    Export = LEXOCAD_CORE_MSGID + 12,
    Import = LEXOCAD_CORE_MSGID + 13,
    SaveStart = LEXOCAD_CORE_MSGID + 14,
    Closing = LEXOCAD_CORE_MSGID + 15,
    PriceCalculationChanged = LEXOCAD_CORE_MSGID + 16,
    PostCheck = LEXOCAD_CORE_MSGID + 17
};



struct LX_CORE_EXPORT DocumentState
{
    // Copy constructor
    DocumentState() = default;
    DocumentState(const DocumentState& rhs)
    {
        PropertyErrors = rhs.PropertyErrors;
        LastErroneousObjects = rhs.LastErroneousObjects;
        LastRecomputeTime = rhs.LastRecomputeTime;
        LastNotifyTime = rhs.LastNotifyTime;
    }

    std::vector<std::string> PropertyErrors;
    std::map<Core::DocObject*, std::vector<std::string>> LastErroneousObjects;
    unsigned long LastRecomputeTime;
    unsigned long LastNotifyTime;

    void clear();
};

struct LX_CORE_EXPORT PropertyLinkDesc
{
    PropertyLinkDesc(std::string sourceDocObjectID, std::string sourcePropertyName, Base::Type sourcePropertyTypeID, std::string targetDocObjectID,std::string propertyLinkName)
        : m_SourceDocObjectID(sourceDocObjectID)
        , m_SourcePropertyName(sourcePropertyName)
        , m_SourcePropertyTypeID(sourcePropertyTypeID)
        , m_TargetDocObjectID(targetDocObjectID)
        , m_PropertyLinkName(propertyLinkName)
    {
    }

    // Copy constructor
    PropertyLinkDesc(const PropertyLinkDesc& rhs)
    {
        m_SourceDocObjectID = rhs.m_SourceDocObjectID;
        m_SourcePropertyName = rhs.m_SourcePropertyName;
        m_SourcePropertyTypeID = rhs.m_SourcePropertyTypeID;
        m_TargetDocObjectID = rhs.m_TargetDocObjectID;
        m_PropertyLinkName = rhs.m_PropertyLinkName;

    }

    std::string m_SourceDocObjectID;
    std::string m_SourcePropertyName;
    Base::Type m_SourcePropertyTypeID;

    std::string m_TargetDocObjectID;
    std::string m_PropertyLinkName;
};

struct LX_CORE_EXPORT IfcHeader
{
    struct FileDescriptor
    {
        PropertyText description;
        PropertyText implementationLevel;
    }
    fileDescriptor;

    struct FileName
    {
        PropertyTextList author;
        PropertyText authorization;
        PropertyText name;
        PropertyTextList organization;
        PropertyText originatingSystem;
        PropertyText preprocessorVersion;
        PropertyText timeStamp;
    }
    filename;

    struct FileSchema
    {
        PropertyText schemaIdentifier;
    }
    fileSchema;
};

class LX_CORE_EXPORT CoreDocument : public Core::PropertyContainer, public Base::Subject<Core::DocChanges>
{
    TYPESYSTEM_HEADER();
    LX_NODE_HEADER();

public:
    friend class CoreApplication;
    friend class CoreDocument_Factory;    
    friend class PropertyGUID;
    friend class DocumentTimeStampSentinel;
    friend class ::App::ElementTool;
 
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    enum Status
    {
        SkipRecompute = 0,
        KeepTrailingDigits = 1,
        Closable = 2,
        Restoring = 3,
        Recomputing = 4,
        PartialRestore = 5,
        Importing = 6,
        PartialDoc = 7,
        AllowPartialRecompute = 8,  // allow recomputing editing object if SkipRecompute is set
        TempDoc = 9,                // Mark as temporary document without prompt for save
        RestoreError = 10
    };

    Core::PropertyText name;
    Core::PropertyText documentVersion;
    Core::PropertyText compatibleInfo;
    Core::PropertyText documentGUID;
    Core::PropertyIndex documentChanges;
    Core::PropertyIndex documentMaxID;
    Core::PropertyIndex application_mainversion;    // This version major of the RESTORED document.
    Core::PropertyIndex application_minorversion;   // This version minor of the RESTORED document.
    Core::PropertyText documentTypeName;
    Core::PropertyText filename;
    Core::PropertyText createdBy;     // designer
    Core::PropertyText creationDate;  // date
    Core::PropertyText lastModifiedBy;
    Core::PropertyText lastModifiedDate;
    Core::PropertyText company;  // customer
    Core::PropertyText comment;
    Core::PropertyText projectNumber;  // related to PieceList
    Core::PropertyText architect;

    IfcHeader ifcHeader;

    Base::String fileName;

    /// Returns the version of the document
    int getDocumentVersion() const;
    /// Adds an existing object to the document
    bool addObject(Core::DocObject* e);
    /// Removes an object from the document
    void removeObject(Core::DocObject* e);
    /// Removes an object from the document
    virtual void removeObjectFinal(Core::DocObject* e, bool deep = false);
    /// Removes objects from the document
    void removeObjects(const std::vector<Core::DocObject*>& objects);

    /// Is called when the file was opened, but before the message FileOpened gets emitted. Can be overwritten to add custom behavior.
    virtual void onFileOpened() {}
    /// callback from the Document objects before property will be changed
    void onBeforeChangeProperty(const Core::DocObject* Who, const Property* What);
    /// callback from the Document objects after property was changed
    void onChangedProperty(const Core::DocObject* Who, const Property* What);

    virtual bool onChangedDebug(Core::DocObject* o, Core::Property* p);
    

    /// Return type of which new copied element should be created.
    /// setCopyType is intentionally not available because it is decided in copy methods.
    Base::Type getCopyType() const;
    /// Sets the copy type to Base::Type::badType(), next copied object will be copied as its own type.
    void clearCopyType();
    /// Creates a copy of 'o' and adds it to the document, provides map of pairs original-copy to see which object is a copy of another one
    Core::DocObject* copyObject(Core::DocObject* o, DocObjectMap& copyMap);
    Core::DocObject* copyObject(Core::DocObject* o);
    /// Creates an object of type 'typeToCreate' and copy properties from 'o' to it. Provides map of pairs original-copy
    Core::DocObject* copyToDifferentType(Core::DocObject* o, Base::Type typeToCreate, DocObjectMap& copyMap);
    /// Copy shared object. This is violating of the share, but in some cases this is useful. Use wisely!!
    Core::DocObject* copySharedObject(Core::DocObject* o, DocObjectMap& copyMap);
    /// Creates a copy of 'o' and adds it to the document. Performs shallow copy.
    template <typename Type>
    Type copyObjectShallow(Type o)
    {
        Core::DocObject* copy = o->shallowCopy(this);
        assert(copy && "Document::copyObjectShallow could not copy object");
        copy->setDocument(this);
        copy->setNew();
        copy->initDocObject();

        Type typedCopy = dynamic_cast<Type>(copy);
        assert(typedCopy && "Document::copyObjectShallow could not cast object");

        return typedCopy;
    }

    /// Returns all objects in the document
    std::vector<Core::DocObject*> getObjects(bool includeDeletedObjects = false) const;
    std::vector<const Core::DocObject*> getObjectsConst(bool includeDeletedObjects = false) const;
    /// Returns all objects topologically sorted
    virtual std::vector<Core::DocObject*> getObjectsSorted() const;    
    /// Creates an object from type name and adds it to the document
    Core::DocObject* createObjectFromTypeName(const char* typeName);
    /// Creates an object from type and adds it to the document
    Core::DocObject* createObjectFromType(Base::Type type);
    /// Returns all objects of typeName
    std::vector<Core::DocObject*> getObjectsByTypeName(const std::string& typeName) const;
    /// Recomputes the document
    virtual void recompute();
    /// Recomputes the document. Takes a lambda as an argument -> { /*CODE*/ auto onRecomputedCB = [this] (DOCOBJECTS newObj, DOCOBJECTS updatedObj,
    /// DOCOBJECTS deletedObj, DOCOBJECTS_ERROR_MAP errorObj); }
    virtual void recompute(
        std::function<void(DOCOBJECTS newObj, DOCOBJECTS updatedObj, DOCOBJECTS deletedObj, DOCOBJECTS_ERROR_MAP errorObj)> onRecomputedCB);
    /// Saves the document under this name*
    virtual bool saveAs(const Base::String& filename);
    /// Returns the temporary directory
    Base::String getTmpDirectory() const;
    /// Returns 'true' if the Document is the active Document. Otherwise returns 'false'
    bool isActive() const;
    /// Returns 'true' if the document is changed.
    virtual bool isChanged();
    /// Returns the DocObject with this GUID
    Core::DocObject* getObjectByGlobalId(const Base::GlobalId& guid) const;

    std::string getDocXMLAsString();

    /// return the status bits
    bool testStatusBits(Status pos) const;
    /// set the status bits
    void setStatusBits(Status pos, bool on);
    //@}

    /** @name Transaction - New Undo/Redo*/
    //@{
    /** @name methods for the UNDO REDO and Transaction handling
     *
     * Introduce a new concept of transaction ID. Each transaction must be
     * unique inside the document. Multiple transactions from different
     * documents can be grouped together with the same transaction ID.
     *
     * When undo, Gui component can query getAvailableUndo(id) to see if it is
     * possible to undo with a given ID. If there more than one undo
     * transactions, meaning that there are other transactions before the given
     * ID. The Gui component shall ask user if he wants to undo multiple steps.
     * And if the user agrees, call undo(id) to unroll all transaction before
     * and including the the one with the give ID. Same applies for redo.
     *
     * The new transaction ID describe here is fully backward compatible.
     * Calling the APIs with a default id=0 gives the original behavior.
     */
     //@{
     /// switch the level of Undo/Redo
    void setUndoMode(int iMode);
    /// switch the level of Undo/Redo
    int getUndoMode(void) const;
    /// switch the transaction mode
    void setTransactionMode(int iMode);
    /** Open a new command Undo/Redo, an UTF-8 name can be specified
     *
     * @param name: transaction name
     *
     * This function calls App::Application::setActiveTransaction(name) instead
     * to setup a potential transaction which will only be created if there is
     * actual changes.
     */
    int openTransaction(const char* name = 0);
    /// Rename the current transaction if the id matches
    void renameTransaction(const char* name, int id);
    /// Commit the Command transaction. Do nothing If there is no Command transaction open.
    void commitTransaction();
    /// Abort the actually running transaction.
    void abortTransaction();
    /// Check if a transaction is open
    bool hasPendingTransaction() const;
    /// Returns pending transaction name. Returns nullptr if there is no pending transaction.
    const char* getPendingTransactionName() const;
    /// Return the undo/redo transaction ID starting from the back
    int getTransactionID(bool undo, unsigned pos = 0) const;
    /// Check if a transaction is open and its list is empty.
    /// If no transaction is open true is returned.
    bool isTransactionEmpty() const;
    /// Set the Undo limit in Byte!
    void setUndoLimit(unsigned int UndoMemSize = 0);
    /// Set the Undo limit as stack size
    void setMaxUndoStackSize(unsigned int UndoMaxStackSize = 20);
    /// Set the Undo limit as stack size
    unsigned int getMaxUndoStackSize(void)const;
    /// Remove all stored Undos and Redos
    void clearUndos();
    /// Returns the number of stored Undos. If greater than 0 Undo will be effective.
    int getAvailableUndos(int id = 0) const;
    /// Returns a list of the Undo names
    std::vector<std::string> getAvailableUndoNames() const;
    /// Will UNDO one step, returns False if no undo was done (Undos == 0).
    bool undo(int id = 0);
    /// Returns the number of stored Redos. If greater than 0 Redo will be effective.
    int getAvailableRedos(int id = 0) const;
    /// Returns a list of the Redo names.
    std::vector<std::string> getAvailableRedoNames() const;
    /// Will REDO one step, returns False if no redo was done (Redos == 0).
    bool redo(int id = 0);
    /// returns true if the document is in an Transaction phase, e.g. currently performing a redo/undo or rollback
    bool isPerformingTransaction() const;
    //@}

    /// Returns the object with this id
    virtual Core::DocObject* getObjectById(const DocObject::IdType& id) const;
    /// Returns the object with this userName
    Core::DocObject* getObjectByUserName(const Base::String& s) const;

    // Filename Recommend - used in SaveAs.
    void setRecommendFileNameForSave( const Base::String& s );
    

#ifndef SWIG
    virtual void emitAndNotify(Core::DocChanges& aDocChanges);
    /** @name Signals of the document */
    //@{
    /// Signals DocChanges (To be removed)
    boost::signals2::signal<void(Core::DocChanges&)> signalDocChanges;
    /// signal on new Object
    boost::signals2::signal<void(const Core::DocObject&)> signalNewObject;
    /// signal on deleted Object
    boost::signals2::signal<void(const Core::DocObject&)> signalDeletedObject;
    /// signal on visibility changed Object
    //boost::signals2::signal<void(const std::vector<Core::DocObject*>&)> signalVisibilityChanged;
    /// signal before changing an Object
    boost::signals2::signal<void(const Core::DocObject&, const Core::Property&)> signalBeforeChangeObject;
    /// signal on changed Object
    boost::signals2::signal<void(const Core::DocObject&, const Core::Property&)> signalChangedObject;
    /// Signals before recompute.
    boost::signals2::signal<void()> signalBeforeRecompute;
    /// Signals NewObjects, UpdatedObjects, DeletedObjects being recomputed.
    boost::signals2::signal<void(const std::vector<Core::DocObject*>&, const std::vector<Core::DocObject*>&,const std::vector<Core::DocObject*>&)> signalRecomputed;
    /// Signals a recompute error.
    boost::signals2::signal<void()> signalRecomputeError;
    /// Signals recomputed error DocObjects.
    boost::signals2::signal<void(const std::map<Core::DocObject*, std::vector<std::string>>&)> signalRecomputedErrorObjects;
    /// Signals defect links from object1 to object2.
    boost::signals2::signal<void(const std::vector<Core::LinkError>&)> signalDefectLinks;
    /// Signals new file.
    boost::signals2::signal<void()> signalNewFile;
    //@}
#endif

#ifndef LXAPI
    

    



    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Creates and adds a new object to the document using templates. If a Core::PropertyBundle is given the object is initialized with these
    /// properties.
    template <typename T>
    T* createObject()
    {
        Core::DocObject* o = createObjectFromType(T::getClassTypeId());
        if (o)
            return static_cast<T*>(o);

        return nullptr;
    }

    /// Adds an immutable object to the document using templates. The Core::PropertyBundle is taken to compare the values with all existing immutable
    /// objects.
    template <typename T>
    T* addImmutableObject(const Core::PropertyBundle<T>* po)
    {
        // Check if it really is immutable
        if (T::isMutableStatic())
            return nullptr;

        // Check if an immutable object with these values already exists
        Core::DocObject* check = getImmutableObjectWithSameValues(T::getClassTypeId(), po);
        if (check)
            return static_cast<T*>(check);

        // If it doesn't exist make a new one and initialize it with the
        // property values from the Core::PropertyBundle.
        Core::DocObject* o = createObjectFromType(T::getClassTypeId());
        if (o)
        {
            o->_setPropertyValues(po, /* bool isInit = */ true);
            o->setStatus(Core::PropertyContainer::Status::New);  // At initialization the status needs to stay NEW
            addImmutableObjectMaterial(o);
            return static_cast<T*>(o);
        }

        return nullptr;
    }

    /// Adds an immutable object to the document using templates. The Core::PropertyBundle is taken to compare the values with all existing immutable
    /// objects.
    template <typename T>
    T* addImmutableObject_NoCheck(Core::PropertyBundle<T>* po)
    {
        // Check if it really is immutable
        if (T::isMutableStatic())
            return nullptr;

        // If it doesn't exist make a new one and initialize it with the
        // property values from the Core::PropertyBundle.
        Core::DocObject* o = createObjectFromType(T::getClassTypeId());
        if (o)
        {
            o->_setPropertyValues(po, /* bool isInit = */ true);
            o->setStatus(Core::PropertyContainer::Status::New);  // At initialization the status needs to stay NEW
            addImmutableObjectMaterial(o);
            return static_cast<T*>(o);
        }

        return nullptr;
    }

    /// Return all object of given type and all derived classes
    template <typename T>
    std::vector<T*> getObjectsByType() const
    {
        // get all resulting types including derived classes
        Base::Type t = T::getClassTypeId();
        std::set<Base::Type> typeset;
        t.getAllChildren(typeset);
        typeset.insert(t);

        std::vector<T*> returnObjs{};
        for (const auto& type : typeset)
        {
            auto type2objects = getTypeMap().find(type);
            if (type2objects == getTypeMap().end())  // do we know this type?
                continue;

            const auto& docObjects = type2objects->second;
            for (const auto& obj : docObjects)  // get un-deleted objects of given type
            {
                if (!obj->isDeleted())
                    returnObjs.push_back(static_cast<T*>(obj));
            }
        }

        return returnObjs;
    }

    /// Returns all objects of type 'T'
    template <typename T>
    void getObjectsByType(std::vector<T*>& objs) const
    {
        const auto& objectMap = getObjectMap();
        for (const auto& it : objectMap)  //#todo go only over seconds
        {
            if (!it.second->isDeleted() && it.second->isDerivedFrom<T>())  // #todo why test for type when the type is in first?
                objs.push_back((T*)it.second);
        }
    }    

    /// Returns all objects of type 'T'
    void getObjectsFromTypeMap(Base::Type t, std::vector<Core::DocObject*>& ret) const;
    const ObjectTypeMap& getTypeMap() const;

    void addPropertyLinkError(const std::string& from, const std::string& to);
    const DocumentState& getDocumentState() const;
    /// Checks the document for errors. Returns false if there is an error
    bool checkObjectLinks(const std::vector<const Core::DocObject*>& objvec,
                          std::vector<Core::LinkError>* errors = nullptr);
    bool checkObjectLinks(const std::vector<const Core::DocObject*>& objvec,
                          const std::vector<const Core::DocObject*>& objToCheck,
                          std::vector<Core::LinkError>* errors= nullptr);
    bool checkDeletedObjectLinks(const std::vector<const Core::DocObject*>& objToCheck,
                                 std::vector<Core::LinkError>* errors);

    bool checkObjectLinks( std::vector<Core::LinkError>* errors );

    bool checkDeletedObjectLinks(const std::vector<const Core::DocObject*>& objvec,
                                 const std::vector<const Core::DocObject*>& objToCheck,
                                 std::vector<Core::LinkError>* errors);

    /// Get ALL Links to me, also indirect
    virtual std::vector<const Core::DocObject*> getInner(const Core::DocObject* me, std::function<bool(const Core::DocObject*)>* allowToAddObject = 0);    
    /// Get ALL Links from me, also indirect
    virtual std::vector<const Core::DocObject*> getOuter(const Core::DocObject* me);

    Core::Link getAllLinksByProperties(const Core::DocObject* source) const;

    std::vector<const Core::DocObject*> getLinksByProperties(const Core::DocObject* o) const;
    std::vector<PropertyLinkDesc> getLinkDescByProperties(const Core::DocObject* o) const;
    std::vector<const Core::DocObject*> getBackLinksByProperties(const Core::DocObject* source) const;

    void removeLinkInProperties(const Core::DocObject* source, Core::DocObject* link);
    void removeBackLinkInProperties(const Core::DocObject* source, Core::DocObject* link);

    /// Returns a string representation of the graph
    std::string dumpGraph(void);
    virtual std::vector<std::string> check_graph();
    /// Returns all objects that directly linked to 'o'
    virtual std::vector<const Core::DocObject*> getLinksToMe(const Core::DocObject* o);
    /// Returns all objects that directly linked to 'o'
    virtual std::vector<const Core::DocObject*> getBackLinksToMe(const Core::DocObject* o);
    /// Returns all objects 'o' directly linked from 'o'
    virtual std::vector<const Core::DocObject*> getLinksFromMe(const Core::DocObject* o);
    /// Returns all objects 'o' directly linked from 'o'
    virtual std::vector<const Core::DocObject*> getBackLinksFromMe(const Core::DocObject* o);
    
    /// Can be overwritten to check if the undo stack is clean etc.
    virtual bool maybeSave() { return true; }
    /// Returns all objects that will be saved in document. Basically interface for build_savemap().
    std::vector<Core::DocObject*> getObjectsToSave();

    /// Returns application's mainversion to be saved in the document.
    static void getDefaultVersionToSave(int& aMajorVersion, int& aMinorVersion);
    /// Returns application's mainversion to be saved in the document saved as PREVIOUS version.
    static void getPreviousVersionToSave(int& aMajorVersion, int& aMinorVersion);
    /// Returns application's version as string to be displayed in the menu for action Save as PREVIOUS version.
    static QString getPreviousVersionToSaveStr();

    /// Saves the file
    bool saveFile(bool toExport = false, bool saveBackupCopy = false);
    /// Saves a new file under this name
    bool saveAsFile(const Base::String& filename = Base::String(),
                    bool toExport = false,
                    bool saveBackupCopy = false,
                    const Base::String& initialDir = Base::String());

    /// Saves a copy of the current document, no notify, only store the doc under this name
    bool saveCopy(const Base::String& filename);
    /// Saves a new file under this name
    bool saveAsFileVersion(int aMajorVersion,
                           int aMinorVersion,
                           const Base::String& filename = Base::String(),
                           bool toExport = false,
                           bool saveBackupCopy = false,
                           const Base::String& initialDir = Base::String(),
                           bool dontRename = false);
    ///	If true: Change to default user on next change. Usually from IFC User to Lexocad User.
    void setOnSaveChangeToDefaultUser(bool onoff);
    ///	Return whether the user get changed to default user on next save.
    bool getOnSaveChangeToDefaultUser() const;
    /// Ask user for filename (if not already passed in as newFilename) and set it to document. Returns false if user cancelled the save.
    bool askAndSetNewFilename(QString& newFilename, const Base::String& initialDir = Base::String());
    /// If true, saving will block until the whole save is finished and file is ready.
    void setSaveBlocksUntilFinished(bool onoff);
    /// Returns whether saving will block until the whole save is finished and file is ready.
    bool getSaveBlocksUntilFinished() const;

    /// Inventor search directories - needs to be stored for IV/Z export, but SoInput is not OK...
    virtual void addInventorDirectory(const Base::String&) {}
    /// To overwrite. Deprecated, do not use.
    virtual void createGroundPlate_deprecated() {}
    
    /// Sets the default GUID policy. This determines what should be done if identical GUIDs are imported
    void setGuidPolicy(const Base::GlobalId_Policy& policy);
    /// Sets the GUID policy for a file suffix. This determines what should be done if identical GUIDs are imported from files with this suffix.
    void setGuidPolicy(const Base::String& suffix, const Base::GlobalId_Policy& policy);
    ///	Returns the default GUID policy
    Base::GlobalId_Policy getGuidPolicy() const;
    ///	Returns the GUID policy	for a file suffix.
    bool getGuidPolicy(const Base::String& suffix, Base::GlobalId_Policy& policy) const;

    void addReferenceFrom(Core::DocObject* from);
    void removeReferenceFrom(Core::DocObject* from);
    bool hasReferencesFrom(Core::DocObject* from) const;
    const std::set<Core::DocObject*>& getReferences() const;
    /// Sets the full file name including the path
    void setFullFileName(const Base::String& fullfilename);

    virtual const char* subject_name(void) { return "CoreDocument"; };

    virtual bool restoreGlobalAttachment(Base::GlobalAttachment* gAtta, std::istream*, uint64_t streamsize, const Base::String& entryName);

    bool addFileToZip(const Base::String& entryName, const Base::String& path);
    bool restoreFileFromZip(const Base::String& entryName, const Base::String& targetpath, bool binaryMode);

    /// Modifies the _lastBackupFileTime to force backup when the document is saved next time
    void forceBackupOnNextSave();

    /// get result of last recompute
    bool hasErrorObjectsInRecompute();
    /// reset result of last recompute();
    void resetHasErrorObjectsInRecompute();

    /// get count of recomputes()
    size_t getRecomputeCount() const;

    virtual void setChanged(bool changed);

    bool getImmutableObjects(Base::Type t, ObjectSet& set) const;
    virtual Core::DocObject* addImmutableObjectMaterial(Core::PropertyContainer* pc);

    void setImportedIFCFile(QString a);
    QString getImportedIFCFile();
   
    static std::pair<int,int> getAppVersionFromDocument( Base::String filename);

    void test_graph();
    void onAddLink( PropertyLinkBaseBase*p, Core::DocObject* from ,Core::DocObject* o );
    void onRemoveLink( PropertyLinkBaseBase*p, Core::DocObject* from ,Core::DocObject* o );
    void onAddLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::list<Core::DocObject*>& linkList );
    void onRemoveLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::list<Core::DocObject*>& linkList);
    void onAddLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::unordered_set<Core::DocObject*>& linkSet );
    void onRemoveLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::unordered_set<Core::DocObject*>& linkSet );

    void onAddBackLink( PropertyLinkBaseBase*p, Core::DocObject* from ,Core::DocObject* o );
    void onRemoveBackLink( PropertyLinkBaseBase*p, Core::DocObject* from ,Core::DocObject* o );
    void onAddBackLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::list<Core::DocObject*>& linkList );
    void onRemoveBackLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::list<Core::DocObject*>& linkList);
    void onAddBackLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::unordered_set<Core::DocObject*>& linkSet );
    void onRemoveBackLinks( PropertyLinkBaseBase*p, Core::DocObject* from ,const std::unordered_set<Core::DocObject*>& linkSet );
    Core::DocObject::IdType getUniqueObjectIdFromInteger(size_t input) const;
    void breakLinks( Core::DocObject* from );
    Core::Link getInLinks(Core::DocObject* docObj);
    Core::Link getInBackLinks(Core::DocObject* docObj);
    Core::Link getOutLinks(Core::DocObject* docObj);
    Core::Link getOutBackLinks(Core::DocObject* docObj);
    bool checkRelGraph();

    bool replaceLink( Core::DocObject* old, Core::DocObject* newLink );

#endif

protected:
    CoreDocument();
    // Copy constructor
    CoreDocument(const CoreDocument& rhs);
    virtual ~CoreDocument(); 

    /// Physically deletes an object without informing the object maps
    virtual void deleteObject(Core::DocObject* o);

    /// Returns the next available unique id
    Core::DocObject::IdType getUniqueObjectId() const;
    
    /// Adds the object to all relevant maps
    virtual void addToDocumentMaps(Core::DocObject* o);
    /// Returns the object that has the same values as 'pc'. Returns '0' if there is no such object.
    Core::DocObject* getImmutableObjectWithSameValues(Base::Type t, const Core::PropertyContainer* pc) const;
    /// Tries to restore an object from a given type name
    virtual Core::DocObject* restoreObject(const std::string& typeName, const std::string& typeHierarchy, const std::string& id);
    void restoreProperty(Core::Property* property,
                         const Base::String& name,
                         Base::AbstractXMLReader& reader,
                         Base::PersistenceVersion& version) override;
    /// Saves the document
    virtual void saveDocument(std::shared_ptr<Base::AbstractWriter> writer, int versionMajor2save, int versionMinor2save, bool showProgress);
    /// Restores the document. Returns the doc version of the restored document
    virtual int restoreDocument(Base::XMLReader& reader, Core::Attachments& attachments);
    /// Build a map of the objects that get saved. Objects that are marked for delete get removed
    virtual std::vector<Core::DocObject*> build_savemap(std::vector<std::string>& delete_log);
    /// Adds objects with status 'New' to the graph
    virtual void addNewObjectsToGraph();
    
    /// After opening a document this method restores the links declared in the document header.
    void resolveLinkInDocument(Core::PropertyLinkBase* link);
    /// Handles renaming of types between versions. This method looks whether it is necessary to create object of different type when restoring
    /// objects. Returns True if something was changed, false when there is no change.
    virtual bool renameTypeFromOlderVersions(int, Base::String&) { return false; }
    /// Is called before restoring objects of a document.
    virtual void checkBeforeObjectRestoring(int, int) {}
    /// Is called when opening a document. Can be overwritten to do some custom check routines.
    virtual void checkAndConfigureOpenedDocument() {}
    /// Is called when opening a document after recompute. Can be overwritten to do some custom check routines.
    virtual void checkAndConfigureOpenedDocumentAfterRecompute(int, int) {}    
    /// Converts document from older version. Is called when a document with an older version number is opened. Returns true if successful, false if
    /// failed to convert.
    virtual bool convertFromOlderVersions(int docVersion, int appVersion);

    virtual bool getPatchedUserTypes(const Base::String& filename, std::map<QString, QString>& id2TypeMap);

    /// Cleans the undo stack. Must be overwritten.
    virtual void cleanUndoStack() {}
    /// Stores directory at given path to zip stream
    virtual void storeDirectory(const QString&, Base::AbstractWriter&) {}
    /// Restores directory to temp
    virtual void restoreDirectory(const QString&) {}

    /// Initialize document.. Can be overwritten to do some custom initialization.
    virtual void initDocument(bool) {}
    /// Returns the object map
    const ObjectMap& getObjectMap() const;
    /// Creates the temporary directory
    void createTempDirectory();
    /// Cleans the temporary directory
    void cleanTempDirectory();
    ///	Adds a guid to the map IF this id is not in use yet.
    bool maybe_add_GUID(const Base::GlobalId& guid, Core::DocObject* o);
    ///	Adds a guid without checking.
    void add_GUID(const Base::GlobalId& guid, Core::DocObject* o);
    ///	Removes a guid without checking.
    void remove_GUID(const Base::GlobalId& guid, Core::DocObject* o);
    /// Saving runs in Threads, wait for finish
    void waitForSaveIsFinished();

    /// Returns true if this document's file is part of catalog
    bool isCatalogFile() const;

    // bool createBackupFile(const Base::String& path, bool savePath);
    bool createBackupFileAfterOpeningDoc(const Base::String& path, bool savePath);

    // Internal, do not use
    void __setEnableTimeStamps__(bool aOnOff);
    bool __getEnableTimeStamps__() const;

    /// checks if a valid transaction is open
    void _checkTransaction(Core::DocObject* pcDelObj, const Property* What, int line);
    /** Open a new command Undo/Redo, an UTF-8 name can be specified
     *
     * @param name: transaction name
     * @param id: transaction ID, if 0 then the ID is auto generated.
     *
     * @return: Return the ID of the new transaction.
     *
     * This function creates an actual transaction regardless of Application
     * AutoTransaction setting.
     */
    int _openTransaction(const char* name = 0, int id = 0);
    /// Internally called by App::Application to commit the Command transaction.
    void _commitTransaction(bool notify = false);
    /// Internally called by App::Application to abort the running transaction.
    void _abortTransaction();
    void _clearRedos();



    DocumentState _state;
    // Map of all objects
    ObjectMap _all_objects_map;
    // For performance reasons we have a vector of all objects
    ObjectVector _all_objects_vector;
    // Map of immutable objects < Type, set of immutable objects >
    ObjectTypeMap _immutableObjectsMap;    
    // The object graph
    //ObjectGraph* _graph;
    // Set of objects per type
    ObjectTypeMap _typeObjects;

    RelGraph* _relGraph;
    RelGraph* _relGraphBackLink;

    std::set<Core::DocObject*> _references;
    std::map<Base::GlobalId, Core::DocObject*> _guid_map;
    std::map<long, Core::DocObject*> _ifcId_map;

    bool _hasErrorObjectsInRecompute = false;
    bool _needRestoreBeforeRecompute = false;
    size_t _recomputeCnt = 0;
    bool mSolvingEnabled = true; /*! To avoid Solver call too early, because it cause early read of Setting */
    

private:
    /// Opens a document from a file. Returns 'True' on success, 'False' on failure.
    bool openFile(const Base::String& filename, bool savePath = true);

    /// Creates an object from type name and adds it to the document
    Core::DocObject* clone_and_replace_Object(const char* typeName, Core::DocObject* base);
    /// Close the Document, for Application only
    bool close(bool dontNotify = false);
    void onNewObjectTransaction(Core::DocObject* aDocObject);
    void _cleanTempDirectory_Helper(const Base::String& dir);
    void _copyFilesInTemp(Core::DocObject* original, Core::DocObject* copy);
    bool _saveFile(Base::String saveFileName, int versionMajor2save, int versionMinor2save, bool toExport, bool saveBackupCopy, bool notify = true);
    void _initNewObject(Core::DocObject* o, const DocObject::IdType& id = "");
    void _saveDocFiles(std::shared_ptr<Base::AbstractWriter> writer, bool notify = true) const;
    bool _docWrite(std::shared_ptr<Base::AbstractWriter> mainwriter,
                   QString tmpfile,
                   QString fileName,
                   bool inThread,
                   bool toExport,
                   bool saveBackupCopy,
                   std::vector<Base::String> tempFilesToDelete);
    void cleanOldTempDirectories();
    void dispatchMsg(const int aMsgId);
    // never make it public, copyShare param must be controlled ONLY from CoreDocument
    Core::DocObject* copyObjectInternal(Core::DocObject* o, DocObjectMap& copyMap, bool standardCopyOfShared = false, bool aCreateNewType = false);

    /// send DocChange notification
    void notifyDocChange(DocChanges::why aWhy, DocMessage aMsgId, const Base::String& aValue);

    /// Restore files from zip while opening document
    bool restoreDocuments(int& docVersion, int& appVersion);
    
    Base::Type m_copyType = Base::Type::badType();
    QString m_importedIFCFile;
    QDateTime _lastBackupFileTime;
    int _backupFilesCounter = 0;
    int _numOfExistBackupFiles = 0;
    bool _onSaveChangeToDefaultUser = false;
    bool _saveBlocksUntilFinished = false;
    Base::String _tmpdirectory;

    // Map for <file suffix / GUID policy>
    std::map<Base::String, Base::GlobalId_Policy> _guidPolicyMap;
    std::map<Base::String, Base::String> _additionalFiles;

    std::list<Transaction*> mUndoTransactions;
    std::map<int, Transaction*> mUndoMap;
    std::list<Transaction*> mRedoTransactions;
    std::map<int, Transaction*> mRedoMap;

    CoreDocumentImpl* _pimpl{};
};

/* @brief This class takes care that time stamping can be securely
 *  deactivated as long as an instance of this class stays in scope.
 *  It restores the old state when the destructor is called.
 */
class LX_CORE_EXPORT DocumentTimeStampSentinel
{
public:
    DocumentTimeStampSentinel() = delete;
    DocumentTimeStampSentinel(Core::CoreDocument* aDoc) : mDoc(aDoc) 
    { 
        mOldEnableTimeStamps = mDoc->__getEnableTimeStamps__();
        mDoc->__setEnableTimeStamps__(false); 
    }

    ~DocumentTimeStampSentinel() 
    { 
        mDoc->__setEnableTimeStamps__(mOldEnableTimeStamps);
    }
    Core::CoreDocument* mDoc;
    bool mOldEnableTimeStamps = true;
};


class LX_CORE_EXPORT DocumentFactory
{
public:
    friend class CoreApplication;
    DocumentFactory() {}
    ~DocumentFactory() {}

    static std::map<std::string, Core::DocumentFactory*> registry;

protected:
    virtual Core::CoreDocument* createByFactory() = 0;
    static Core::CoreDocument* create(const std::string& type);
};


class CoreDocument_Factory : public Core::DocumentFactory
{
    virtual Core::CoreDocument* createByFactory()
    {
        Core::CoreDocument* doc = new Core::CoreDocument;
        return doc;
    }
};

}  // namespace Core



#define DECLARE_DOCUMENT_FACTORY(_factoryName_, _class_) \
    class _factoryName_ : public Core::DocumentFactory \
    { \
    private: \
        virtual Core::CoreDocument* createByFactory() \
        { \
            Core::CoreDocument* doc = new _class_; \
            return doc; \
        } \
    };

#define REGISTER_DOCUMENT_FACTORY(_factoryName_, _class_) Core::DocumentFactory::registry[#_class_] = (Core::DocumentFactory*)new _factoryName_();
