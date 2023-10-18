#pragma once


#define LX__QUOTE(str) #str

// FIXME: document. 20000103 mortene.
#define LX_NODE_HEADER() \
public: \
    static void lx_field_init(); \
\
protected: \
    static const Core::LxFieldData** getFieldDataPtr(void); \
    virtual const Core::LxFieldData* getFieldData(void) const; \
    virtual const Core::LxFieldData* getParentFieldData(void) const; \
\
private: \
    static const Core::LxFieldData** parentFieldData; \
    static Core::LxFieldData* fieldData; \
    static unsigned int classinstances; \
    static bool lxFieldIsInit;

#define LX_NODE_ABSTRACT_SOURCE(_class_) \
\
    unsigned int ::_class_::classinstances = 0; \
    const Core::LxFieldData** ::_class_::parentFieldData = (const Core::LxFieldData**)0xdeadbeefLL; \
    Core::LxFieldData* ::_class_::fieldData = nullptr; \
    bool ::_class_::lxFieldIsInit = false; \
\
    const Core::LxFieldData** _class_::getFieldDataPtr(void) { return const_cast<const Core::LxFieldData**>(&::_class_::fieldData); } \
\
    const Core::LxFieldData* _class_::getFieldData(void) const { return ::_class_::fieldData; } \
\
    const Core::LxFieldData* _class_::getParentFieldData(void) const { return *(::_class_::parentFieldData); }

#define LX_INIT(_class_, _parentclass_) \
    void _class_::lx_field_init() \
    { \
        ::_class_::parentFieldData = ::_parentclass_::getFieldDataPtr(); \
        ::_class_::lxFieldIsInit = true; \
    }

#define LX_INIT_NO_PARENT(_class_) \
    void _class_::lx_field_init() \
    { \
        _class_::parentFieldData = 0; \
        _class_::lxFieldIsInit = true; \
    }

#define LX_NODE_SOURCE(_class_, _parentclass_) \
    LX_NODE_ABSTRACT_SOURCE(_class_) \
    LX_INIT(_class_, _parentclass_)

#define LX_NODE_SOURCE_NO_PARENT(_class_) \
    LX_NODE_ABSTRACT_SOURCE(_class_) \
    LX_INIT_NO_PARENT(_class_)


#define LX_NODE_CONSTRUCTOR(_class_) \
    do \
    { \
        ::_class_::classinstances++; \
        /* Catch attempts to use a node class which has not been initialized. */ \
        /* assert(_class_::classTypeId != SoType::badType() && "you forgot init()!"); */ \
        /* Initialize a field data container for the class only once. */ \
        assert(::_class_::lxFieldIsInit && "\nClass not init!\n"); \
        assert((::_class_::parentFieldData != (const Core::LxFieldData**)0xdeadbeefLL) && "\nParent-Class not init\n"); \
        if (!::_class_::fieldData) \
        { \
            ::_class_::fieldData = new Core::LxFieldData(::_class_::parentFieldData ? *::_class_::parentFieldData : nullptr); \
        } \
        /* Extension classes from the application programmers should not be \
           considered native. This is important to get the export code to do \
           the Right Thing. */ \
\
        Core::PropertyContainer::isValid(); \
\
    } while (0); \
    Core::PostInitClass __postInit__(this)


#define LX_PRIVATE_COMMON_INIT_CODE(_class_, _parentclass_) \
    do \
    { \
        /* Store parent's field data pointer for later use in the constructor. */ \
        _class_::parentFieldData = _parentclass_::getFieldDataPtr(); \
    } while (0)

#define LX_NODE_INIT_CLASS_NO_PARENT(_class_) \
    do \
    { \
        _class_::parentFieldData = 0; \
        _class_::lxFieldIsInit = true; \
    } while (0)


#define LX_NODE_INIT_CLASS(_class_, _parentclass_) \
    do \
    { \
        LX_PRIVATE_COMMON_INIT_CODE(_class_, _parentclass_); \
        _class_::lxFieldIsInit = true; \
    } while (0)

