#pragma once

#include <OpenLxApp/Element.h>

#include <OpenLxUI/SelectionCB.h>
#include <OpenLxUI/UIElement.h>
#include <OpenLxUI/UIElementFilter.h>

#include <QObject>


namespace OpenLxUI
{
class SelectionP;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT Selection

#ifndef SWIG
    : public QObject
#endif

{
    Q_OBJECT

public:
    std::shared_ptr<OpenLxApp::Document> getDocument() const;

    void selectAll() const;
    void select(std::shared_ptr<OpenLxApp::Element> aElem) const;
    void select(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems) const;
    void deselectAll() const;
    void deselect(std::shared_ptr<OpenLxApp::Element> aElem) const;
    void deselect(const std::vector<std::shared_ptr<OpenLxApp::Element>>& aElems) const;
    void forceUpdate() const;

    std::vector<std::shared_ptr<OpenLxApp::DocObject>> getDocObjects() const;
    std::vector<std::shared_ptr<OpenLxApp::Element>> getAsElements() const;
    std::vector<std::shared_ptr<OpenLxUI::UIElement>> getUIElements() const;


#ifndef SWIG

signals:
    // Is emitted when one or more UIElements get selected.
    void selectedSignal(const std::vector<std::shared_ptr<OpenLxUI::UIElement>>&);
    // Is emitted when one or more UIElements get deselected.
    void deselectedSignal(const std::vector<std::shared_ptr<OpenLxUI::UIElement>>&);
    // Is emitted when the selection is cleared.
    void clearedSelectionSignal();

private slots:
    void _onSelected(const std::vector<Core::DocObject*>&);
    void _onDeselected(const std::vector<Core::DocObject*>&);
    void _onClearedSelection();
#endif
public:
    void addCallback(OpenLxUI::SelectionCB* aCB);
    void addCallback(OpenLxUI::SelectionCB* aCB, OpenLxUI::UIElementFilter* aFilter);
    void removeCallback(OpenLxUI::SelectionCB* aCB);
    void removeCallbacks();
    std::vector<OpenLxUI::SelectionCB*> getCallbacks() const;
    std::vector<OpenLxUI::SelectionCB*> getCallbacks(OpenLxUI::UIElementFilter* aFilter) const;

    // Testing
    void testCB();

    Selection(std::shared_ptr<OpenLxApp::Document> aDoc);

    ~Selection();
    Selection() = delete;

private:
    std::shared_ptr<OpenLxUI::SelectionP> _pimpl;
};
}  // namespace OpenLxUI