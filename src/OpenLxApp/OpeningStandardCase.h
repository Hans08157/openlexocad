#pragma once
#include <OpenLxApp/OpeningElement.h>

#include <memory>

FORWARD_DECL(App, OpeningElement)

namespace OpenLxApp
{
/*!
 * @brief The standard opening, OpeningStandardCase, defines an opening with certain constraints
 * for the dimension parameters, position within the voided element, and with certain constraints for
 * the geometric representation. The OpeningStandardCase handles all cases of openings, that:
 *  - are true openings by cutting through the body of the voided element, that is,
 *    where the opening depth is greater than or equal to the thickness of the element,
 *  - are extruded perpendicular to the wall plane in case of openings in a wall
 *  - are extruded perpendicular to the slab plane in case of openings in a slab
 *  - have a local placement relative to the local placement of the voided element
 *  - have a 'Body' shape representation with 'SweptSolid' representation type
 *  - have only a single extrusion body within the 'Body' shape representation
 *
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/final/html/link/ifcopeningstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcOpeningStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */

class LX_OPENLXAPP_EXPORT OpeningStandardCase : public OpeningElement
{
    PROXY_HEADER(OpeningStandardCase, App::OpeningElement, IFCOPENINGELEMENT)

public:
    virtual ~OpeningStandardCase(void);
    virtual bool setGeometry(std::shared_ptr<Geometry> geo) override;

protected:
    OpeningStandardCase() {}
};

}  // namespace OpenLxApp