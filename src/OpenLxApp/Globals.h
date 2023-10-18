#pragma once

#include <sstream>
#include <string>

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795029
#endif

#ifndef END_OF_LOOP
#define END_OF_LOOP -2
#endif

#ifndef END_OF_FACE
#define END_OF_FACE -1
#endif

namespace OpenLxApp
{
enum class LX_OPENLXAPP_EXPORT SDK_Language
{
    PYTHON,
    CSHARP,
    // CPLUSPLUS -> conflict with cadwork3d
};

enum class LX_OPENLXAPP_EXPORT View_Direction
{
    X,
    Y,
    Z,
    NX,
    NY,
    NZ,
    AXO_LEFT,
    AXO_BACK_LEFT,
};

enum class LX_OPENLXAPP_EXPORT Event
{
    NewDocument,
    CloseDocument,
    SetActiveDocument,
    RecomputeFinished,
    FileOpened,
    NewFile,
    BeforeSave,
    AddSelection,
    RemoveSelection,
    ClearSelection,
    UpdateSelection,
    RemoveActivePoint,
    SetActivePoint,
    // PickedPoint
};

struct LX_OPENLXAPP_EXPORT Version
{
    int major = 0;
    int minor = 0;
    int micro = 0;
    int revision = 0;
    std::string name;

    /**
     * Prints a version string
     *
     * @result        std::string
     *
     * @since         24.0
     * @author        HPK
     * @date          2016-12-11
     */
    std::string toString() const
    {
        std::stringstream ss;
        ss << name << " Version: " << major << "." << minor << " Build " << revision;
        return ss.str();
    }
};

enum class ErrorCode
{
    NoError = 0,
    UnknownError = 1,
    InvalidArguments = 2,
    ResultingGeometryIsInvalid = 3,
    InsufficientArraySize = 4

};
}  // namespace OpenLxApp

#define FORWARD_DECL(x, y) \
    namespace x \
    { \
        class y; \
    }

#define PLUGIN_HEADER(_class_) \
public: \
    std::string getName() override { return #_class_; }

#define PLUGIN_SOURCE(_class_) \
    PLUGINDECL App::Plugin* createPlugin(App::PluginManager& mgr) { return (App::Plugin*)new _class_(); }



/**
 * @brief    If the external application/plug-in developer derives from a Doc.Object class
 *           to extend the functionality of Lexocad there must be an OpenLexocad Proxy class
 *           for the derived class to be able to work with the OpenLexocad API.
 *           These macros provide the automatic declaration and implementation of the
 *           Proxy classes.
 *
 * @since    24.0
 * @author   HPK
 * @date     2017-01-10
 */
#define OBJECT_HEADER(_class_, _type_) \
public: \
    static LxIfc4::LxIfc4EntityEnum getEntityType_Static() { return LxIfc4::_type_; } \
\
    explicit _class_(std::shared_ptr<_class_> other) { _coreObj = other->_coreObj; } \
    _class_& operator=(std::shared_ptr<_class_> other) \
    { \
        _coreObj = other->_coreObj; \
        return *this; \
    } \
    friend bool operator==(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return x->_coreObj == y->_coreObj; } \
    friend bool operator!=(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return !(x == y); } \
    friend bool operator<(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return x->_coreObj < y->_coreObj; } \
    friend bool operator>(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return y < x; } \
    friend bool operator<=(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return !(x > y); } \
    friend bool operator>=(std::shared_ptr<_class_> x, std::shared_ptr<_class_> y) { return !(x < y); } \
    bool isEqual(std::shared_ptr<_class_> other) const /*For Python*/ { return (_coreObj == other->_coreObj); }

#define PROXY_HEADER_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
    OBJECT_HEADER(_openlexocadclass_, _type_) \
public: \
    _openlexocadclass_(_corelexocadclass_* aObj); \
\
public: \
    _corelexocadclass_* __getCasted__() const;


#define PROXY_HEADER(_openlexocadclass_, _corelexocadclass_, _type_) \
    PROXY_HEADER_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
public: \
    _openlexocadclass_(std::shared_ptr<OpenLxApp::Document> aDoc); \
\
public: \
    static std::shared_ptr<_openlexocadclass_> createIn(std::shared_ptr<OpenLxApp::Document> aDoc); \
\
public: \
    static std::shared_ptr<_openlexocadclass_> createFrom(_corelexocadclass_* aObj);


#ifdef _DEBUG
#define PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
    _corelexocadclass_* _openlexocadclass_::__getCasted__() const \
    { \
        auto casted = dynamic_cast<_corelexocadclass_*>(_coreObj); \
        assert(casted); \
        return casted; \
    }
#define PROXY_SOURCE(_openlexocadclass_, _corelexocadclass_, _type_) \
    PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
    _openlexocadclass_::_openlexocadclass_(std::shared_ptr<OpenLxApp::Document> aDoc) \
    /* TODO: ADD CALL TO SUPER CLASS */ { _coreObj = aDoc->__getInternalDoc__()->createObject<_corelexocadclass_>(); } \
    std::shared_ptr<_openlexocadclass_> _openlexocadclass_::createIn(std::shared_ptr<OpenLxApp::Document> aDoc) \
    { \
        auto obj = aDoc->__getInternalDoc__()->createObject<_corelexocadclass_>(); \
        assert(obj); \
        if(obj) return std::make_shared<_openlexocadclass_>(obj); \
        else return nullptr;\
    } \
    std::shared_ptr<_openlexocadclass_> _openlexocadclass_::createFrom(_corelexocadclass_* aObj) \
    { \
        if(aObj) return std::make_shared<_openlexocadclass_>(aObj); \
        else return nullptr; \
    }
#define PROXY_SOURCE_CUSTOM_CREATE(_openlexocadclass_, _corelexocadclass_, _type_) \
    PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_)
