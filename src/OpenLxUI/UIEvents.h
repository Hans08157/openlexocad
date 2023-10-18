#pragma once

#include <Gui/PropertyTree.h>

#include <OpenLxUI/UIElement.h>

#include <QEvent>

static const QEvent::Type DisplayUIPropertiesEventType = QEvent::Type(QEvent::User + 1000);
static const QEvent::Type ChangedUIPropertyEventType = QEvent::Type(QEvent::User + 1001);

namespace OpenLxUI
{
/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT DisplayUIPropertiesEvent : public QEvent
{
public:
    DisplayUIPropertiesEvent(Gui::PropertyTree* aTree, std::shared_ptr<OpenLxUI::UIElement> aUIElem)
        : QEvent(DisplayUIPropertiesEventType), tree(aTree), uiElem(aUIElem)
    {
    }

    Gui::PropertyTree* tree = nullptr;
    std::shared_ptr<OpenLxUI::UIElement> uiElem;
};

class LX_OPENLXUI_EXPORT ChangedUIPropertyEvent : public QEvent
{
public:
    ChangedUIPropertyEvent(Gui::PropertyTreeItem* aItem, std::shared_ptr<OpenLxUI::UIElement> aUIElem)
        : QEvent(ChangedUIPropertyEventType), item(aItem), uiElem(aUIElem)
    {
    }

    Gui::PropertyTreeItem* item = nullptr;
    std::shared_ptr<OpenLxUI::UIElement> uiElem;
};

}  // namespace OpenLxUI