#pragma once
#include <OpenLxApp/Element.h>

#include <memory>

FORWARD_DECL(App, ElementAssembly)

namespace OpenLxApp
{
/**
 * @brief The IfcElementAssembly represents complex element assemblies aggregated from several elements,
 * such as discrete elements, building elements, or other elements.
 *
 * EXAMPLE: Steel construction assemblies, such as trusses and different kinds of frames, can be represented
 * by the IfcElementAssembly entity. Other examples include slab fields aggregated from a number of precast
 * concrete slabs or reinforcement units made from several reinforcement bars. Also bathroom units, staircase sections
 * and other premanufactured or precast elements are examples of the general IfcElementAssembly entity
 *
 * NOTE:  The IfcElementAssembly is a general purpose entity that is required to be decomposed.
 * Also other subtypes of Element can be decomposed, with some dedicated entities such as WallElementedCase and SlabElementedCase.
 * The assembly structure can be nested, i.e. an ElementAssembly could be an aggregated part within another ElementAssembly.
 *
 * NOTE  View definitions and/or implementer agreements may restrict the number of allowed levels of nesting.
 * The geometry of an ElementAssembly is generally formed from its components, in which case it does not need to have
 * an explicit geometric representation. In some cases it may be useful to also expose an own explicit representation of the aggregate.
 *
 * NOTE:  View definitions or implementer agreements may further constrain the applicability of certain shape representations at the
 * ElementAssembly in respect of the shape representations of its parts.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT ElementAssembly : public Element
{
    PROXY_HEADER(ElementAssembly, App::ElementAssembly, IFCELEMENTASSEMBLY)

public:
    enum class ElementAssemblyTypeEnum
    {
        ACCESSORY_ASSEMBLY,  //	Assembled accessories or components.
        ARCH,                //	A curved structure.
        BEAM_GRID,           //	Interconnected beams, located in one(typically horizontal) plane.
        BRACED_FRAME,        //	A rigid frame with additional bracing members.
        GIRDER,              //	A beam - like superstructure.
        REINFORCEMENT_UNIT,  //	Assembled reinforcement elements.
        RIGID_FRAME,         //	A structure built up of beams, columns, etc.with moment - resisting joints.
        SLAB_FIELD,          //	Slabs, laid out in one plane.
        TRUSS,               //	A structure built up of members with(quasi) pinned joint.
        USERDEFINED,         //	User - defined element assembly.
        NOTDEFINED,          //  Undefined element assembly.
    };

    void setPredefinedType(ElementAssemblyTypeEnum aType);
    ElementAssemblyTypeEnum getPredefinedType() const;

    void addToAssembly(std::shared_ptr<Element> aElement);
    void removeFromAssembly(std::shared_ptr<Element> aElement);
    std::vector<std::shared_ptr<Element>> getAssembledElements() const;

    virtual ~ElementAssembly(void);


protected:
    ElementAssembly() {}
};

}  // namespace OpenLxApp