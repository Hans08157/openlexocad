///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
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
#include <OpenLxApp/SubElement.h>


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
class LX_OPENLXCMD_EXPORT CmdExtrudeSubElementFace : public Core::Command
{
public:
    CmdExtrudeSubElementFace();
    CmdExtrudeSubElementFace(std::shared_ptr<OpenLxApp::SubElement> aSubElem, int aFaceindex, const Geom::Dir& aNormal, double aLength);
    ~CmdExtrudeSubElementFace();

    bool redo();
    bool undo();

    std::shared_ptr<OpenLxApp::SubElement> getExtrudedSubElement() const;

private:
    Core::Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd