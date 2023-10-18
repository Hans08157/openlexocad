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

#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Product.h>
#include <OpenLxApp/Root.h>


namespace Gui
{
class ViewProvider;
class ViewProviderElementInterface;
}  // namespace Gui

namespace OpenLxUI
{
class UIElementP;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT UIElement
#ifndef SWIG
    : public QObject
#endif

{
    Q_OBJECT

public:
    friend class UIDocument;

    std::shared_ptr<OpenLxApp::DocObject> getObject() const;
    std::shared_ptr<OpenLxApp::Root> getAsRoot() const;
    std::shared_ptr<OpenLxApp::Product> getAsProduct() const;
    std::shared_ptr<OpenLxApp::Element> getAsElement() const;

#ifndef SWIG

signals:

private slots:

#endif
public:
    bool isSelected() const;
    bool isDrawable() const;
    void setTmpVisible(bool onoff);
    bool isTmpVisible() const;
    // void setTmpSelected(bool on, bool singleselect = false);
    // void setTmpGreyscale(bool on);
    // void setTmpHiddenLine(bool on);
    // void setTmpTexturesGrey(bool onoff);
    void setHighlighted(bool onoff, int r, int g, int b);
    // void setHasDragger(bool on);
    // bool hasDragger();
    // void setTmpDrawStyle(const Draw::DrawStyle& ds);
    void setPickable(bool);
    bool isPickable();
    void setTmpBaseColor(int r, int g, int b);
    void removeTmpBaseColor();
    // int  getTmpTransparency() const;
    // void setTmpTransparency(int value);
    // void setLODEnabled(bool onoff);
    // void drawBoundingBox(bool onoff);
    void setTmpWireframe(bool on);
    bool hasTmpWireframe() const;
    Geom::Bnd_Box getBoundingBox();

    UIElement() = delete;

private:
    UIElement(Gui::ViewProvider* aVP);
    UIElement(std::shared_ptr<OpenLxApp::DocObject> aObj);
    std::shared_ptr<OpenLxUI::UIElementP> _pimpl;
};
}  // namespace OpenLxUI