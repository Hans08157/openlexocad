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


#include <OpenLxUI/UICallback.h>
#include <OpenLxUI/UIElement.h>

#include <memory>
#include <vector>


namespace OpenLxUI
{
/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT DragAndDropCB : public OpenLxUI::UICallback
{
public:
    DragAndDropCB();
    virtual ~DragAndDropCB();

    // TODO: Is calling back a registered file is dropped in the viewer.
    virtual void onDrop();

private:
};
}  // namespace OpenLxUI