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
 * @brief	Cuts one or more Element into the given Element
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdBooleanCut : public Core::Command
{
public:
    CmdBooleanCut(const std::vector<std::shared_ptr<OpenLxApp::Element>>& hardElements, std::shared_ptr<OpenLxApp::Element> softElement);
    CmdBooleanCut(std::shared_ptr<OpenLxApp::Element> hardElement, std::shared_ptr<OpenLxApp::Element> softElement);
    ~CmdBooleanCut();

    bool redo() override;
    bool undo() override;

    std::vector<std::shared_ptr<OpenLxApp::Element>> getElements() const;

private:
    Command* _cmd = nullptr;
    std::vector<std::shared_ptr<OpenLxApp::Element>> _resultElements = {};
};
}  // namespace OpenLxCmd
