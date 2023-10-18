///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// �2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once
#include <Core/Command.h>
#include <OpenLxApp/Element.h>


namespace OpenLxCmd
{
/**
 * @brief	Attach a Task (provided its identifier) to the given Element. If the Command fails, check the log for more information.
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdAttachToTask : public Core::Command
{
public:
    CmdAttachToTask(const Base::String& taskId, std::shared_ptr<OpenLxApp::Element> element);
    ~CmdAttachToTask();

    bool redo() override;
    bool undo() override;

private:
    Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd
