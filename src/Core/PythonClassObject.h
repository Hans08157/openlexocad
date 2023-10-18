#pragma once

#include <Core/DocObject.h>
#include <Core/PropertyBackLink.h>
#include <Core/PropertyLink.h>
#include <Core/PropertyGUID.h>
#include <Core/PropertyText.h>
#include <Core/PropertyInteger.h>
#include <Core/StandardManipulatorPolicy.h>


namespace Core
{
class PythonScriptObject;
class PropertyDescriptor;
    /**
 * @brief Keeps the information about a Python class like class name,
 * the super class etc. Also keeps the information how properties are
 * displayed.
 *
 * @ingroup
 * @since    24.0
 */
class LX_CORE_EXPORT PythonClassObject : public Core::DocObject
{
    typedef Core::DocObject inherited;

    TYPESYSTEM_HEADER()
    LX_NODE_HEADER()

public:
    friend class PythonClassObject_Factory;

    PropertyBackLink<PythonScriptObject*> pythonScriptObject;  // Link to the Python Script
    PropertyGUID classId;                                      // The class Id
    PropertyText className;                                    // The class name
    PropertyText superClassName;                               // The name of the super class
    PropertyUInt64 standardManipulatorPolicy;                  // The StandardManipulatorPolicy in the UI
    PropertyText propertyHeader;                               // The header text in the UI
    PropertyIndex translatorHeader;                            // Index of the translator text
    PropertyText propertyGroupName;                            // The group name in the UI
    PropertyIndex translatorGroupName;                         // Index of the translator text

    Core::StandardManipulatorPolicy getStandardManipulatorPolicy() const;
    void setStandardManipulatorPolicy(const Core::StandardManipulatorPolicy& aPolicy);
    void setPropertyHeader(const Base::String& aDefaultName, int aTranslationId = -1);
    void setPropertyGroupName(const Base::String& aDefaultName, int aTranslationId = -1);
    Base::String getPropertyHeader() const;
    int getTranslationHeader() const;
    Base::String getPropertyGroupName() const;
    int getTranslationGroupName() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool mustBeSaved() const override;
    static bool isRegistered(const Base::GlobalId& aClassId);
    static bool registerClass(PythonClassObject* aClassObject);
    static PythonClassObject* getRegisteredClass(const Base::GlobalId& aClassId);

    bool restorePythonInstance(const Base::GlobalId& aObjectId);
    // static Base::String getPythonClassName(PyObject* aObject);

    std::list<PropertyDescriptor*> getPropertyDescriptorList() const;
    std::map<std::string, PropertyDescriptor*> getPropertyDescriptorMap() const;
    void addPropertyDescriptor(PropertyDescriptor* aDescriptor);
    PropertyDescriptor* getPropertyDescriptorByName(const std::string& aName);

    PythonClassObject();
    virtual ~PythonClassObject();

private:
    PropertyLinkList scriptParamConfig;  // Configuration of the ScriptParams
    static std::map<Base::GlobalId, PythonClassObject*> classRegistry;

protected:
    Core::DocObject* copy(Core::CoreDocument* toDoc, DocObjectMap& copyMap ) override;
};
DECLARE_OBJECT_FACTORY_NOIFC(Core::PythonClassObject_Factory, Core::PythonClassObject);
}  // namespace Core
