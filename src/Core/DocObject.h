#pragma once
#include <Core/PropertyContainer.h>

namespace Base { class AbstractWriter; }
namespace Core { class DbgInfo; }
namespace App
{
class Document;
class ElementTool;
}  // namespace App

namespace Core
{
enum ObjectStatus
{
    Touch = 0,
    Error = 1,
    New = 2,
    Recompute = 3,  // set when the object is currently being recomputed
    Restore = 4,
    Remove = 5,
    PythonCall = 6,
    Destroy = 7,
    Enforce = 8,
    Recompute2 = 9,  // set when the object is being recomputed in the second pass
    PartialObject = 10,
    PendingRecompute = 11,  // set by Document, indicating the object is in recomputation queue
    PendingRemove = 12,     // set by Document, indicating the object is in pending for remove after recompute
    ObjImporting = 13,      // Mark the object as importing
    NoTouch = 14,           // no touch on any property change
    GeoExcluded = 15,       // mark as a member but not claimed by GeoFeatureGroup
    // Expand = 16,                   // indicate the object's tree item expansion status
    // NoAutoExpand = 17,             // disable tree item auto expand on selection for this object
    PendingTransactionUpdate = 18,  // mark that the object expects a call to onUndoRedoFinished() after transaction is finished.

    Prop_PlacementChanged = 20,   // @see P_MODIFY_PLACEMENT
    Prop_LinkChanged = 21,        // @see P_MODIFY_LINK
    Prop_VisibilityChanged = 22,  // @see P_MODIFY_VISIBLITY
    Prop_ShapeChanged = 23,       // @see P_MODIFY_SHAPE
    Prop_AppearanceChanged = 24,  // @see P_MODIFY_APPEARANCE
    Prop_BackLinkChanged = 25,    // @see P_MODIFY_BACKLINK
    Prop_DataChanged = 26,        // @see P_MODIFY_DATA
    Prop_DrawStyle_Changed = 27       // @see P_MODIFY_DRAWSTYLE

};

class DocObject;
class CoreDocument;
class DocObjectNotifier;
struct DocProperties;
typedef std::map<Core::DocObject*, Core::DocObject*> DocObjectMap;

class LX_CORE_EXPORT DocObject : public Core::PropertyContainer
{
    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()

public:
    friend class CoreDocument;
    friend class ::App::Document;
    friend class ::App::ElementTool;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    typedef std::string IdType;

    /// Sets the CoreDocument of this DocObject
    void setDocument(Core::CoreDocument* doc);
    /// Returns the CoreDocument of this DocObject
    Core::CoreDocument* getDocument() const;
    /// Returns the id of the object
    IdType getId() const;
    /// get called before the value is changed
    virtual bool onBeforeChange(Core::Property* p, const Core::Variant& newValue = Core::Variant()) override;
    /// Is called when a property has changed its value
    virtual void onChanged(Core::Property* p);
    /// get called after an undo/redo transaction is finished
    virtual void onUndoRedoFinished();
    /// Checks if the DocObject is executable
    virtual bool isExecutable() const { return false; }
    /// Returns the reference count of this object
    long getRefCount() const;

    virtual std::string getViewProviderName();
    virtual bool hasLazyViewProvider() const;
    virtual bool attachViewProvider() const;
    virtual void breakLinks() override;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Returns the IFC Entity Id (not the GUID)
    virtual long getIfcId() const { return -1L; }

    /// The object should not added to the graph
    virtual bool ignoreInGraph() const { return false; }

    // Chained virtual functions!
    // Shallow copy properties from 'source' to this
    virtual void shallowCopyProperties(const DocObject* source);

    virtual void setNewTimestamp(int) {}
    virtual void setUpdatedTimestamp(int) {}
    virtual void setUpdatedTimestampNoNotify(int){};
    virtual void setDeletedTimestamp(int) {}
    virtual void setImportedTimestamp(int) {}
    virtual int getNewTimestamp() const { return 0; }
    virtual int getUpdatedTimestamp() const { return 0; }
    virtual int getDeletedTimestamp() const { return 0; }
    virtual int getImportedTimestamp() const { return 0; }
    void checkAfterOnDeleted() override;

