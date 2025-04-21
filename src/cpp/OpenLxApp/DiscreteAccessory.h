#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, DiscreteAccessory)

/** @defgroup OPENLX_ELEMENTS Elements


*/

namespace OpenLxApp
{
/**
 * @brief A discrete accessory is a representation of different kinds of accessories included in or added to elements.
 *
 * @see <a href="https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/link/ifcdiscreteaccessory.htm" target="_blank">Documentation from IFC4: IfcDiscreteAccessory</a>
 * @ingroup OPENLX_ELEMENTS
 */
class LX_OPENLXAPP_EXPORT DiscreteAccessory : public Element
{
    PROXY_HEADER(DiscreteAccessory, App::DiscreteAccessory, IFCDISCRETEACCESSORY)

public:
    //enum class DiscreteAccessoryTypeEnum
    //{
    //    ANCHORPLATE,            //	An accessory consisting of a steel plate, shear stud connectors or welded - on rebar which is embedded into the surface of a concrete element so that other elements can be welded or bolted onto it later.
    //    BRACKET,                //	An L - shaped or similarly shaped accessory attached in a corner between elements to hold them together or to carry a secondary element.
    //    SHOE,                   //	A column shoe or a beam shoe(beam hanger) used to support or secure an element.
    //    EXPANSION_JOINT_DEVICE, // Assembly connection element between construction elements to allow for thermic differential expansions.
    //    USERDEFINED,            //	User - defined accessory.
    //    NOTDEFINED              //	Undefined accessory.
    //};

    //void setPredefinedType(DiscreteAccessoryTypeEnum aType);
    //DiscreteAccessoryTypeEnum getPredefinedType() const;

    virtual ~DiscreteAccessory(void);




protected:
    DiscreteAccessory() {}
};

}  // namespace OpenLxApp