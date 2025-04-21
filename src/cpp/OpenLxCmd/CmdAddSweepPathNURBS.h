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
class LX_OPENLXCMD_EXPORT CmdAddSweepPathNURBS : public Core::Command
{
public:
    enum class ResultingShape
    {
        AUTO,
        OPEN,
        CLOSED
    };

    CmdAddSweepPathNURBS();
    explicit CmdAddSweepPathNURBS(const ResultingShape& aResultingShapeEnum);
    CmdAddSweepPathNURBS(std::shared_ptr<OpenLxApp::Element> aProfileElement, std::shared_ptr<OpenLxApp::Element> aPathElement, const ResultingShape& aResultingShapeEnum = ResultingShape::AUTO);
    CmdAddSweepPathNURBS(pConstShape aProfileShape, pConstShape aPathShape, const ResultingShape& aResultingShapeEnum = ResultingShape::AUTO);
    virtual ~CmdAddSweepPathNURBS() = default;

    bool redo() override;
    bool undo() override;

    std::shared_ptr<OpenLxApp::Element> getElement() const;

private:
    App::Document* _document = nullptr;
    App::Element* _newElement = nullptr;

    void execute(pConstShape profileShape, pConstShape pathShape, const ResultingShape& aResultingShapeEnum);
};
}
