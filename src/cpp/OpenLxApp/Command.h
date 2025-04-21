#pragma once

namespace Core
{
class Command;
}

namespace OpenLxApp
{
/**
 * @brief Command is the base class of all commands.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT Command
{
public:
    Command(void);
    virtual ~Command(void);

    virtual bool redo() { return true; }
    virtual bool undo() { return true; }

    // For internal use
    Core::Command* __getCmd__() const;

protected:
    Core::Command* _cmd;
};

}  // namespace OpenLxApp