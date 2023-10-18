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
class LX_OPENLXCMD_EXPORT CmdAddSkinLinearNURBS : public Core::Command
{
public:
    enum class ResultingShape
    {
        AUTO,
        OPEN,
        CLOSED
    };

    CmdAddSkinLinearNURBS();
    explicit CmdAddSkinLinearNURBS(const ResultingShape& aResultingShapeEnum);
    explicit CmdAddSkinLinearNURBS(std::vector<std::shared_ptr<OpenLxApp::Element>> aElements, const ResultingShape& aResultingShapeEnum = ResultingShape::AUTO);
    explicit CmdAddSkinLinearNURBS(std::vector<pConstShape> aElements, const ResultingShape& aResultingShapeEnum = ResultingShape::AUTO);
    virtual ~CmdAddSkinLinearNURBS() = default;

    bool redo() override;
    bool undo() override;

    std::shared_ptr<OpenLxApp::Element> getElement() const;

private:
    App::Document* _document = nullptr;
    App::Element* _newElement = nullptr;

    void execute(const std::vector<pConstShape> &shapes, const ResultingShape& aResultingShapeEnum);
};
}