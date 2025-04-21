#pragma once
#include <Core/Command.h>

#include <memory>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddBeamStandardCaseAxis : public Core::Command
{
public:
    CmdAddBeamStandardCaseAxis();
    ~CmdAddBeamStandardCaseAxis() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};

/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddColumnStandardCaseAxis : public Core::Command
{
public:
    CmdAddColumnStandardCaseAxis();
    ~CmdAddColumnStandardCaseAxis() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};

/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddMemberStandardCaseAxis : public Core::Command
{
public:
    CmdAddMemberStandardCaseAxis();
    ~CmdAddMemberStandardCaseAxis() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
