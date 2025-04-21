#pragma once
#include <map>
#include <set>
#include <string>
#include <vector>


namespace Base
{
struct TypeData;


/** Type system class
  Many of the classes in the Lexocad must have their type
  information registered before any instances are created (including,
  but not limited to: Object, Property...
  ). The use of Type to store this information provides
  lots of various functionality for working with class hierarchies,
  comparing class types, instantiating objects from classnames, etc
  etc.

  It is for instance possible to do things like this:

  \code
  void getRightFeature(Base::Base * anode)
  {
    assert(anode->isDerivedFrom<App::Feature>());

    if (anode->getTypeId() == Mesh::MeshFeature::getClassTypeId()) {
      // do something..
    }
    else if (anode->getTypeId() == Part::PartFeature::getClassTypeId()) {
      // do something..
    }
    else {
      Base::Console().Warning("getRightFeature", "Unknown feature type %s!\n",
                                anode->getTypeId().getName());
    }
  }
  \endcode

  A notable feature of the Type class is that it is only 16 bits
  long and therefore should be passed around by value for efficiency
  reasons.

  One important note about the use of Type to register class
  information: super classes must be registered before any of their
  derived classes are.
*/
class LX_BASE_EXPORT Type
{
public:
    /// Construction
    Type(const Type& type);
    Type(void);
    /// Destruction
    virtual ~Type() = default;

    /// creates a instance of this type
    void* createInstance(void);
    /// creates a instance of the named type
    static void* createInstanceByName(const char* TypeName, bool bLoadModule = false);

    typedef void* (*instantiationMethod)(void);

    static Type fromName(const char* name);

    inline const Type getParent(void) const;
    inline void getChildren(std::set<Type>& children) const;
    inline void getAllChildren(std::set<Type>& children) const;
    inline bool isDerivedFrom(const Type type) const;
    inline bool isDerivedFrom(const std::vector<Base::Type>& types) const;

    /// Returns all types derived from type
    static int getAllDerivedFrom(const Type type, std::vector<Type>& List);
    static std::vector<Type> getAllDerivedFrom(const Type type);
    /// Returns the hierarchy of type t in backward order as a string
    static std::string getHierarchyAsString(Base::Type t);

    static int getNumTypes(void);

    static const Type createType(const Type parent, const char* name, instantiationMethod method = 0);

    unsigned int getKey(void) const;
    bool isBad(void) const;
    const std::string& getName(void) const;

    inline void operator=(const Type type);
    inline bool operator==(const Type type) const;
    inline bool operator!=(const Type type) const;

    inline bool operator<(const Type type) const;
    inline bool operator<=(const Type type) const;
    inline bool operator>=(const Type type) const;
    inline bool operator>(const Type type) const;

    inline static const Type badType(void) { return Type(); }
    static void init(void);

protected:
    static std::string getModuleName(const char* ClassName);


private:
    unsigned int index;

    static std::map<std::string, unsigned int> typemap;
    static std::vector<TypeData*> typedata;
    static std::set<std::string> loadModuleSet;

    static std::vector<unsigned int> typeVector;
    static std::map<unsigned int, unsigned int> typederivated;
};


inline unsigned int Type::getKey(void) const
{
    return this->index;
}

inline bool Type::operator!=(const Type type) const
{
    return (this->getKey() != type.getKey());
}

inline void Type::operator=(const Type type)
{
    this->index = type.getKey();
}

inline bool Type::operator==(const Type type) const
{
    return (this->getKey() == type.getKey());
}

inline bool Type::operator<(const Type type) const
{
    return (this->getKey() < type.getKey());
}

inline bool Type::operator<=(const Type type) const
{
    return (this->getKey() <= type.getKey());
}

inline bool Type::operator>=(const Type type) const
{
    return (this->getKey() >= type.getKey());
}

inline bool Type::operator>(const Type type) const
{
    return (this->getKey() > type.getKey());
}

inline bool Type::isBad(void) const
{
    return (this->index == 0);
}



}  // namespace Base
