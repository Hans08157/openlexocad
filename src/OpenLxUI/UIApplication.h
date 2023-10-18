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

#include <OpenLxUI/UIApplicationCB.h>
#include <OpenLxUI/UIDocument.h>
#include <OpenLxUI/UIElement.h>
#include <OpenLxUI/UIElementFilter.h>

#include <QObject>

/** @defgroup OPENLX_UI User Interface (UI)
 */


namespace OpenLxUI
{
class UIApplicationP;
class UIApplicationCB;
class Viewer;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT UIApplication

#ifndef SWIG
    : public QObject
#endif

{
    Q_OBJECT

public:
    OpenLxApp::Application* getApplication() const;
    std::shared_ptr<OpenLxUI::UIDocument> getUIDocument(std::shared_ptr<OpenLxApp::Document> aDoc) const;

    static UIApplication* getInstance();

#ifndef SWIG
signals:
    // This signal is emitted when the UIProperties in the Modify Panel are about to be displayed.
    void displayUIPropertiesSignal(Gui::PropertyTree*, std::shared_ptr<OpenLxUI::UIElement>);
    // This signal is emitted when a UIProperty has been changed by the user.
    void changedUIPropertySignal(Gui::PropertyTreeItem*, std::shared_ptr<OpenLxUI::UIElement>);

private slots:

    void _onLexocadDisplayUIProperties(Gui::PropertyTree*, Core::DocObject*);
    void _onLexocadChangedUIProperty(Gui::PropertyTreeItem*, Core::DocObject*);

public:
    void installCustomEventFilter(QObject* aFilterObj);
    void removeCustomEventFilter(QObject* aFilterObj);


#endif
public:
    ~UIApplication();

public:
    void processEvents();

    void addCallback(OpenLxUI::UIApplicationCB* aCB);
    void addCallback(OpenLxUI::UIApplicationCB* aCB, OpenLxUI::UIElementFilter* aFilter);
    void removeCallback(OpenLxUI::UIApplicationCB* aCB);
    void removeCallbacks();

    std::shared_ptr<OpenLxUI::Viewer> getActiveViewer() const;
    std::vector<std::shared_ptr<OpenLxUI::Viewer>> getViewer() const;

    // Testing
    void testCB();
    void onLexocadChangedUIProperty(Gui::PropertyTreeItem*, std::shared_ptr<OpenLxUI::UIElement>);

    UIApplication() = delete;

private:
    UIApplication(OpenLxApp::Application* theApp);
    static UIApplication* instance;
    std::shared_ptr<UIApplicationP> _pimpl;
};

}  // namespace OpenLxUI