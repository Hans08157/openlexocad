#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddSkinGuidesNURBS : public Core::Command
{
public:
    enum class ResultingShape
    {
        AUTO,
        OPEN,
        CLOSED
    };

    CmdAddSkinGuidesNURBS();
    explicit CmdAddSkinGuidesNURBS(const ResultingShape &aResultingShapeEnum);
    CmdAddSkinGuidesNURBS(std::vector<std::shared_ptr<OpenLxApp::Element>> aElements, std::vector<std::shared_ptr<OpenLxApp::Element>> aGuideElements, const ResultingShape &aResultingShapeEnum = ResultingShape::AUTO);
    CmdAddSkinGuidesNURBS(std::vector<pConstShape> aShapes, std::vector<pConstShape> aGuideShapes, const ResultingShape& aResultingShapeEnum = ResultingShape::AUTO);
    virtual ~CmdAddSkinGuidesNURBS() = default;

    bool redo() override;
    bool undo() override;

    std::shared_ptr<OpenLxApp::Element> getElement() const;

private:
    App::Document* _document = nullptr;
    App::Element* _newElement = nullptr;

    void execute(const std::vector<pConstShape> &shapes, const std::vector<pConstShape> &guideShapes, const ResultingShape& aResultingShapeEnum);
};
}