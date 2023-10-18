#pragma once
#include <OpenLxApp/Property.h>


namespace Core
{
class PropertyScriptParam;
}


namespace OpenLxApp
{
/**
 * @brief PropertyFactory to create Properties
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT PropertyFactory
{
public:
    static std::shared_ptr<Property> create(Core::PropertyScriptParam* aProp);
};



}  // namespace OpenLxApp