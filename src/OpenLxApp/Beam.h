#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, Beam)

/** @defgroup OPENLX_BUILDINGELEMENTS Building Elements


*/

namespace OpenLxApp
{
/**
 * @brief An Beam is a horizontal, or nearly horizontal, structural member that is
 * capable of withstanding load primarily by resisting bending. It represents such a member from an architectural point of view. It is not required to
 * be load bearing.
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcbeam.htm" target="_blank">Documentation from IFC4: IfcBeam</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT Beam : public Element
{
    PROXY_HEADER(Beam, App::Beam, IFCBEAM)

public:
    enum class BeamTypeEnum
    {
        BEAM,
        JOIST,
        HOLLOWCORE,
        LINTEL,
        SPANDREL,
        T_BEAM,
        USERDEFINED,
        NOTDEFINED

    };

    void setPredefinedType(BeamTypeEnum aType);
    BeamTypeEnum getPredefinedType() const;

    virtual ~Beam(void);

    static std::shared_ptr<Beam> buildFrom2Points(std::shared_ptr<Document> aDoc,
                                                  double aWidth,
                                                  double aHeight,
                                                  const Geom::Pnt& aPnt1,
                                                  const Geom::Pnt& aPnt2);


protected:
    Beam() {}
};

}  // namespace OpenLxApp