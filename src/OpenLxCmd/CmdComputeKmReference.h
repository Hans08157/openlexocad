#pragma once
#include <Core/Command.h>
#include <OpenLxApp/Element.h>

#include <memory>
#include <vector>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdComputeKmReference : public Core::Command
{
public:
    CmdComputeKmReference();
    explicit CmdComputeKmReference(double km);
    explicit CmdComputeKmReference(std::shared_ptr<OpenLxApp::Element> curveElement, double km = 0);
    CmdComputeKmReference(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems, std::shared_ptr<OpenLxApp::Element> curveElement, double km = 0);
    ~CmdComputeKmReference() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
