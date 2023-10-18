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

namespace Base
{
    enum class SplitStatus;
}

namespace OpenLxCmd
{
/**
 * @brief	Python interface for command Gui::CmdBooleanSplitShapeWithPlane
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdBooleanSplitShapeWithPlane : public Core::Command
{
public:
    CmdBooleanSplitShapeWithPlane(std::shared_ptr<OpenLxApp::Element> softElement, Geom::Pnt point1, Geom::Pnt point2);
    CmdBooleanSplitShapeWithPlane(std::shared_ptr<OpenLxApp::Element> softElement, std::shared_ptr<OpenLxApp::Element> hardElement, Base::SplitStatus status);
    ~CmdBooleanSplitShapeWithPlane() override;

    bool redo() override;
    bool undo() override;

    std::vector<std::shared_ptr<OpenLxApp::Element>> getElements() const;

private:
    Command* _cmd = nullptr;
    std::vector<std::shared_ptr<OpenLxApp::Element>> _resultElements = {};
};
}  // namespace OpenLxCmd
