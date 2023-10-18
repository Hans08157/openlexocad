#pragma once


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
class LX_OPENLXUI_EXPORT UIElementFilter
{
public:
    // Can be overridden to create a custom filter behavior.
    virtual bool filterUIElement(const std::vector<std::shared_ptr<OpenLxUI::UIElement>>&) const;

    virtual ~UIElementFilter() {}
};
}  // namespace OpenLxUI