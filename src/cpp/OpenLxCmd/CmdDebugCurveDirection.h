#pragma once
#include <Core/Command.h>
#include <OpenLxApp/Element.h>

#include <memory>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdDebugCurveDirection : public Core::Command
{
public:
    CmdDebugCurveDirection();
    CmdDebugCurveDirection(std::shared_ptr<OpenLxApp::Element> aPathElem, size_t repetitions);
    ~CmdDebugCurveDirection() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
