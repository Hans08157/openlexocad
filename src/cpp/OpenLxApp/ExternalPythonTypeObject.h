#pragma once

#include <OpenLxApp/Document.h>
#include <OpenLxApp/Property.h>


namespace Core
{
class PropertyScriptParam;
}

namespace OpenLxApp
{
/**
 * @brief DEPRECATED. Do not use!
 *
 */
class LX_OPENLXAPP_EXPORT ExternalPythonTypeObject : public DocObject
{
public:
    PropertyString typeName;
    PropertyString fileName;
    PropertyString scriptGUID;
    PropertyString scalingCB;


    Core::PropertyScriptParam* getPropertyScriptParam(const std::string& aName);
    Core::PropertyScriptParam* addPropertyScriptParam(const std::string& aName, const Core::Variant& aValue);
    void removePropertyScriptParam(const std::string& aName);
    static ExternalPythonTypeObject* createIn(std::shared_ptr<OpenLxApp::Document> aDoc);

    virtual ~ExternalPythonTypeObject(void);

protected:
    ExternalPythonTypeObject(void);
};
}  // namespace OpenLxApp