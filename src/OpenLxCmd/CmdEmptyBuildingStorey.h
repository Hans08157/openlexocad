#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>


namespace OpenLxCmd
{
/**
 * @brief Remove Elements from the BuildingStorey of the active Building, whose elevation value corresponds to the given one.
 *        Optionally remove the Elements from the Document too.
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdEmptyStorey : public Core::Command
{
public:
    CmdEmptyStorey(const double& elevation, bool removeElements);
    ~CmdEmptyStorey();

    bool redo() override;
    bool undo() override;

private:
    Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd