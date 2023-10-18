#pragma once

#include <OpenLxApp/ProfileDef.h>
#include <OpenLxApp/Globals.h>


namespace Part {
class ParameterizedProfileDef;
}

namespace OpenLxApp
{
/*!
 * @brief The parameterized profile definition defines a 2D position coordinate system to which
 * the parameters of the different profiles relate to. All profiles are defined centric to the
 * origin of the position coordinate system, or more specific, the origin [0.,0.] shall be in the
 * center of the bounding box of the profile.
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcparameterizedprofiledef.htm" target="_blank">Documentation from IFC4:
 * IfcParameterizedProfileDef</a>
 * @ingroup OPENLX_PROFILEDEF
 */

class LX_OPENLXAPP_EXPORT ParameterizedProfileDef : public ProfileDef
{
    PROXY_HEADER_ABSTRACT(ParameterizedProfileDef, Part::ParameterizedProfileDef, IFCPARAMETERIZEDPROFILEDEF)

    DECL_PROPERTY(ParameterizedProfileDef, Position, Geom::Ax22d)

public:
    virtual ~ParameterizedProfileDef(void);

protected:
    ParameterizedProfileDef(void) {}
};
}  // namespace OpenLxApp