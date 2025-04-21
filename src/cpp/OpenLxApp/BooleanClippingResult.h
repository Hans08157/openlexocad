#pragma once

#include <OpenLxApp/Geometry.h>




FORWARD_DECL(Part, Cut)


namespace OpenLxApp
{
/*!
 * @brief Boolean difference / cut operation
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/Add2/html/link/ifcbooleanclippingresult.htm" target="_blank">Documentation from IFC4:
 * IfcBooleanClippingResult</a>
 */

class LX_OPENLXAPP_EXPORT BooleanClippingResult : public Geometry
{
    PROXY_HEADER(BooleanClippingResult, Part::Cut, IFCBOOLEANCLIPPINGRESULT)

public:
    ~BooleanClippingResult(void);

    /// Sets the tool geometry ( = the 'hard' geo )
    void setTool(std::shared_ptr<Geometry> toolGeo);
    std::shared_ptr<Geometry> getTool() const;
    /// Sets the blank geometry ( = the 'soft' geo )
    void setBlank(std::shared_ptr<Geometry> blankGeo);
    std::shared_ptr<Geometry> getBlank() const;

private:
    BooleanClippingResult(void) {}
};
}  // namespace OpenLxApp
