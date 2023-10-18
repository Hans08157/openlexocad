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
class LX_OPENLXUI_EXPORT SelectionCB : public OpenLxUI::UICallback
{
public:
    SelectionCB();
    virtual ~SelectionCB();

    virtual void test();
    // Is calling back when one or more UIElement get selected.
    virtual void onSelected(const std::vector<std::shared_ptr<OpenLxUI::UIElement>>&);
    // Is calling back when one or more UIElement get deselected.
    virtual void onDeselected(const std::vector<std::shared_ptr<OpenLxUI::UIElement>>&);
    // Is calling back when the selection is cleared.
    virtual void onClearedSelection();

private:
};
}  // namespace OpenLxUI