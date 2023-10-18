    #pragma once
#include <Core/Command.h>

#include <App/ComponentType.h>
#include <App/Properties/PropertySetInfo.h>
#include <OpenLxApp/Element.h>

#include "Gui/CA_Command_5.h"


    namespace OpenLxCmd
{
/**
 * \brief "CmdModifyPropertySetValue" is used to assign a value to ane EXISTING Property in a PropertySet.
 */
class LX_OPENLXCMD_EXPORT CmdModifyPropertySetValue : public Core::Command
{
public:
    CmdModifyPropertySetValue() = default;
    CmdModifyPropertySetValue(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue);
    CmdModifyPropertySetValue(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdModifyPropertySetValue(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue, std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);
    ~CmdModifyPropertySetValue() = default;

    bool redo() override;
    bool undo() override;

private:
    void execute(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue, const std::vector<App::Element*> &elements);
    App::PropertySetDefinition* getPropertySetDefinition(const Base::String& propertySetName, App::Element* element) const;

    std::unique_ptr<CmdRunCommands> _commands;
};
}
