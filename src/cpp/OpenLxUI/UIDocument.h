///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once

#include <Base/String.h>
#include <Core/DocObject.h>
#include <Geom/Dir.h>
#include <Geom/Pnt.h>
#include <Gui/AbstractPreview.h>
#include <Gui/Action.h>
#include <Gui/PickingService.h>
#include <Gui/PropertyTree.h>
#include <Gui/SceneGraphInterface.h>
#include <OpenLxApp/Application.h>
#include <OpenLxApp/CartesianPoint.h>
#include <OpenLxApp/Document.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/Globals.h>
#include <OpenLxUI/ActiveEdge.h>
#include <OpenLxUI/ActiveFace.h>
#include <OpenLxUI/ActiveVertex.h>

#include <OpenLxUI/Selection.h>
#include <OpenLxUI/UIElement.h>

#include <vector>



namespace OpenLxUI
{
class UIDocumentP;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    24.0
 */
class LX_OPENLXUI_EXPORT UIDocument
{
public:
    friend class UIApplication;

    std::shared_ptr<OpenLxApp::Document> getDocument() const;
    std::shared_ptr<OpenLxUI::Selection> getSelection() const;

    //
    std::shared_ptr<OpenLxUI::UIElement> getUIElement(std::shared_ptr<OpenLxApp::DocObject> aObj) const;
    std::shared_ptr<OpenLxUI::UIElement> getUIElement(Core::DocObject* aObj) const;

    // PICKING
    bool pickPoint();
    Geom::Pnt getPickedPoint();
    std::shared_ptr<OpenLxApp::Element> getPickedElement();
    bool hasPickedNormal();
    Geom::Dir getPickedNormal();
    Gui::PickingService* getPickingService();
    void setIntersectionPicking(bool onoff);
    bool isIntersectionPickingEnabled();


    // SNAPPING
    enum SnapMode
    {
        NOPOINT = 1 << 1,
        NEARESTPOINT = 1 << 2,
        MIDPOINT = 1 << 3,
        ENDPOINT = 1 << 4,
        GRIDPOINT = 1 << 5,
        BBOXPOINT = 1 << 6,
        INTERSECTIONPOINT = 1 << 7,
        EDGEPOINT = 1 << 8,
        ONLYVERTICES = 1 << 9,
        ONLYVIRTUALGEO = 1 << 10,
        CONTROLPOINT = 1 << 11,
        INVISIBLECONTROLPOINT = 1 << 12,
        AUXILIARYPOINT = 1 << 13
    };

    unsigned long getSnapMode();
    unsigned long getSnapfor2dElements();
    void setSnapMode(unsigned long mode);

    // MISC
    static bool getPlaneMode(Geom::Pln& p);
    void moveMouseToWorldPnt(const Geom::Pnt& pntTo);
    std::shared_ptr<OpenLxApp::CartesianPoint> getMidPoint(unsigned long snapMode);


    // PREVIEW AND HIGHLIGHTING
    void drawRubberBand(const Geom::Pnt& fromPnt);
    void removeRubberBand();
    void highlightByShapeType(Topo::ShapeType shapeType);
    void stopHighlightByShapeType();
    void drawElementPositionPreview(std::shared_ptr<OpenLxApp::Element> aElem, const Geom::Pnt& startPnt);
    // LX_OPENLXUI_EXPORT void showElementAttributesInViewer(const Gui::ShowAttributesFlags& flags, const Base::Color& color = Base::Color(128, 0, 255),
    // int pointSize = 20, bool bold = false);
    void hideElementAttributesInViewer();
    Gui::AbstractTangentArcPreview* createTangentArcPreview(const Geom::Pnt& pnt, const Geom::Vec& tangent);
    Gui::AbstractLinePreview* createLinePreview(const Geom::Pnt& startPnt);
    Gui::AbstractArc3PointsPreview* createArc3PointsPreview(
        const Geom::Pnt& startPnt,
        const Geom::Pnt& fixedPnt,
        Gui::AbstractArc3PointsPreview::PreviewMode mode = Gui::AbstractArc3PointsPreview::ENDPOINT_CHANGES);
    void drawPreview(Gui::AbstractPreview* preview);
    void removePreview(Gui::AbstractPreview* preview);
    void removeAllPreviews();
    void getAllPreviews(std::set<Gui::AbstractPreview*>& pw);
    void enablePreview(Gui::AbstractPreview* preview);
    void disablePreview(Gui::AbstractPreview* preview);

