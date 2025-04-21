    #pragma once
#include <Core/Command.h>

#include <App/ComponentType.h>
#include <App/Properties/PropertySetInfo.h>
#include <OpenLxApp/Element.h>


namespace OpenLxCmd
{
/**
 * \brief "CmdAddPropertySet" is used to assign one or more EXISTING Property to a PropertySet.
 */
class LX_OPENLXCMD_EXPORT CmdAddPropertySet : public Core::Command
{
public:
    CmdAddPropertySet() = default;
    CmdAddPropertySet(const std::string& propertySetName, const std::string& propertyName);
    CmdAddPropertySet(const std::string& propertySetName, const std::string& propertyName, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdAddPropertySet(const std::string& propertySetName, const std::string& propertyName, std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);
    CmdAddPropertySet(const std::string& propertySetName, const std::vector<std::string>& propertyNames);
    CmdAddPropertySet(const std::string& propertySetName, const std::vector<std::string>& propertyNames, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdAddPropertySet(const std::string& propertySetName, const std::vector<std::string>& propertyNames, std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);
    ~CmdAddPropertySet() = default;

    bool redo() override;
    bool undo() override;

private:
    std::map<App::ComponentType*, std::map<App::Element*, App::PropertySet*>> _components = {};
    App::Document* _document = nullptr;
    App::PropertySetInfo* _propertySetInfo = nullptr;
    std::vector<Core::PropertyDescriptor *> _propertyDescriptors = {};

    void execute(const std::string& propertySetName, const std::vector<std::string>& propertyNames, const std::vector<App::Element*> &elements);
    Core::PropertyDescriptor* getPropertyDescriptor(const Base::String& propertyName) const;
    App::PropertySet* getPropertySet(const Base::String& propertySetName, App::Element* element) const;
};
}