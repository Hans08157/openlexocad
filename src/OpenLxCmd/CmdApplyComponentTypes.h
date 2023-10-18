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
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdApplyComponentTypes : public Core::Command
{
public:
    CmdApplyComponentTypes() = default;
    CmdApplyComponentTypes(std::shared_ptr<OpenLxApp::Element>& aElem);
    CmdApplyComponentTypes(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    ~CmdApplyComponentTypes() = default;

    bool redo() override;
    bool undo() override;
};
}  // namespace OpenLxCmd