    void drawAngle(const Geom::Pnt& center, const Geom::Dir& normal, double angle);
    void removeAngle();

    enum class Justification
    {
        LEFT = 1,
        RIGHT,
        CENTER
    };

    Gui::SG_Node drawOwnText2(const Geom::Pnt& pnt,
                              const Base::String& text,
                              const Base::Color& color = Base::Color(255, 0, 0),
                              float fontSize = 32,
                              const Base::String& fontName = Base::String(L"Arial"),
                              bool bold = false,
                              Justification ju = Justification::CENTER);
    Gui::SG_Node drawOwnText2(const std::vector<Geom::Pnt>& pnts,
                              const Base::String& text,
                              const Base::Color& color = Base::Color(255, 0, 0),
                              float fontSize = 32,
                              const Base::String& fontName = Base::String(L"Arial"),
                              bool bold = false,
                              Justification ju = Justification::CENTER);
    void removeOwnText2(Gui::SG_Node aNode);

    void drawHelpPoint(const Geom::Pnt& p);
    void drawHelpVector(const Geom::Pnt& p, const Geom::Vec& v);
    void drawHelpAx2(const Geom::Ax2& axis2, const double& magnitude);
    void removeHelpObjects();

    Gui::SG_Node drawOwnDirection(const Geom::Pnt& pnt, const Geom::Dir& dir, const Base::Color& color = Base::Color(255, 0, 0));
    Gui::SG_Node drawOwnDirectionToPoint(const Geom::Pnt& pnt, const Geom::Dir& dir, const Base::Color& color = Base::Color(255, 0, 0));
    void removeOwnDirection(Gui::SG_Node ownDirection);

    Gui::SG_Node drawOwnLine(const std::vector<Geom::Pnt>& pnts,
                             int thickenss,
                             const Base::Color& color = Base::Color(255, 0, 0),
                             bool dashed = false);
    Gui::SG_Node drawOwnOverlayLine(const std::vector<Geom::Pnt>& pnts,
                                    int thickenss,
                                    const Base::Color& color = Base::Color(255, 0, 0),
                                    bool dashed = false);
    void removeOwnLine(Gui::SG_Node ownLine);

    Gui::SG_Node drawOwnMesh(const std::vector<Geom::Pnt>& points,
                             const std::vector<int>& model,
                             const Base::Color& color,
                             int transparency,
                             const Base::Color& emissiveColor = Base::Color(0, 0, 0));
    void removeOwnMesh(Gui::SG_Node ownMesh);

    void drawAuxiliaryLine(const Geom::Pnt& orgin, const Geom::Dir& dir);
    void drawHelpPointMeasure(const std::string& name, const Geom::Pnt& pos, float red = 1.0f, float green = 1.0f, float blue = 0.0f);
    void removeHelpPointsMeasure();

    std::vector<std::shared_ptr<OpenLxApp::Element>> getVisibleElements() const;
    std::vector<std::shared_ptr<OpenLxApp::Element>> getSelectedElements() const;

    std::shared_ptr<OpenLxApp::Element> getActiveElement() const;
    std::shared_ptr<OpenLxApp::SubElement> getActiveSubElement() const;
    bool hasActivePoint() const;
    Geom::Pnt getActivePoint() const;
    std::shared_ptr<ActiveVertex> getActiveVertex() const;
    std::shared_ptr<ActiveEdge> getActiveEdge() const;
    std::shared_ptr<ActiveFace> getActiveFace() const;

    ~UIDocument();

private:
    UIDocument(std::shared_ptr<OpenLxApp::Document> aDoc);
    UIDocument() {}
    std::shared_ptr<OpenLxUI::UIDocumentP> _pimpl;
};
}  // namespace OpenLxUI