#pragma once
#include <OpenLxApp/Element.h>
#include <memory>

FORWARD_DECL(App, OpeningElement)

namespace OpenLxApp
{
/*!
 * @brief The opening element stands for opening, recess or chase, all reflecting voids.
 * It represents a void within any element that has physical manifestation.
 * Openings can be inserted into walls, slabs, beams, columns, or other elements.
 *
 * (Definition from ISO/CD 16739:2011)
 *
 * @see <a href="http://www.buildingsmart-tech.org/ifc/IFC4/final/html/link/ifcopeningelement.htm" target="_blank">Documentation from IFC4:
 * IfcOpeningElement</a>
 * @ingroup OPENLX_BUILDINGELEMENTS
 */
class LX_OPENLXAPP_EXPORT OpeningElement : public Element
{
    PROXY_HEADER(OpeningElement, App::OpeningElement, IFCOPENINGELEMENT)

public:
    enum class OpeningElementTypeEnum
    {
        OPENING,  // An opening as subtraction feature that cuts through the element it voids.It thereby creates a hole.An opening in addition have a
                  // particular meaning for either providing a void for doors or windows, or an opening to permit flow of air and passing of light.
        RECESS,   // An opening as subtraction feature that does not cut through the element it voids.It creates a niche or similar voiding pattern.
        USERDEFINED,  // User - defined opening element.
        NOTDEFINED    // Undefined opening element.
    };

    void setPredefinedType(OpeningElementTypeEnum aType);
    OpeningElementTypeEnum getPredefinedType() const;

    void addFilling(std::shared_ptr<Element> aFilling);
    std::vector<std::shared_ptr<Element>> getFillings() const;
    void removeFilling(std::shared_ptr<Element> aFilling);
    void removeFillings();

    std::shared_ptr<Element> getVoidedElement() const;

    virtual ~OpeningElement(void);


protected:
    OpeningElement() {}
};

}  // namespace OpenLxApp