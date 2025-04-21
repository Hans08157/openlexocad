#pragma once

#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Wall)

namespace OpenLxApp
{
/**
 * @brief The wall represents a vertical construction that bounds or subdivides spaces.
 * Wall are usually vertical, or nearly vertical, planar elements, often designed to
 * bear structural loads. A wall is however not required to be load bearing.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcwall.htm" target="_blank">Documentation from IFC4: IfcWall</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Wall : public Element
{
    PROXY_HEADER(Wall, App::Wall, IFCWALL)

public:
    enum class WallTypeEnum
    {
        MOVABLE,
        PARAPET,
        PARTITIONING,
        PLUMBINGWALL,
        SHEAR,
        SOLIDWALL,
        STANDARD,
        POLYGONAL,
        ELEMENTEDWALL,
        USERDEFINED,
        NOTDEFINED
    };

    void setPredefinedType(WallTypeEnum aType);
    WallTypeEnum getPredefinedType() const;

    virtual ~Wall(void);


protected:
    Wall() {}
};

}  // namespace OpenLxApp