#pragma once 

#include <map>

namespace Core
{
class DocObject;
typedef std::map<Core::DocObject*, Core::DocObject*> DocObjectMap;
/**
 * @brief The SharedObject is an interface that must be implemented by all classes that want to share their resources when
 * copied within the same document.
 *
 * Derived classes must implement the 'copyShared()' method. These objects are treated differently in @see Core::CoreDocument::copyObject().
 * The standard implementation is:
 * @code
 * virtual Core::DocObject* copyShared(Core::CoreDocument* toDoc, DocObjectMap &copyMap = DocObjectMap()) override
 * {
 *     if (getDocument() == toDoc) return this;
 *     else return App::LxObject::copy(toDoc, copyMap);
 * }
 * @endcode
 *
 * @ingroup  XXX
 * @since    26.0
 */
class LX_CORE_EXPORT SharedObject
{
public:
    friend class CoreDocument;
    virtual ~SharedObject() = default;

protected:
    virtual Core::DocObject* copyShared(Core::CoreDocument* toDoc, DocObjectMap& copyMap) = 0;
};

}  // namespace Core