#pragma once
#include <string>
#include <map>
#include <list>

namespace Base
{
template <typename BaseClassType, typename ClassType>
BaseClassType* CreateObject()
{
    return new ClassType();
}

template <typename BaseClassType, typename UniqueIdType>
class Factory
{
protected:
    typedef BaseClassType* (*CreateObjectFunc)();

public:
    typedef typename std::map<UniqueIdType, CreateObjectFunc>::const_iterator ConstIterator;
    typedef typename std::map<UniqueIdType, CreateObjectFunc>::iterator Iterator;

    template <typename ClassType>
    bool Register(UniqueIdType unique_id)
    {
        if (m_object_creator.find(unique_id) != m_object_creator.end())
            return false;

        m_object_creator[unique_id] = &CreateObject<BaseClassType, ClassType>;

        return true;
    }

    bool Unregister(UniqueIdType unique_id) { return (m_object_creator.erase(unique_id) == 1); }

    BaseClassType* Create(UniqueIdType unique_id)
    {
        Iterator iter = m_object_creator.find(unique_id);

        if (iter == m_object_creator.end())
            return NULL;

        return ((*iter).second)();
    }

    ConstIterator GetBegin() const { return m_object_creator.begin(); }
    Iterator GetBegin() { return m_object_creator.begin(); }
    ConstIterator GetEnd() const { return m_object_creator.end(); }
    Iterator GetEnd() { return m_object_creator.end(); }

protected:
    std::map<UniqueIdType, CreateObjectFunc> m_object_creator;
};

/// Abstract base class of all producers
class LX_BASE_EXPORT AbstractProducer
{
public:
    virtual ~AbstractProducer() = default;
    /// overwritten by a concrete producer to produce the needed object
    virtual void* Produce() const = 0;
};

/** Base class of all factories
  * This class has the purpose to produce at runtime instances
  * of classes not known at compile time. It holds a map of so called
  * producers which are able to produce an instance of a special class.
  * Producer can be registered at runtime through e.g. application modules
  */
class LX_BASE_EXPORT Factory2
{
public:
    /// Adds a new producer instance
    void AddProducer(const char* sClassName, AbstractProducer* pcProducer);
    /// returns true if there is a producer for this class registered
    bool CanProduce(const char* sClassName) const;
    /// returns a list of all registered producer
    std::list<std::string> CanProduce() const;

protected:
    /// produce a class with the given name
    void* Produce(const char* sClassName) const;
    std::map<const std::string, AbstractProducer*> _mpcProducers;
    /// construction
    Factory2(void) {}
    /// destruction
    virtual ~Factory2();
};

// --------------------------------------------------------------------

/** The ScriptFactorySingleton singleton
  */
class LX_BASE_EXPORT ScriptFactorySingleton : public Factory2
{
public:
    static ScriptFactorySingleton& Instance(void);
    static void Destruct();

    const char* ProduceScript(const char* sScriptName) const;

private:
    static ScriptFactorySingleton* _pcSingleton;

    ScriptFactorySingleton() = default;
};

inline ScriptFactorySingleton& ScriptFactory()
{
    return ScriptFactorySingleton::Instance();
}

// --------------------------------------------------------------------

/** Script Factory
  * This class produce Scripts.
  * @see Factory
  */
class LX_BASE_EXPORT ScriptProducer : public AbstractProducer
{
public:
    /// Constructor
    ScriptProducer(const char* name, const char* script) : mScript(script)
    {
        ScriptFactorySingleton::Instance().AddProducer(name, this);
    }

    /// Produce an instance
    virtual void* Produce() const
    {
        return (void*)mScript;
    }

private:
    const char* mScript;
};

}  // namespace Base



