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
#include <Base/String.h>
#include <Core/Command.h>
#include <OpenLxApp/Element.h>


#include <memory>
#include <vector>

namespace OpenLxCmd
{
/**
 * @brief
 *
 * @ingroup  OPENLX_CMD
 * @since    24.0
 */
class LX_OPENLXCMD_EXPORT CmdExportLXZFile : public Core::Command
{
public:
    CmdExportLXZFile();
    CmdExportLXZFile(bool visibleonly, bool resetPlacement = false);
    CmdExportLXZFile(const Base::String& aPath, bool visibleonly = false, bool resetPlacement = false);
    ~CmdExportLXZFile();

    bool redo();
    bool undo();

private:
    Core::Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd