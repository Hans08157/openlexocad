#pragma once
#include <OpenLxApp/SpatialElement.h>

#include <memory>

FORWARD_DECL(App, SpatialZone)

/** @defgroup OPENLX_SPATIALELEMENTS Spatial Elements


*/

namespace OpenLxApp
{
/**
 * @brief A spatial zone is a non-hierarchical and potentially overlapping decomposition of the project under some functional consideration.
 * A spatial zone might be used to represent a thermal zone, a construction zone, a lighting zone, a usable area zone.
 * A spatial zone might have its independent placement and shape representation.
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcspatialzone.htm" target="_blank">Documentation from IFC4:
 * IfcSpatialZone</a>
 * @ingroup OPENLX_SPATIALELEMENTS
 */
class LX_OPENLXAPP_EXPORT SpatialZone : public SpatialElement
{
    PROXY_HEADER(SpatialZone, App::SpatialZone, IFCSPATIALZONE)

public:
    virtual ~SpatialZone(void);

protected:
    SpatialZone() {}
};
}  // namespace OpenLxApp

// IfcRoot -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcGloballyUniqueId>			m_GlobalId;
//  std::shared_ptr<IfcOwnerHistory>				m_OwnerHistory;				//optional
//  std::shared_ptr<IfcLabel>					m_Name;						//optional
//  std::shared_ptr<IfcText>						m_Description;				//optional

// IfcObjectDefinition -----------------------------------------------------------
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssigns> >	m_HasAssignments_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >		m_Nests_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >		m_IsNestedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDeclares> >	m_HasContext_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >	m_IsDecomposedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >	m_Decomposes_inverse;
//  std::vector<std::weak_ptr<IfcRelAssociates> >	m_HasAssociations_inverse;

// IfcObject -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcLabel>					m_ObjectType;				//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >	m_IsDeclaredBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >	m_Declares_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByType> >	m_IsTypedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByProperties> >	m_IsDefinedBy_inverse;

// IfcProduct -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcObjectPlacement>			m_ObjectPlacement;			//optional
//  std::shared_ptr<IfcProductRepresentation>	m_Representation;			//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssignsToProduct> >	m_ReferencedBy_inverse;

// IfcSpatialElement -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcLabel>					m_LongName;					//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelContainedInSpatialStructure> >	m_ContainsElements_inverse;
//  std::vector<std::weak_ptr<IfcRelServicesBuildings> >	m_ServicedBySystems_inverse;
//  std::vector<std::weak_ptr<IfcRelReferencedInSpatialStructure> >	m_ReferencesElements_inverse;

// IfcSpatialZone -----------------------------------------------------------
// attributes:
// std::shared_ptr<IfcSpatialZoneTypeEnum>		m_PredefinedType;			//optional
