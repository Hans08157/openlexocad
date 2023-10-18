#pragma once

#include <Core/Command.h>
#include <Gui/CA_Command_5.h>

#include <memory>

namespace OpenLxCmd
{
/**
 * @brief Python interface for adding a Building.
 *  The function internally calls the appropriate Lexocad command, which in turn also creates a Storey.
 *  It is possible to specify a name for the Building, one for the Storey and the elevation for the Storey.
 *  The Building is set as active and the Storey is also set as active.
 *  New Elements will be created in the active Storey.
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddBuilding : public Core::Command
{
public:
    CmdAddBuilding();
    explicit CmdAddBuilding(std::string buildingName);
    CmdAddBuilding(std::string buildingName, std::string storeyName);
    CmdAddBuilding(std::string buildingName, std::string storeyName, double elevation);
    ~CmdAddBuilding() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<CmdCreateBuilding> _cmd;

    std::string _buildingName = {};
    std::string _storeyName = {};
    double _elevation = 0.;

    App::Building* _activeBuilding = nullptr;
    App::BuildingStorey* _activeStorey = nullptr;
};

/**
 * @brief Python interface for adding a Storey inside the active Building.
 *  The function internally calls the appropriate Lexocad command.
 *  It is possible to specify a name for the Storey and the elevation for the Storey.
 *  The Storey is set as active.
 *  New Elements will be created in the active Storey.
 *  The function fails if the given elevation is already used inside the same Building.
 *
 * @ingroup  OPENLX_CMD
 * @since    28.0
 */
class LX_OPENLXCMD_EXPORT CmdAddStorey : public Core::Command
{
public:
    CmdAddStorey();
    explicit CmdAddStorey(std::string storeyName);
    CmdAddStorey(std::string storeyName, double z);
    ~CmdAddStorey() = default;

    bool redo() override;
    bool undo() override;

private:
    std::unique_ptr<CmdCreateBuildingStorey> _cmd;

    App::BuildingStorey* _activeStorey = nullptr;
};
}
