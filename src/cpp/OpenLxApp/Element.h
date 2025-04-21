#pragma once

#include <OpenLxApp/CdwkAttributeData.h>
#include <OpenLxApp/MaterialDefinition.h>
#include <OpenLxApp/MaterialSelect.h>
#include <OpenLxApp/Product.h>
#include <OpenLxApp/Property.h>
#include <Topo/ShapeAttributes.h>

#include <memory>

FORWARD_DECL(App, Element)

namespace OpenLxApp
{
class Group;
class Geometry;
class OpeningElement;
class SubElement;

/**
 * @brief An element is a generalization of all components that make up an AEC product.
 * Those elements can be logically contained by a spatial structure element that constitutes
 * a certain level within a project structure hierarchy (site, building, storey or space).
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT Element : public Product
{
    PROXY_HEADER(Element, App::Element, IFCELEMENT)

public:
    /** @name Placement */
    //@{
    void setPlacementRelativeTo(std::shared_ptr<Element> other);
    void setPlacementRelativeTo(std::shared_ptr<Element> other, bool keepGlobalPosition);
    std::shared_ptr<Element> getPlacementRelativeTo() const;
    //@}

    /** @name Layer */
    //@{
    bool setLayer(int layernumber);
    int getLayer() const;
    //@}

    /** @name Openings */
    //@{
    void addOpeningElement(std::shared_ptr<OpeningElement> aOpening);
    void removeOpeningElement(std::shared_ptr<OpeningElement> aOpening);
    void removeOpeningElements();
    std::vector<std::shared_ptr<OpeningElement>> getOpeningElements() const;
    //@}

    /** @name Parametric Cuts */
    //@{
    void addParamCutHardElement(std::shared_ptr<Element> aElement);
    void addParamCutSoftElement(std::shared_ptr<Element> aElement);
    void removeParamCutHardElement(std::shared_ptr<Element> aElement);
    void removeParamCutSoftElement(std::shared_ptr<Element> aElement);
    std::vector<std::shared_ptr<Element>> getParamCutHardElements(bool includeAggregatedElements = false) const;
    std::vector<std::shared_ptr<Element>> getParamCutSoftElements() const;
    bool isParamCutHardElement() const;
    bool isParamCutSoftElement() const;
    //@}

    /** @name SubElements */
    //@{
    bool addSubElement(std::shared_ptr<SubElement> aSubElement);
    std::vector<std::shared_ptr<SubElement>> getSubElements() const;
    void removeSubElement(std::shared_ptr<SubElement> aSubElement);
    void removeSubElements();
    //@}

    /** @name Fillings */
    //@{
    std::shared_ptr<OpeningElement> getFilledOpeningElement() const;
    //@}

    /** @name Material */
    //@{
    void setAssociatedMaterial(std::shared_ptr<MaterialDefinition> aMaterialDefinition);
    // void setAssociatedMaterial(std::shared_ptr<MaterialUsageDefinition> aMaterialUsageDefinition);
    void removeAssociatedMaterial();
    std::shared_ptr<MaterialSelect> getAssociatedMaterial() const;
    //@}

    /** @name Misc */
    //@{
    bool isTemporary() const;
    void setTemporary(bool on);
    std::shared_ptr<Group> getGroup() const;
    std::shared_ptr<Element> copy() const;
    Topo::Cdwk_SAT_Attributes get_Cdwk_SAT_Attributes() const;
    Base::String getTag() const;
    void setTag(const Base::String& aTag);
    
    std::string getCadworkGroup() const;
    void setBoundingBoxEnabled(bool enabled);
    CdwkAttributeData getCdwkAttributeData() const;
    void setCdwkAttributeData(const CdwkAttributeData& aData);
    //@}

    /** @desc Interface to allow "switching" between Axis and SolidModel Representations */
    //@{
    std::shared_ptr<OpenLxApp::Geometry> getAxisRepresentation() const;
    bool setAxisRepresentation(std::shared_ptr<OpenLxApp::Geometry> aGeometry) const;

    std::shared_ptr<OpenLxApp::Geometry> getSolidModelRepresentation() const;
    bool setSolidModelRepresentation(std::shared_ptr<OpenLxApp::Geometry> aGeometry) const;

    void showAxisRepresentation() const;
    void showSolidModelRepresentation() const;
    //@}

    /** @desc Interface for Connected Elements */
    //@{
    std::vector<std::shared_ptr<Element>> getElementsConnectedAtEnd() const;
    std::vector<std::shared_ptr<Element>> getElementsConnectedAtStart() const;
    std::vector<int> getJointsTypeAtEnd() const;
    std::vector<int> getJointsTypeAtStart() const;
    //@}

    /** @desc Internal do not use */
    //@{
    void     __setMiscAttributesFlags__(uint32_t aValue);
    uint32_t __getMiscAttributesFlags__() const;
    void __setElementFlags__(unsigned long aValue);
    unsigned long __getElementFlags__() const;
    //@}

    virtual ~Element() = default;

protected:
    Element() = default;
    void _copySubElems(App::Element* fromElem, std::shared_ptr<Element> toElem) const;
};

}  // namespace OpenLxApp
