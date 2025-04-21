#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
/**
 * @brief Creates a "generic" command given its name (if it exists)
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdCreateGenericCommand : public Core::Command
{
public:
    CmdCreateGenericCommand() = default;
    explicit CmdCreateGenericCommand(const std::string &commandName);
    ~CmdCreateGenericCommand() = default;

    bool created() const;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
