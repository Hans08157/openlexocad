#pragma once

#include <Base/String.h>
#include <Base/md5.h>

#include <memory>
#include <vector>



namespace Core
{
class DbgInfo;
class DocObject;
}
namespace Topo
{
class Shape;
}


typedef std::shared_ptr<Core::DbgInfo> pDbgInfo;

namespace Core
{
class LX_CORE_EXPORT DbgInfo

#ifndef SWIG
    : public std::enable_shared_from_this<Core::DbgInfo>
#endif

{
public:
    friend class DocObject;

    DbgInfo();
    virtual ~DbgInfo() {}

    // Creates a DbgInfo and calls createMD5()
    template <typename T>
    static std::shared_ptr<T> createDbgInfo(const Base::String& name, const Base::String& value, const Base::String& type, pDbgInfo parent = nullptr)
    {
        std::shared_ptr<T> mp1 = std::make_shared<T>();
        mp1->name = name;
        mp1->value = value;
        mp1->type = type;
        if (parent)
        {
            parent->addChild(mp1);
        }
        return mp1;
    }

    MD5 dbginfo_md5;
    Base::String name;
    Base::String value;
    Base::String type;

    void addChild(pDbgInfo child);
    std::vector<pDbgInfo> getChildren() const;
    // Creates a 'unique' MD5
    void createMD5(const Base::String& prefix);

private:
    void getNameForMD5(Base::String& md5_name);
    std::vector<pDbgInfo> children;
    pDbgInfo parent;
};

// DbgInfo that points to s DocObject
class LX_CORE_EXPORT DbgInfoLink : public Core::DbgInfo
{
public:
    virtual ~DbgInfoLink() {}
    const Core::DocObject* object = nullptr;
};

// DbgInfo for a shape
class LX_CORE_EXPORT DbgInfoShape : public Core::DbgInfo
{
public:
    virtual ~DbgInfoShape() {}
    std::shared_ptr<const Topo::Shape> shape;
};


}  // namespace Core
