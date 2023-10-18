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


namespace OpenLxCmd
{
/**
 * @brief	Convert the geometry of the given Element into a FacetedBrep
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdConvertToFacetedBrep : public Core::Command
{
public:
    explicit CmdConvertToFacetedBrep(std::shared_ptr<OpenLxApp::Element> element);
    explicit CmdConvertToFacetedBrep(const std::vector<std::shared_ptr<OpenLxApp::Element>>& elements);
    ~CmdConvertToFacetedBrep();

    bool redo() override;
    bool undo() override;

    std::vector<std::shared_ptr<OpenLxApp::Element>> getElements() const;

private:
    Command* _cmd = nullptr;
    std::vector<std::shared_ptr<OpenLxApp::Element>> _resultElements = {};
};

/**
 * @brief	Convert the given Element into a ElementExtension::BeamElement
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdConvertToBeamElement : public Core::Command
{
public:
    explicit CmdConvertToBeamElement(std::shared_ptr<OpenLxApp::Element> element);

    bool redo() override;
    bool undo() override;

private:
    Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd