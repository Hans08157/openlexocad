/**
 * @file
 * Singleton template macro definition.
 * Use this macros to define singleton classes.
 *
 * @author Tomáš "Shamot" Burian
 */
#pragma once
#error "This is shit, do not include pls";

//----------------------------------------------------------------------------
// DECLARATIONs
//----------------------------------------------------------------------------

/**
 * Singleton class declaration. Must be in a header file.
 * Example:
 *
 * class ClassX
 * {
 *   DECLARE_SINGLETON(ClassX);
 * };
 *
 */
#define DECLARE_SINGLETON(CLASSNAME) \
\
public: \
    static CLASSNAME* instance(); \
    static void destroy(); \
\
protected: \
    CLASSNAME(); \
    ~CLASSNAME(); \
\
private: \
    static CLASSNAME* _instance;



/**
 * Singleton class definition. Must be in a cpp file.
 * Example:
 *
 * DEFINE_SINGLETON(ClassX);
 *
 * Continue to define class constructor and destructor:
 *
 * ClassX::ClassX() {};
 *
 * ClassX::~ClassX() {};
 *
 *
 */
#define DEFINE_SINGLETON(CLASSNAME) \
    CLASSNAME* CLASSNAME::_instance = nullptr; \
\
    CLASSNAME* CLASSNAME::instance() \
    { \
        if (!_instance) \
        { \
            _instance = new CLASSNAME; \
        } \
        return _instance; \
    } \
\
    void CLASSNAME::destroy() \
    { \
        delete _instance; \
        _instance = nullptr; \
    }
