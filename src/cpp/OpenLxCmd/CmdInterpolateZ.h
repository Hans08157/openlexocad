#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
/**
 * @brief   Python interface for "PartCommands::CmdInterpolateZ"
 *
 * @ingroup OPENLX_CMD
 * @since   28.0
 */
class LX_OPENLXCMD_EXPORT CmdInterpolateZ : public Core::Command
{
public:
    CmdInterpolateZ();
    explicit CmdInterpolateZ(std::shared_ptr<OpenLxApp::Element> aElem);               // Interpolate ALL Points
    CmdInterpolateZ(std::shared_ptr<OpenLxApp::Element> aElem, const Geom::Pnt &pnt);

    ~CmdInterpolateZ() override = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd = nullptr;
};
}