    bool mustNotify();
    bool hasVisiblityChanged();
    bool hasOnlyVisibilityChanged() const;
    void resetPropertyStatus();

#ifndef SWIG
    bool onChangedDebug(Core::Property* p) override;
    unsigned long getObjectStatus() const { return StatusBits.to_ulong(); }
    bool testObjectStatus(ObjectStatus pos) const { return StatusBits.test((size_t)pos); }
    void setObjectStatus(ObjectStatus pos, bool on) { StatusBits.set((size_t)pos, on); }
#endif


protected:
    DocObject();
    virtual ~DocObject();

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API

#ifndef SWIG

protected:
    void onBeforeChangeProperty(const Property* prop) override;
    void onChangedProperty(const Property* prop) override;
    virtual DocObject* copy(Core::CoreDocument* toCoreDoc, DocObjectMap& copyMap);
    virtual DocObject* shallowCopy(Core::CoreDocument* toDoc);
    virtual DocObject* copyToDifferentType(Base::Type aNewType, DocObjectMap& aCopyMap);

    /** Status bits of the document object
     * The first 8 bits are used for the base system the rest can be used in
     * derived classes to mark special statuses on the objects.
     * The bits and their meaning are listed below:
     *  0 - object is marked as 'touched'
     *  1 - object is marked as 'erroneous'
     *  2 - object is marked as 'new'
     *  3 - object is marked as 'recompute', i.e. the object gets recomputed now
     *  4 - object is marked as 'restoring', i.e. the object gets loaded at the moment
     *  5 - object is marked as 'deleting', i.e. the object gets deleted at the moment
     *  6 - reserved
     *  7 - reserved
     * 16 - object is marked as 'expanded' in the tree view
     */
    std::bitset<32> StatusBits;

#endif

public:
    void ref(void);
    void unref(void);
    void setTimeSlot(int p);
    int getTimeSlot() const;

    std::vector<Base::String> getFilesInTemp() const;
    void addFileInTemp(const Base::String& s);
    void removeFileInTemp(const Base::String& s);
    virtual void fixPathToFileInTemp(const Base::String& s);

    virtual bool replace(Core::DocObject* source, Core::CoreDocument* fromDoc);
    virtual void onCreated();
    virtual void initDocObject();

    Base::String getTypeName() const;
    const char* getTypeCName() const;
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const;
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo(const Core::Property* p) const;

    virtual bool viewProviderDisabled() const { return false; };
    virtual void setViewProviderDisabled(bool){};
    virtual bool isTemporary() const { return false; };
    virtual Base::GlobalId getGlobalId() const;

    /// For internal use only
    void __setId__(const DocObject::IdType& id);
    /// For internal use only. Sets a random GUID.
    virtual Base::GlobalId __createAndSetGUID__();

    virtual bool createSQLColumnNames(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool dataMode);
    virtual bool createSQL(Base::AbstractWriter& /*writer*/, Base::PersistenceVersion& /*save_version*/, bool data) override;

    virtual void collectDocProperties(Core::DocProperties& props) const;



private:
    Core::CoreDocument* _coredoc;  // document in which object resides
    long _refcnt;                  // reference count
    std::string _internalName;     // lexocad internal ID
    int _timeSlot;
    std::vector<Base::String> _filesInTemp;
    DocObjectNotifier* _notifier = nullptr;


    virtual Base::Type getTypeForSave() const;

#endif
};

class LX_CORE_EXPORT ObjectFactory
{
public:
    friend class CoreDocument;
    friend class ::App::Document;

    ObjectFactory(void) {}
    virtual ~ObjectFactory(void) {}
    static std::map<std::string, ObjectFactory*> registry;
    static bool registerFactory(const std::string& name, Core::ObjectFactory* fact);
    static bool isRegistered(const std::string& name);
    static bool isRegistered(const Base::Type t);
    virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) = 0;

private:
    static DocObject* create(Core::CoreDocument* doc, const std::string& type);
};

}  // namespace Core
