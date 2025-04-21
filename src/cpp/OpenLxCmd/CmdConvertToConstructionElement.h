#pragma once
#include <Core/Command.h>
#include <OpenLxApp/Element.h>

#include <memory>
#include <vector>

namespace OpenLxCmd
{
/**
 * @brief   Python interface for "ElementExtensions::CmdConvertToConstructionElement"
 *
 * @ingroup OPENLX_CMD
 * @since   28.0
 */
class LX_OPENLXCMD_EXPORT CmdConvertToConstructionElement : public Core::Command
{
public:
    CmdConvertToConstructionElement();
    explicit CmdConvertToConstructionElement(std::shared_ptr<OpenLxApp::Element> aElement);
    explicit CmdConvertToConstructionElement(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    ~CmdConvertToConstructionElement() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
