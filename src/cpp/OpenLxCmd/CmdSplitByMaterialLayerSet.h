#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
/**
 * @brief   Python interface for "PartCommands::CmdSplitByMaterialLayerSet"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdSplitByMaterialLayerSet : public Core::Command
{
public:
    CmdSplitByMaterialLayerSet();
    explicit CmdSplitByMaterialLayerSet(std::shared_ptr<OpenLxApp::Element> aElem, bool reverseOrder = false);
    explicit CmdSplitByMaterialLayerSet(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems, bool reverseOrder = false);

    virtual ~CmdSplitByMaterialLayerSet() = default;

    bool redo() override;
    bool undo() override;

    std::vector<std::shared_ptr<OpenLxApp::Element>> getNewElements() const;
    std::vector<std::shared_ptr<OpenLxApp::Element>> getNewElements(std::shared_ptr<OpenLxApp::Element> aOldElem) const;

private:
    std::unique_ptr<Core::Command> _cmd = nullptr;
};
}
