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
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddFormwork : public Core::Command
{
public:
    CmdAddFormwork();
    ~CmdAddFormwork() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}