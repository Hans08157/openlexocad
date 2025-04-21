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
class LX_OPENLXCMD_EXPORT CmdAddCentroid : public Core::Command
{
public:
    CmdAddCentroid();
    explicit CmdAddCentroid(std::shared_ptr<OpenLxApp::Element> curveElement);
    explicit CmdAddCentroid(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    ~CmdAddCentroid() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
