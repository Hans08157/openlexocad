#pragma once


#include <OpenLxApp/ObjectDefinition.h>
#include <memory>

FORWARD_DECL(App, Object)

namespace OpenLxApp
{
/**
 * @brief An IfcObject is the generalization of any semantically treated thing or process. Objects are things as they appear - i.e. occurrences.
 *
 * NOTE  Examples of IfcObject include physically tangible items such as wall, beam or covering, physically existing items such as spaces,
 * or conceptual items such as grids or virtual boundaries. It also stands for processes such as work tasks, for controls such as cost items,
 * or for actors such as persons involved in the design process.
 * Objects can be named, using the inherited Name attribute, which should be a user recognizable label for the object occurrence.
 * Further explanations to the object can be given using the inherited Description attribute. The ObjectType attribute is used:
 *
 * to store the user defined value for all subtypes of IfcObject, where a PredefinedType attribute is given, and its value is set to USERDEFINED.
 * to provide a type information (could be seen as a very lightweight classifier) of the subtype of IfcObject, if no PredefinedType attribute is
 * given. This is often the case, if no comprehensive list of predefined types is available. Objects are independent pieces of information that might
 * contain or reference other pieces of information. There are several relationships in which objects can be involved:
 *
 * - Association to external/internal resource information - an association relationship that refers to external/internal sources of information. See
 * supertype IfcObjectDefinition for more information.
 * - Assignment of other objects - an assignment relationship that refers to other types of objects. See supertype IfcObjectDefinition for more
 * information.
 * - Aggregation of other objects - an aggregation relationship that establishes a whole/part relation. Objects can either be a whole, or a part, or
 * both. See supertype IfcObjectDefinition for more information.
 * - Assignment of a type : IsTypedBy - a definition relationship IfcRelDefinesByType that uses a type definition to define the common characteristics
 * of this occurrences, potentially including the common shape representation and common properties of all object occurrences assigned to this type.
 * It is a specific - occurrence relationship with implied dependencies (as the occurrence properties depend on the properties of the type, but may
 * override them).
 * - Assignment of a partial type : IsDeclaredBy, Declares - a definition relationship IfcRelDefinesByObject that uses a component of a type
 * definition (a part of a type, called the "declaring part") to define a component of an occurence (part of occurrence, called the "reflected part").
 * This is also refered to as a "deep copy". The common characteristics of all parts in the occurrence are defined by parts in the type. It is a
 * specific - occurrence relationship with implied dependencies (as the occurrence properties depend on the properties of the type, but may override
 * them).
 * - Assignment of property sets : IsDefinedBy - a definition relationship IfcRelDefinesByProperties that assignes property set definitions to the
 * object occurrence.
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT Object : public ObjectDefinition
{
    PROXY_HEADER_ABSTRACT(Object, App::Object, IFCOBJECT)

public:
    /** @name TypeObject */
    //@{

    //@}


    /** @name PropertySets*/
    //@{

    //@}



    virtual ~Object(void);

protected:
    Object();
};

}  // namespace OpenLxApp