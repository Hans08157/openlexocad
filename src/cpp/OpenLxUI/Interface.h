#pragma once

#include <Base/String.h>
#include <Core/Result.h>
#include <Gui/Action.h>
#include <OpenLxApp/Application.h>
#include <OpenLxApp/CartesianPoint.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/Globals.h>

#include <OpenLxUI/UIApplication.h>
#include <OpenLxUI/UIDocument.h>

#include <vector>

#ifndef SWIG
#include <QIcon>
#include <QWidget>
#endif


namespace OpenLxUI
{
/////////////////////////////////////////
/// General
/////////////////////////////////////////

LX_OPENLXUI_EXPORT long long getMainWidgetPtr();

#ifndef SWIG
LX_OPENLXUI_EXPORT QWidget* getMainWidget();
#endif

/////////////////////////////////////////
/// KEYBOARD
/////////////////////////////////////////

LX_OPENLXUI_EXPORT void enableKeyboardShortcuts(bool onoff);


/////////////////////////////////////////
/// ACTIONS AND WIDGETS
/////////////////////////////////////////

#ifndef SWIG
LX_OPENLXUI_EXPORT Gui::Action* addTemporaryAction(const QIcon& icon,
                                                const QString& text,
                                                const QObject* receiver,
                                                const char* member,
                                                const QKeySequence& shortcut = 0);
LX_OPENLXUI_EXPORT Gui::Action* addTemporaryAction(const QString& text, const QObject* receiver, const char* member, const QKeySequence& shortcut = 0);
LX_OPENLXUI_EXPORT Gui::Action* addActionToWidget(Gui::Action* action, QWidget* widget);

LX_OPENLXUI_EXPORT Gui::Action* addAction(const QString& name, const Gui::ActionBehavior& = Gui::ActionBehavior());
LX_OPENLXUI_EXPORT Gui::Action* addAction(const QString& name, QAction* action, const Gui::ActionBehavior& = Gui::ActionBehavior());
LX_OPENLXUI_EXPORT Gui::Action* addMenuAction(const QString& name, QMenu* menu, const Gui::ActionBehavior& = Gui::ActionBehavior());
LX_OPENLXUI_EXPORT void setDefaultMenuAction(QMenu* menu, Gui::Action* action);
LX_OPENLXUI_EXPORT Gui::Action* getActionByName(const QString& name);
LX_OPENLXUI_EXPORT QString getActionName(Gui::Action* action);
LX_OPENLXUI_EXPORT bool removeActionFromWidget(Gui::Action* action, QWidget* widget);
LX_OPENLXUI_EXPORT bool removeAllActionsFromWidget(QWidget* widget);
LX_OPENLXUI_EXPORT Gui::Action* insertActionToWidget(Gui::Action* action, QWidget* widget, Gui::Action* before);
LX_OPENLXUI_EXPORT Gui::Action* addActionToActionGroup(Gui::Action* action, Gui::ActionGroup* actionGroup);
LX_OPENLXUI_EXPORT Gui::Action* addTemporaryMenuAction(QMenu* menu);
LX_OPENLXUI_EXPORT Gui::ActionGroup* addActionGroup(QWidget* parent);
LX_OPENLXUI_EXPORT bool setShortcut(Gui::Action* action, const QKeySequence& shortcut);
LX_OPENLXUI_EXPORT void removeShortcut(const QKeySequence& shortcut);
LX_OPENLXUI_EXPORT const std::map<QString, Gui::Action*>& getActions();
LX_OPENLXUI_EXPORT const std::map<QString, Gui::Action*>& getActionsForFKeyAssignDialog();
LX_OPENLXUI_EXPORT Gui::Action* getActionByShortcut(const QKeySequence& shortcut);
LX_OPENLXUI_EXPORT bool removeAction(Gui::Action* action);
LX_OPENLXUI_EXPORT void removeAllActions();
LX_OPENLXUI_EXPORT bool removeTemporaryAction(Gui::Action* action);
LX_OPENLXUI_EXPORT void removeAllTemporaryActions();
LX_OPENLXUI_EXPORT const std::set<Gui::Action*>& getAllTemporaryActions();  //|Test|

#endif

/////////////////////////////////////////
/// VIEWER
/////////////////////////////////////////

LX_OPENLXUI_EXPORT void viewAll(int aViewerId, int aAnimationTime = 0);
LX_OPENLXUI_EXPORT void view(int aViewerId, OpenLxApp::View_Direction aViewDirection, int aAnimationTime = 0);
LX_OPENLXUI_EXPORT void lookAt(int aViewerId, const Geom::Pnt& aFromPnt, const Geom::Pnt& aToPnt, const Geom::Vec& aUpVector);
LX_OPENLXUI_EXPORT void viewOrthogonal(int aViewerId);
LX_OPENLXUI_EXPORT void viewPerspective(int aViewerId);

/////////////////////////////////////////
/// DIALOGS AND MESSAGE
/////////////////////////////////////////

LX_OPENLXUI_EXPORT int showMessageBox(const Base::String& title, const Base::String& message, int icon = 1);
LX_OPENLXUI_EXPORT bool showMessageBoxQuestionYesNo(const Base::String& title, const Base::String& text, int defaultChoice = 1);
LX_OPENLXUI_EXPORT void showStatusBarMessage(const Base::String& msg);
LX_OPENLXUI_EXPORT void showStatusBarMessage(int aMsgNumber);
LX_OPENLXUI_EXPORT void resetStatusBarMessage();
LX_OPENLXUI_EXPORT Core::DoubleResult getDoubleDialog(const Base::String& label,
                                                   const double& initialValue = 0,
                                                   const int& decimals = 1,
                                                   const double& minValue = -DBL_MAX,
                                                   const double& maxValue = DBL_MAX);
LX_OPENLXUI_EXPORT Core::IntegerResult getIntDialog(const Base::String& label,
                                                 const int& initialValue = 0,
                                                 const int& step = 1,
                                                 const int& minValue = -INT_MAX,
                                                 const int& maxValue = INT_MAX);
LX_OPENLXUI_EXPORT Core::StringResult getTextDialog(const Base::String& label, const Base::String& initialValue = L"", const int& mode = 0);
LX_OPENLXUI_EXPORT Core::StringResult getItemDialog(const Base::String& label,
                                                 std::vector<Base::String>& initialValues,
                                                 const int& current = 0,
                                                 const bool& editable = false);

}  // namespace OpenLxUI