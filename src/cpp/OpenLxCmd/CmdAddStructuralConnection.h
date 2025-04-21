#pragma once

#include <Core/Command.h>
#include <OpenLxApp/Element.h>

namespace OpenLxCmd
{
/**
 * @brief Interface(s) to the command "CmdAddStructuralPointConnection"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStructuralPointConnection : public Core::Command
{
public:
    CmdAddStructuralPointConnection();
    explicit CmdAddStructuralPointConnection(const Geom::Pnt &pnt);
    ~CmdAddStructuralPointConnection() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};

/**
 * @brief Interface(s) to the command "CmdAddStructuralCurveConnection"
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStructuralCurveConnection : public Core::Command
{
public:
    CmdAddStructuralCurveConnection();
    explicit CmdAddStructuralCurveConnection(const Geom::Pnt &pnt1);
    CmdAddStructuralCurveConnection(const Geom::Pnt &pnt1, const Geom::Pnt &pnt2);
    ~CmdAddStructuralCurveConnection() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<Core::Command> _cmd;
};
}
