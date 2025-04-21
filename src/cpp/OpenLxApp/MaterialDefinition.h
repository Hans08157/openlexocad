#pragma once

#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Globals.h>

/** @defgroup OPENLX_MATERIAL Material
 */

namespace App
{
class MaterialDefinition;
}

namespace OpenLxApp
{
//class Document;


/**
 * @brief Super-class of all Materials
 *
 * @ingroup OPENLX_MATERIAL
 */

class LX_OPENLXAPP_EXPORT MaterialDefinition : public DocObject
{
    PROXY_HEADER_ABSTRACT(MaterialDefinition, App::MaterialDefinition, IFCMATERIALDEFINITION)

public:
    virtual ~MaterialDefinition(void);

protected:
    MaterialDefinition() {}
};

}  // namespace OpenLxApp
