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
class LX_OPENLXCMD_EXPORT CmdCopyAlongCurve : public Core::Command
{
public:
    CmdCopyAlongCurve();

    CmdCopyAlongCurve(std::shared_ptr<OpenLxApp::Element> aElem,
                      std::shared_ptr<OpenLxApp::Element> aPathElem,
                      bool fromEnd,
                      int number,
                      bool useRepetitions,
                      bool blockRotationX,
                      bool blockRotationY,
                      bool blockRotationZ);
    CmdCopyAlongCurve(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems,
                      std::shared_ptr<OpenLxApp::Element> aPathElem,
                      bool fromEnd,
                      int number,
                      bool useRepetitions,
                      bool blockRotationX,
                      bool blockRotationY,
                      bool blockRotationZ);

    CmdCopyAlongCurve(std::shared_ptr<OpenLxApp::Element> aElem,
                      std::shared_ptr<OpenLxApp::Element> aPathElem,
                      bool fromEnd,
                      double distance,
                      bool useRepetitions,
                      bool blockRotationX,
                      bool blockRotationY,
                      bool blockRotationZ);
    CmdCopyAlongCurve(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems,
                      std::shared_ptr<OpenLxApp::Element> aPathElem,
                      bool fromEnd,
                      double distance,
                      bool useRepetitions,
                      bool blockRotationX,
                      bool blockRotationY,
                      bool blockRotationZ);

    ~CmdCopyAlongCurve() = default;

    bool redo() override;
    bool undo() override;

    std::vector<std::shared_ptr<OpenLxApp::Element>> getCopiedElements() const;

private:
    std::unique_ptr<Core::Command> _cmd = nullptr;
};
}  // namespace OpenLxCmd
