#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Column)

namespace OpenLxApp
{
/**
 * @brief A Column is a vertical structural member which often is aligned with a structural grid intersection.
 * It represents a vertical, or nearly vertical, structural member that transmits, through compression,
 * the weight of the structure above to other structural elements below. It represents such a member from an architectural point of view.
 * It is not required to be load bearing.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifccolumn.htm" target="_blank">Documentation from IFC4: IfcColumn</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Column : public Element
{
    PROXY_HEADER(Column, App::Column, IFCCOLUMN)

public:
    enum class ColumnTypeEnum
    {
        COLUMN,
        PILASTER,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(ColumnTypeEnum aType);
    ColumnTypeEnum getPredefinedType() const;

    virtual ~Column(void);

protected:
    Column() {}
};

}  // namespace OpenLxApp