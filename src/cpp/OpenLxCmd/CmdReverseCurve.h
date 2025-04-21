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
class LX_OPENLXCMD_EXPORT CmdReverseCurve : public Core::Command
{
public:
    CmdReverseCurve();
    explicit CmdReverseCurve(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    ~CmdReverseCurve() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
