#pragma once
#include <Core/DbgInfo.h>
#include <LxIfc4/IFC4_impl/LxIfc4EntityEnums.h>
#include <OpenLxApp/Property.h>

#include <memory>
#include <string>

namespace Core
{
class DocObject;
class CoreDocument;
}  // namespace Core

namespace OpenLxApp
{
class Document;

/**
 * @brief DocObject is the base class of all persistent objects.
 * The DocObject belongs to exactly one Document.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT DocObject
{
public:
    friend class Document;
    std::shared_ptr<Document> getDocument() const;

    bool isNew() const;
    bool isUpdated() const;
    bool isValid() const;
    bool hasErrors() const;
    void touch();

    LxIfc4::LxIfc4EntityEnum getEntityType() const;
    std::string getEntityTypeAsString() const;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const;

    DocObject(Core::DocObject* aObject);
    virtual ~DocObject(void);

protected:
    DocObject();
    Core::DocObject* _coreObj = nullptr;  

public:
    // For internal use only
    Core::DocObject* __getObj__() const;
};
}  // namespace OpenLxApp