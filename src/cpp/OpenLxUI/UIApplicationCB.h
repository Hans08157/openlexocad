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

#include <Gui/PropertyTree.h>
#include <OpenLxApp/Application.h>
#include <OpenLxApp/Document.h>

#include <OpenLxUI/UICallback.h>
#include <OpenLxUI/UIDocument.h>

#include <QObject>

namespace OpenLxUI
{
/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT UIApplicationCB : public OpenLxUI::UICallback
{
public:
    UIApplicationCB();
    virtual ~UIApplicationCB();

    virtual void test();
    virtual void onLexocadDisplayUIProperties(Gui::PropertyTree*, std::shared_ptr<OpenLxUI::UIElement>);
    virtual void onLexocadChangedUIProperty(Gui::PropertyTreeItem*, std::shared_ptr<OpenLxUI::UIElement>);

    virtual void onFileOpened();

private:
};
}  // namespace OpenLxUI