#pragma once

#include <OpenLxApp/Property.h>
#include <OpenLxApp/Root.h>

#include <memory>
#include <vector>

FORWARD_DECL(App, PropertySet)



namespace OpenLxApp
{
/**
 * @brief: The PropertySet defines all dynamically extensible properties.
 * These properties are interpreted according to their name attribute.
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT PropertySet : public Root
{
    PROXY_HEADER(PropertySet, App::PropertySet, IFCPROPERTYSET)

public:
    virtual ~PropertySet();

    std::vector<std::shared_ptr<OpenLxApp::Property>> getHasProperties() const;
    std::vector<std::shared_ptr<OpenLxApp::PropertyEnum>> getPropertyEnums() const;

protected:
};

}  // namespace OpenLxApp