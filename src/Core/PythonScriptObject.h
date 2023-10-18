#pragma once 

#include <Core/DocObject.h>
#include <Core/PropertyGUID.h>
#include <Core/PropertyBoolean.h>
#include <Core/PropertyText.h>

namespace Core
{
class LX_CORE_EXPORT PythonScriptObject : public Core::DocObject
{
    typedef Core::DocObject inherited;

    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()
public:
    friend class PythonScriptObject_Factory;

    PythonScriptObject();

    PropertyGUID scriptId;       // The Script Id
    PropertyText scriptPath;     // The Script path
    PropertyBoolean isExternal;  // Flag if Script is internal or external

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool mustBeSaved() const override;

    static bool isRegistered(const Base::GlobalId& aScriptId);
    static bool registerScript(PythonScriptObject* aScriptObject);
    static PythonScriptObject* getRegisteredScript(const Base::GlobalId& aScriptPath);

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap ) override;

private:
    static std::map<Base::GlobalId, Core::PythonScriptObject*> scriptRegistry;
};

DECLARE_OBJECT_FACTORY_NOIFC(PythonScriptObject_Factory, PythonScriptObject);
}  // namespace Core