#define LX_NODE_ADD_FIELD(_field_, _defaultval_) \
    do \
    { \
        fieldData->addField(this, LX__QUOTE(_field_), &this->_field_); \
    } while (0)

#ifndef LXAPI

#define CONCATSTR(a, b) a##b

#define BUILDCLASS(CLASS, NAME, CTR, CTR2) \
    class CONCATSTR(NAME, CTR) \
    { \
    public: \
        CONCATSTR(NAME, CTR)() { CLASS::setIfcNameAndID(LX__QUOTE(NAME), LxIfc4::NAME); } \
    }; \
    static CONCATSTR(NAME, CTR) CONCATSTR(NAME, CTR2);

#ifdef SWIG

#define DECLARE_OBJECT_FACTORY_IFC(_factoryName_, _class_, _ifc4Class_, _ifc3Class_)

#else

#define DECLARE_OBJECT_FACTORY_IFC(_factoryName_, _class_, _ifc4Class_, _ifc3Class_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            o->setIfc3EntityType(LxIfc3::_ifc3Class_); \
            o->setIfc4EntityType(LxIfc4::_ifc4Class_); \
            o->setIfc4x3EntityType(LxIfc4x3::EntityFactory::getClassIDForString(LX__QUOTE(_ifc4Class_))); \
            return o; \
        } \
    }; \
    BUILDCLASS(_class_, _ifc4Class_, __COUNTER__, __COUNTER__)

#endif

#else
#define DECLARE_OBJECT_FACTORY_IFC(_factoryName_, _class_, _ifc4Class_, _ifc3Class_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            return o; \
        } \
    };
#endif

#ifndef LXAPI

#ifdef SWIG

#define DECLARE_OBJECT_FACTORY_IFC4X3(_factoryName_, _class_, _aIfcClass_, _bIfcClass_)

#else

/**
 * \brief DECLARE_OBJECT_FACTORY_IFC4X3
 * \param _factoryName_
 * \param _class_
 * \param _aIfcClass_ - IFC version == 4X3
 * \param _bIfcClass_ - IFC version != 4X3
 */
#define DECLARE_OBJECT_FACTORY_IFC4X3(_factoryName_, _class_, _aIfcClass_, _bIfcClass_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            o->setIfc3EntityType(LxIfc3::_bIfcClass_); \
            o->setIfc4EntityType(LxIfc4::_bIfcClass_); \
            o->setIfc4x3EntityType(LxIfc4x3::EntityFactory::getClassIDForString(LX__QUOTE(_aIfcClass_))); \
            return o; \
        } \
    }; \
    BUILDCLASS(_class_, _aIfcClass_, __COUNTER__, __COUNTER__)

#endif

#else
#define DECLARE_OBJECT_FACTORY_IFC4X3(_factoryName_, _class_, _aIfcClass_, _bIfcClass_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            return o; \
        } \
    };
#endif

#ifndef LXAPI

#ifdef SWIG

#define DECLARE_OBJECT_FACTORY(_factoryName_, _class_, _ifcClass_)
#define DECLARE_OBJECT_FACTORY_NOIFC(_factoryName_, _class_)

#else

#define DECLARE_OBJECT_FACTORY(_factoryName_, _class_, _ifcClass_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            o->setIfc3EntityType(LxIfc3::_ifcClass_); \
            o->setIfc4EntityType(LxIfc4::_ifcClass_); \
            o->setIfc4x3EntityType(LxIfc4x3::EntityFactory::getClassIDForString(LX__QUOTE(_ifcClass_))); \
            return o; \
        } \
    }; \
    BUILDCLASS(_class_, _ifcClass_, __COUNTER__, __COUNTER__)



