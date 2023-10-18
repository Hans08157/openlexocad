#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

#include <vector>

namespace OpenLxCmd
{
/**
 * @brief Interface to set the color of an Element without losing the data connected to the related Component (e.g. PropertySets)
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdSetComponentColor : public Core::Command
{
public:
    CmdSetComponentColor() = default;
    CmdSetComponentColor(std::shared_ptr<OpenLxApp::Element>& aElem, const Base::Color& color);
    CmdSetComponentColor(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems, const Base::Color& color);
    ~CmdSetComponentColor() = default;

    bool redo() override;
    bool undo() override;

private:
    void setComponentColor(std::shared_ptr<OpenLxApp::Element> aElem, const Base::Color& color);

    std::map<App::Element*, Draw::OglMaterial> _oldColors;
    std::map<App::Element*, Draw::OglMaterial> _newColors;
};
}
