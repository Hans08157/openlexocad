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
class LX_OPENLXCMD_EXPORT CmdAddIsoParamLines : public Core::Command
{
public:
    CmdAddIsoParamLines();
    CmdAddIsoParamLines(std::shared_ptr<OpenLxApp::Element> aElem);
    CmdAddIsoParamLines(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems);
    CmdAddIsoParamLines(std::shared_ptr<OpenLxApp::Element> aElem, size_t u, size_t v);
    CmdAddIsoParamLines(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems, size_t u, size_t v);
    ~CmdAddIsoParamLines();
    bool redo();
    bool undo();

    std::vector<std::shared_ptr<OpenLxApp::Element>> getIsoParamLineElements() const;

private:
    Core::Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd