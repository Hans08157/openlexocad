#pragma once
#include <OpenLxApp/Product.h>

#include <memory>

FORWARD_DECL(App, SpatialElement)

/** @defgroup OPENLX_SPATIALELEMENTS Spatial Elements


*/

namespace OpenLxApp
{
/**
 * @brief A spatial element is the generalization of all spatial elements that might be used to define a spatial structure or to define spatial zones.
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcspatialelement.htm" target="_blank">Documentation from
 * IFC4: IfcSpatialElement</a>
 * @ingroup OPENLX_SPATIALELEMENTS
 */
class LX_OPENLXAPP_EXPORT SpatialElement : public Product
{
    PROXY_HEADER_ABSTRACT(SpatialElement, App::SpatialElement, IFCSPATIALELEMENT)

public:
    virtual ~SpatialElement(void);

protected:
    SpatialElement() {}
};
}  // namespace OpenLxApp



// IfcRoot -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcGloballyUniqueId>								m_GlobalId;
//  std::shared_ptr<IfcOwnerHistory>									m_OwnerHistory;				//optional
//  std::shared_ptr<IfcLabel>										m_Name;						//optional
//  std::shared_ptr<IfcText>											m_Description;				//optional

// IfcObjectDefinition -----------------------------------------------------------
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssigns> >						m_HasAssignments_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >							m_Nests_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >							m_IsNestedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDeclares> >						m_HasContext_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >					m_IsDecomposedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >					m_Decomposes_inverse;
//  std::vector<std::weak_ptr<IfcRelAssociates> >					m_HasAssociations_inverse;

// IfcObject -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcLabel>										m_ObjectType;				//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >				m_IsDeclaredBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >				m_Declares_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByType> >					m_IsTypedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByProperties> >			m_IsDefinedBy_inverse;

// IfcProduct -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcObjectPlacement>								m_ObjectPlacement;			//optional
//  std::shared_ptr<IfcProductRepresentation>						m_Representation;			//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssignsToProduct> >				m_ReferencedBy_inverse;

// IfcSpatialElement -----------------------------------------------------------
// attributes:
// std::shared_ptr<IfcLabel>										m_LongName;					//optional
// inverse attributes:
// std::vector<std::weak_ptr<IfcRelContainedInSpatialStructure> >	m_ContainsElements_inverse;
// std::vector<std::weak_ptr<IfcRelServicesBuildings> >				m_ServicedBySystems_inverse;
// std::vector<std::weak_ptr<IfcRelReferencedInSpatialStructure> >	m_ReferencesElements_inverse;
