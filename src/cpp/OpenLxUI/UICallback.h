#pragma once

#include <Base/GlobalId.h>


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
class LX_OPENLXUI_EXPORT UICallback
{
public:
    void setActive(bool onoff);
    bool isActive() const;

    virtual ~UICallback() {}

private:
    bool _active = true;
};
}  // namespace OpenLxUI