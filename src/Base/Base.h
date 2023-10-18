#pragma once
#include <Base/Type.h>

namespace Core
{
class CoreDocument;
}



/// define for subclassing Base::BaseClass
#define TYPESYSTEM_HEADER() \
public: \
    friend class Core::CoreDocument; \
    static Base::Type getClassTypeId(void); \
    virtual Base::Type getTypeId(void) const; \
    static void setIfcNameAndID(const std::string& s, int id); \
    static void init(void); \
    static void* create(void); \
\
private: \
    static Base::Type classTypeId; \
    static std::string ifcEntityName; \
    static int ifcEntityID;


/// define to implement a  subclass of Base::BaseClass
#define TYPESYSTEM_SOURCE_P(_class_) \
    Base::Type _class_::getClassTypeId(void) { return ::_class_::classTypeId; } \
    Base::Type _class_::getTypeId(void) const { return ::_class_::classTypeId; } \
    void _class_::setIfcNameAndID(const std::string& s, int id) \
    { \
        ifcEntityName = s; \
        ifcEntityID = id; \
    } \
    Base::Type _class_::classTypeId = Base::Type::badType(); \
    std::string _class_::ifcEntityName; \
    int _class_::ifcEntityID; \
    void* _class_::create(void) { return  new ::_class_(); }

/// define to implement a  subclass of Base::BaseClass
#define TYPESYSTEM_SOURCE_ABSTRACT_P(_class_) \
    Base::Type _class_::getClassTypeId(void) { return ::_class_::classTypeId; } \
    Base::Type _class_::getTypeId(void) const { return ::_class_::classTypeId; } \
    void _class_::setIfcNameAndID(const std::string& s, int id) \
    { \
        ifcEntityName = s; \
        ifcEntityID = id; \
    } \
    Base::Type _class_::classTypeId = Base::Type::badType(); \
    std::string _class_::ifcEntityName; \
    int _class_::ifcEntityID; \
    void* _class_::create(void) { return 0; }


/// define to implement a subclass of Base::BaseClass
#define TYPESYSTEM_SOURCE(_class_, _parentclass_) \
    TYPESYSTEM_SOURCE_P(_class_); \
    void _class_::init(void) \
    { \
        initSubclass(::_class_::classTypeId, #_class_, #_parentclass_, &(::_class_::create)); \
        initIfcTypes(::_class_::ifcEntityName, ::_class_::classTypeId, ::_class_::ifcEntityID); \
    }

/// define to implement a subclass of Base::BaseClass
#define TYPESYSTEM_SOURCE_ABSTRACT(_class_, _parentclass_) \
    TYPESYSTEM_SOURCE_ABSTRACT_P(_class_); \
    void _class_::init(void) \
    { \
        initSubclass(::_class_::classTypeId, #_class_, #_parentclass_, &(::_class_::create)); \
        initIfcTypes(::_class_::ifcEntityName, ::_class_::classTypeId, ::_class_::ifcEntityID); \
    }

namespace Base
{
/// BaseClass class and root of the type system
class LX_BASE_EXPORT BaseClass
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    static Type getClassTypeId(void);
    virtual Type getTypeId(void) const;
    static void init(void);

    static void* create(void) { return 0; }
    static void setIfcNameAndID(const std::string& n, int id);

    // DG, Debugging, after destructor, this value is 0xDEADBEEF
    long ____deadVal = 0xBADEAFFE;

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
    template <typename T>
    bool isDerivedFrom() const
    {
        return dynamic_cast<const T*>(this);
    }
#endif

    bool isDerivedFrom(const Type type) const { return getTypeId().isDerivedFrom(type); }

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


    void* operator new(size_t size)
    {
        //cout << "Overloading new operator with size: " << size << endl;
        void* p = ::operator new(size);        
        return p;
    }

    void operator delete(void* p)
    {
        //cout << "Overloading delete operator " << endl;
        free(p);
    }

    /*
    BaseClass* operator->() 
    { 
        return this; 
    }
    */

    BaseClass* operator->() 
    { 
        return this; 
    }

    BaseClass* operator->() const
    { 
        BaseClass* me = (BaseClass*)(this);
        return me; 
    }

    /*
    BaseClass* operator->() const 
    { 
        return static_cast<BaseClass*>(this);
    }
    */

private:
    static Type classTypeId;
    static std::string ifcEntityName;
    static int ifcEntityID;

protected:
    static void initSubclass(Base::Type& toInit, const char* ClassName, const char* ParentName, Type::instantiationMethod method = 0);
    static void initIfcTypes(const std::string& s, Base::Type classTypeId, int id);

public:
    /// Construction
    BaseClass() = default;
    /// Destruction
    virtual ~BaseClass();




private:
    int getEntityTypeID();
    std::string getEntityTypeString();
    static int getEntityTypeIDStatic();
    static std::string getEntityTypeStringStatic();
    static std::vector<Base::Type> getLxTypeForIfcEntityTypeID(int id);
    std::vector<Base::Type> getLxTypeForIfcEntityTypeString(std::string& s);
    static int getIfcEntityTypeIDForLxType(Base::Type t);
    static std::map<Base::Type, std::string> getLxTypesMap();

};


template <typename T>
T* cast2(Base::BaseClass* b)
{
    return dynamic_cast<T*>(b);

/*
#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
    if (b && b->isDerivedFrom<T>())
        return (T*)b;
    else
        return 0;
#endif
*/
}

template <typename T>
const T* ccast2(const Base::BaseClass* b)
{
    return dynamic_cast<const T*>(b);
/*
#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
    if (b && b->isDerivedFrom<T>())
        return (T*)b;
    else
        return 0;
#endif
*/
}

}  // namespace Base
