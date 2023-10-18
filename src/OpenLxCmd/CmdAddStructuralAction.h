#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
class LX_OPENLXCMD_EXPORT CmdAddStructuralAction : public Core::Command
{
public:
    CmdAddStructuralAction() = default;
    explicit CmdAddStructuralAction(Core::Command *command);
    ~CmdAddStructuralAction() = default;

    bool redo() override;
    bool undo() override;

    std::shared_ptr<OpenLxApp::Element> getNewElement() const;

protected:
    std::unique_ptr<Core::Command> _cmd;
};

/**
 * @brief Interface(s) to the command "CmdAddStructuralCurveAction"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStructuralCurveAction : public OpenLxCmd::CmdAddStructuralAction
{
public:
    CmdAddStructuralCurveAction();
    explicit CmdAddStructuralCurveAction(std::shared_ptr<OpenLxApp::Element> relatingElement);
    CmdAddStructuralCurveAction(std::shared_ptr<OpenLxApp::Element> relatingElement, const std::vector<Geom::Pnt>& pickedPoints);
    ~CmdAddStructuralCurveAction() = default;
};

/**
 * @brief Interface(s) to the command "CmdAddStructuralPlanarAction"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStructuralPlanarAction : public OpenLxCmd::CmdAddStructuralAction
{
public:
    CmdAddStructuralPlanarAction();
    explicit CmdAddStructuralPlanarAction(std::shared_ptr<OpenLxApp::Element> relatingElement);
    CmdAddStructuralPlanarAction(std::shared_ptr<OpenLxApp::Element> relatingElement, const std::vector<Geom::Pnt>& pickedPoints);
    ~CmdAddStructuralPlanarAction() = default;
};

/**
 * @brief Interface(s) to the command "CmdAddStructuralPointAction"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStructuralPointAction : public OpenLxCmd::CmdAddStructuralAction
{
public:
    CmdAddStructuralPointAction();
    explicit CmdAddStructuralPointAction(std::shared_ptr<OpenLxApp::Element> relatingElement);
    CmdAddStructuralPointAction(std::shared_ptr<OpenLxApp::Element> relatingElement, const Geom::Pnt &pickedPoint);
    ~CmdAddStructuralPointAction() = default;
};
}