#define DECLARE_OBJECT_FACTORY_NOIFC(_factoryName_, _class_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            return o; \
        } \
    }; \
    //BUILDCLASS(_class_, _ifcClass_, __COUNTER__, __COUNTER__)

#endif


#else
#define DECLARE_OBJECT_FACTORY(_factoryName_, _class_, _ifcClass_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            return o; \
        } \
    };

#define DECLARE_OBJECT_FACTORY_NOIFC(_factoryName_, _class_) \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_; \
            o->setDocument(doc); \
            return o; \
        } \
    };

#endif

#define DECLARE_TEMPLATE_OBJECT_FACTORY(_factoryName_, _class_, _ifcClass_) \
    template <class T> \
    class _factoryName_ : public Core::ObjectFactory \
    { \
    private: \
        virtual Core::DocObject* createByFactory(Core::CoreDocument* doc) \
        { \
            auto o = new _class_<T>; \
            o->setDocument(doc); \
            o->setIfc3EntityType(LxIfc3::_ifcClass_); \
            /*o->setLxIfcEntity( std::shared_ptr<LxIfc3::LxIfc3Entity>( LxIfcEntityFactory::createIfc3Entity<_ifcClass_> ) );*/ \
            return o; \
        } \
    };


#define REGISTER_OBJECT_FACTORY(_factoryName_, _class_) Core::ObjectFactory::registry[#_class_] = (Core::ObjectFactory*)new _factoryName_();

#define INIT_PROPERTY_TEMPLATES(_class_) \
    Core::PropertyLink<_class_*>::init(qPrintable(QString("PropertyLink[%1]").arg(#_class_))); \
    Core::PropertyLinkSet<_class_*>::init(qPrintable(QString("PropertyLinkSet[%1]").arg(#_class_))); \
    Core::PropertyBackLink<_class_*>::init(qPrintable(QString("PropertyBackLink[%1]").arg(#_class_))); \
    Core::PropertyBackLinkSet<_class_*>::init(qPrintable(QString("PropertyBackLinkSet[%1]").arg(#_class_))); \
    Core::PropertyTypedLinkList<_class_*>::init(qPrintable(QString("PropertyTypedLinkList[%1]").arg(#_class_)));

#define DECLARE_PROPERTY_TEMPLATES(_class_, _export_symbol_) \
    template class _export_symbol_ Core::PropertyLink<_class_*>; \
    template class _export_symbol_ Core::PropertyLinkSet<_class_*>; \
    template class _export_symbol_ Core::PropertyBackLink<_class_*>; \
    template class _export_symbol_ Core::PropertyBackLinkSet<_class_*>; \
    template class _export_symbol_ Core::PropertyTypedLinkList<_class_*>;

#define CREATE_FOR_TEST(_class_) \
    do \
    { \
        class R : public _class_ \
        { \
        public: \
            R(){}; \
            virtual ~R(){}; \
        }; \
\
        auto v = new R(); \
        v->check_lx(#_class_, __FUNCTION__); \
        delete v; \
    } while (false);



#define TYPE_FOR_SAVE_IS_PARENT() \
private: \
    Base::Type getTypeForSave() { return getTypeId().getParent(); }



#define __INIT_OBJECT(_class_) \
    _class_::init(); \
    INIT_PROPERTY_TEMPLATES(_class_)

#define LX_INIT_OBJECT(_class_) \
    _class_::init(); \
    _class_::lx_field_init(); \
    CREATE_FOR_TEST(_class_) \
    INIT_PROPERTY_TEMPLATES(_class_)

#define LX_INIT_OBJECT_LINK(_class_) \
    _class_::init(); \
    _class_::lx_field_init(); \
    CREATE_FOR_TEST(_class_) \
    INIT_PROPERTY_TEMPLATES(_class_)

#define LX_INIT_OBJECT_ABSTRACT(_class_) \
    _class_::init(); \
    _class_::lx_field_init(); \
    INIT_PROPERTY_TEMPLATES(_class_)
