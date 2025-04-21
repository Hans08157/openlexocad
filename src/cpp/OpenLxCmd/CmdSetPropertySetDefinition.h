#pragma once

#include <Core/Command.h>

namespace OpenLxCmd
{
/**
 * @brief   Python interface for "PartCommands::CmdSetPropertySetDefinition"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdSetPropertySetDefinition : public Core::Command
{
public:
    CmdSetPropertySetDefinition() = default;
    ~CmdSetPropertySetDefinition() = default;

    /*
     * Signatures to DELETE a Property (only working for "PropertySets" not for "PredefinedPropertySets")
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    /*
     * Signatures to ADD/MODIFY a "bool"
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const bool& propertyValue);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const bool& propertyValue, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const bool& propertyValue, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    /*
     * Signatures to ADD/MODIFY a "double"
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const double& propertyValue);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const double& propertyValue, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const double& propertyValue, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    /*
     * Signatures to ADD/MODIFY a "std::string"
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::string& propertyValue);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::string& propertyValue, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::string& propertyValue, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    /*
     * Signatures to ADD/MODIFY a "Core::Variant"
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const Core::Variant& propertyValue, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    /*
     * Signatures to ADD/MODIFY an "Enum"
     */
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::vector<std::string>& propertyValue, const int& index);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::vector<std::string>& propertyValue, const int& index, std::shared_ptr<OpenLxApp::Element> aElement);
    CmdSetPropertySetDefinition(const std::string& propertySetName, const std::string& propertyName, const std::vector<std::string>& propertyValue, const int& index, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElements);

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd = nullptr;
};
}