#else
#define PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
    _corelexocadclass_* _openlexocadclass_::__getCasted__() const \
    { \
        auto casted = dynamic_cast<_corelexocadclass_*>(_coreObj); \
        return casted; \
    }
#define PROXY_SOURCE(_openlexocadclass_, _corelexocadclass_, _type_) \
    PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_) \
    _openlexocadclass_::_openlexocadclass_(std::shared_ptr<OpenLxApp::Document> aDoc) \
    /* TODO: ADD CALL TO SUPER CLASS */ { _coreObj = aDoc->__getInternalDoc__()->createObject<_corelexocadclass_>(); } \
    std::shared_ptr<_openlexocadclass_> _openlexocadclass_::createIn(std::shared_ptr<OpenLxApp::Document> aDoc) \
    { \
        auto obj = aDoc->__getInternalDoc__()->createObject<_corelexocadclass_>(); \
        if(obj) return std::make_shared<_openlexocadclass_>(obj); \
        else return nullptr; \
    } \
    std::shared_ptr<_openlexocadclass_> _openlexocadclass_::createFrom(_corelexocadclass_* aObj) \
    { \
        if(aObj) return std::make_shared<_openlexocadclass_>(aObj); \
        else return nullptr; \
    }
#define PROXY_SOURCE_CUSTOM_CREATE(_openlexocadclass_, _corelexocadclass_, _type_) \
    PROXY_SOURCE_ABSTRACT(_openlexocadclass_, _corelexocadclass_, _type_)
#endif


#define EXT_FORWARD_DECL(_class_) class _class_##_Proxy;

#define EXT_DECLARE_PROXYOBJECT(_class_, _parentclass_) \
    class _class_##_Proxy : public _parentclass_ \
    { \
        OBJECT_HEADER(_class_##_Proxy, IFC_ENTITY_UNDEFINED) \
    public: \
        _class_##_Proxy(_class_* aObject) : _parentclass_(aObject) { assert(aObject); } \
        virtual ~_class_##_Proxy(void) {} \
\
    protected: \
        _class_##_Proxy() {} \
    }; \
    DECLARE_OBJECT_FACTORY(_class_##_Factory, _class_, IFC_ENTITY_UNDEFINED);


#define EXT_OBJECT_SOURCE(_class_, _parent_) \
    TYPESYSTEM_SOURCE(_class_, _parent_) \
    LX_NODE_SOURCE(_class_, _parent_)

#define EXT_FORWARD_DECL(_class_) class _class_##_Proxy;

/**
 * @brief    DECL_PROPERTY and DEFINE_PROPERTY are macros used for
 *           mapping between the properties of Lexocad objects
 *           and their corresponding getter setter in OpenLexocad.
 *
 * @since    24.0
 * @author   HPK
 * @date     2017-01-26
 */
#define DECL_PROPERTY(_class_, _name_, _type_) \
public: \
    _type_ get##_name_() const; \
\
public: \
    void set##_name_(const _type_& aValue);

#define DEFINE_PROPERTY(_class_, _name_, _propname_, _type_) \
    _type_ _class_::get##_name_() const { return __getCasted__()->_propname_.getValue(); } \
    void _class_::set##_name_(const _type_& aValue) { __getCasted__()->_propname_.setValue(aValue); }
