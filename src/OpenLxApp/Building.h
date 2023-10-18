#pragma once
#include <OpenLxApp/BuildingStorey.h>
#include <OpenLxApp/SpatialStructureElement.h>

#include <memory>

FORWARD_DECL(App, Building)

/** @defgroup OPENLX_SPATIALELEMENTS Spatial Elements


*/

namespace OpenLxApp
{
/**
 * @brief A building represents a structure that provides shelter for its occupants or contents and stands in one place.
 * The building is also used to provide a basic element within the spatial structure hierarchy for the components of a
 * building project (together with site, storey, and space).
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcbuilding.htm" target="_blank">Documentation from IFC4:
 * IfcBuilding</a>
 * @ingroup OPENLX_SPATIALELEMENTS
 */
class LX_OPENLXAPP_EXPORT Building : public SpatialStructureElement
{
    PROXY_HEADER(Building, App::Building, IFCBUILDING)

public:
    virtual ~Building(void);

    void addBuildingStorey(std::shared_ptr<BuildingStorey> aBuildingStorey);
    std::vector<std::shared_ptr<BuildingStorey>> getBuildingStoreys() const;

protected:
    Building() {}
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

// IfcSpatialStructureElement -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcElementCompositionEnum>	m_CompositionType;			//optional

// IfcBuilding -----------------------------------------------------------
// attributes:
// std::shared_ptr<IfcLengthMeasure>			m_ElevationOfRefHeight;		//optional
// std::shared_ptr<IfcLengthMeasure>			m_ElevationOfTerrain;		//optional
// std::shared_ptr<IfcPostalAddress>			m_BuildingAddress;			//optional
