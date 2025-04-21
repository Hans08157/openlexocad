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
class LX_OPENLXCMD_EXPORT CmdAddCanalizationAssembly : public Core::Command
{
public:
    CmdAddCanalizationAssembly();
    ~CmdAddCanalizationAssembly() override = default;

    std::shared_ptr<OpenLxApp::Element> getElement() const;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
