#pragma once

#include <OpenLxApp/DocObject.h>
#include <OpenLxApp/Globals.h>

/** @defgroup OPENLX_PROFILEDEF Profile Definitions
 */

namespace Part
{
class ProfileDef;
}

namespace OpenLxApp
{
/*!
 * @brief ProfileDef is the supertype of all definitions of standard
 * and arbitrary profiles. It is used to define a standard set of commonly
 * used section profiles by their parameters or by their explicit curve geometry.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT ProfileDef : public DocObject
{
    PROXY_HEADER_ABSTRACT(ProfileDef, Part::ProfileDef, IFCPROFILEDEF)

    DECL_PROPERTY(ProfileDef, ProfileName, Base::String)
public:
    virtual ~ProfileDef(void);

protected:
    ProfileDef(void) {}
};
}  // namespace OpenLxApp