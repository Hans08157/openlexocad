#pragma once
#include <OpenLxApp/Column.h>

#include <memory>

FORWARD_DECL(App, ColumnStandardCase)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief The standard column, ColumnStandardCase, defines a column with certain constraints for the provision of material usage, parameters and with
 * certain constraints for the geometric representation. The IfcColumnStandardCase handles all cases of columns, that:
 * - have a reference to the MaterialProfileSetUsage defining the material profile association of the column with the cardinal point of its insertion
 * relative to the local placement.
 *  - are based on a sweep of a planar profile, or set of profiles, as defined by the MaterialProfileSet
 *  - have an 'Axis' shape representation with constraints provided below in the geometry use definition
 *  - have a 'Body' shape representation with constraints provided below in the geometry use definition
 *  - have a start profile, or set of profiles, that is swept along the directrix and might be changed uniformly by a taper definition
 *  - are consistent in using the correct cardinal point offset of the profile as compared to the 'Axis' and 'Body' shape representation
 *  - are extruded perpendicular to the profile definition plane
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccolumnstandardcase.htm" target="_blank">Documentation from IFC4:
 * IfcColumnStandardCase</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT ColumnStandardCase : public Column
{
    PROXY_HEADER(ColumnStandardCase, App::ColumnStandardCase, IFCCOLUMNSTANDARDCASE)

public:
    virtual ~ColumnStandardCase(void);

protected:
    ColumnStandardCase() {}
};

}  // namespace OpenLxApp