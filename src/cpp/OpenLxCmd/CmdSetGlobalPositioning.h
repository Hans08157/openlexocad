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
 * @brief	This Command creates/updates the "Global Positioning" structures introduced with IFC4. The "projection" data are obtained through an
 * internet connection to the site http://epsg.io in json format.
 *
 * @ingroup  OPENLX_CMD
 * @since    26.0
 */
class LX_OPENLXCMD_EXPORT CmdSetGlobalPositioning : public Core::Command
{
public:
    CmdSetGlobalPositioning(std::shared_ptr<OpenLxApp::Document> document,
                            const Base::String& epsgCode,
                            double eastings,
                            double northings,
                            double orthogonalHeight);
    ~CmdSetGlobalPositioning();

    bool redo() override;
    bool undo() override;

private:
    Command* _cmd = nullptr;
};
}  // namespace OpenLxCmd
