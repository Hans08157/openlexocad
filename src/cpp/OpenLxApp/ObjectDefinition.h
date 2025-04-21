#pragma once


#include <LxIfcBase/LxIfcProperty.h>
#include <OpenLxApp/Root.h>

#include <memory>
#include <vector>

FORWARD_DECL(App, ObjectDefinition)

namespace OpenLxApp
{
/**
 * @brief An ObjectDefinition is the generalization of any semantically treated thing or process,
 * either being a type or an occurrences.
 * Objects are independent pieces of information that might contain or reference other pieces of information.
 * There are four essential kinds of relationships in which object definitions (by their instantiable subtypes) can be involved:
 *
 * - Assignment of other objects
 * - Association to external resources
 * - Aggregation of other objects
 * - Nesting of other objects
 * - Declaration within a context
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT ObjectDefinition : public Root
{
    PROXY_HEADER_ABSTRACT(ObjectDefinition, App::ObjectDefinition, IFCOBJECTDEFINITION)

public:
    /** @name Decomposition */
    //@{

    std::vector<std::shared_ptr<ObjectDefinition>> getDecompositionObjects() const;
    std::vector<std::shared_ptr<ObjectDefinition>> getAllDecompositionObjects() const;
    std::shared_ptr<ObjectDefinition> getDecomposedObject() const;
    std::vector<std::shared_ptr<ObjectDefinition>> getAllDecomposedObjects() const;
    //@}


    /** @name Aggregation (Specialization of a Decomposition) */
    //@{
    void addAggregationObject(std::shared_ptr<ObjectDefinition> aObject);
    void addAggregationObjects(const std::vector<std::shared_ptr<ObjectDefinition>>& aObjects);
    void removeAggregationObject(std::shared_ptr<ObjectDefinition> aObject);
    void removeAggregationObjects();
    std::vector<std::shared_ptr<ObjectDefinition>> getAggregationObjects() const;
    std::vector<std::shared_ptr<ObjectDefinition>> getAllAggregationObjects() const;
    std::shared_ptr<ObjectDefinition> getAggregatedObject() const;
    std::vector<std::shared_ptr<ObjectDefinition>> getAllAggregatedObjects() const;
    //@}

    /** @name Assignment */
    //@{
    // void addAssignmentObject(std::shared_ptr<ObjectDefinition> aObject, App::ObjectTypeEnum aObjectType = NOTDEFINED);
    // std::vector<std::shared_ptr<ObjectDefinition>> getAssignmentObjects() const;
    //@}

    /** @name Association */
    //@{
    void addAssociationObject(std::shared_ptr<Root> aObject);
    std::vector<std::shared_ptr<Root>> getAssociationObjects() const;
    //@}

    /** @name IFC Properties */
    //@{
    std::shared_ptr<LxIfcBase::LxIfcProperty> getIfcPropertySets() const;
    //@}

    virtual ~ObjectDefinition(void);

protected:
    ObjectDefinition();
};

}  // namespace OpenLxApp