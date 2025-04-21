#pragma once
#include <OpenLxApp/Building.h>
#include <OpenLxApp/SpatialStructureElement.h>

#include <memory>

FORWARD_DECL(App, Site)

/** @defgroup OPENLX_SPATIALELEMENTS Spatial Elements


*/

namespace OpenLxApp
{
/**
 * @brief A site is a defined area of land, possibly covered with water, on which the project construction is to be completed.
 * A site may be used to erect, retrofit or turn down building(s), or for other construction related developments.
 *
 * @see <a href="http://standards.buildingsmart.org/IFC/RELEASE/IFC4/ADD2_TC1/HTML/link/ifcsite.htm" target="_blank">Documentation from IFC4:
 * IfcSite</a>
 * @ingroup OPENLX_SPATIALELEMENTS
 */
class LX_OPENLXAPP_EXPORT Site : public SpatialStructureElement
{
    PROXY_HEADER(Site, App::Site, IFCSITE)

public:
    virtual ~Site(void);

    void addBuilding(std::shared_ptr<Building> aBuilding);
    std::vector<std::shared_ptr<Building>> getBuildings() const;

protected:
    Site() {}
};
}  // namespace OpenLxApp



// IfcRoot -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcGloballyUniqueId>				m_GlobalId;
//  std::shared_ptr<IfcOwnerHistory>					m_OwnerHistory;				//optional
//  std::shared_ptr<IfcLabel>						m_Name;						//optional
//  std::shared_ptr<IfcText>							m_Description;				//optional

// IfcObjectDefinition -----------------------------------------------------------
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssigns> >		m_HasAssignments_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >			m_Nests_inverse;
//  std::vector<std::weak_ptr<IfcRelNests> >			m_IsNestedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDeclares> >		m_HasContext_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >	m_IsDecomposedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelAggregates> >	m_Decomposes_inverse;
//  std::vector<std::weak_ptr<IfcRelAssociates> >	m_HasAssociations_inverse;

// IfcObject -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcLabel>						m_ObjectType;				//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >	m_IsDeclaredBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByObject> >	m_Declares_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByType> >	m_IsTypedBy_inverse;
//  std::vector<std::weak_ptr<IfcRelDefinesByProperties> >	m_IsDefinedBy_inverse;

// IfcProduct -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcObjectPlacement>				m_ObjectPlacement;			//optional
//  std::shared_ptr<IfcProductRepresentation>		m_Representation;			//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelAssignsToProduct> >	m_ReferencedBy_inverse;

// IfcSpatialElement -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcLabel>						m_LongName;					//optional
// inverse attributes:
//  std::vector<std::weak_ptr<IfcRelContainedInSpatialStructure> >	m_ContainsElements_inverse;
//  std::vector<std::weak_ptr<IfcRelServicesBuildings> >	m_ServicedBySystems_inverse;
//  std::vector<std::weak_ptr<IfcRelReferencedInSpatialStructure> >	m_ReferencesElements_inverse;

// IfcSpatialStructureElement -----------------------------------------------------------
// attributes:
//  std::shared_ptr<IfcElementCompositionEnum>		m_CompositionType;			//optional

// IfcSite -----------------------------------------------------------
// attributes:
// std::shared_ptr<IfcCompoundPlaneAngleMeasure>	m_RefLatitude;				//optional
// std::shared_ptr<IfcCompoundPlaneAngleMeasure>	m_RefLongitude;				//optional
// std::shared_ptr<IfcLengthMeasure>				m_RefElevation;				//optional
// std::shared_ptr<IfcLabel>						m_LandTitleNumber;			//optional
// std::shared_ptr<IfcPostalAddress>				m_SiteAddress;				//optional
