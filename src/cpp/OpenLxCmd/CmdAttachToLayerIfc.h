#pragma once
#include <Core/Command.h>
#include <OpenLxApp/LayerIfc.h>

#include <memory>
#include <vector>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 */
class LX_OPENLXCMD_EXPORT CmdAttachToLayerIfc : public Core::Command
{
public:
    CmdAttachToLayerIfc();
    CmdAttachToLayerIfc(const std::shared_ptr<OpenLxApp::LayerIfc>& aLayerIfc, const std::shared_ptr<OpenLxApp::Element>& aElem);
    CmdAttachToLayerIfc(const std::shared_ptr<OpenLxApp::LayerIfc>& aLayerIfc, const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    ~CmdAttachToLayerIfc() override = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
