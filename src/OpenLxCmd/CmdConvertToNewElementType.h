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
class LX_OPENLXCMD_EXPORT CmdConvertToNewElementType : public Core::Command
{
public:
    CmdConvertToNewElementType();
    CmdConvertToNewElementType(std::shared_ptr<OpenLxApp::Element> aElem, int userType);
    CmdConvertToNewElementType(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems, int userType);
    ~CmdConvertToNewElementType() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
