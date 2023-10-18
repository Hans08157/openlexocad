///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2021   Cadwork Informatik. All rights reserved.             //
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

#include <OpenLxApp/Element.h>
#include <OpenLxUI/SceneView.h>

namespace Gui
{
class Viewer;
}


namespace OpenLxUI
{
class ViewerP;

/**
 * @brief
 *
 * @ingroup  OPENLX_UI
 * @since    28.0
 */
class LX_OPENLXUI_EXPORT Viewer
{
public:
    Viewer(Gui::Viewer& aViewer);
    Viewer() = delete;
    virtual ~Viewer(); // Must be polymorphic for SWIG

    enum class EViewDirection
    {
        UNDEFINED,
        TOP,
        BOTTOM,
        FRONT,
        BACK,
        LEFT,
        RIGHT,
        AXO,
        AXOLEFT,
        AXOBACKRIGHT,
        AXOBACKLEFT
    };

    void lookAt(const Geom::Pnt& fromPnt, const Geom::Pnt& toPnt, const Geom::Vec& upVector);

    void viewLast();
    OpenLxUI::SceneView getCurrentSceneView();
    void saveSceneView(OpenLxUI::SceneView& view);
    void setSceneView(const OpenLxUI::SceneView& view, bool forceNotAnimated = false);

    bool isZoomViewAvailable() const;
    void saveZoomView();
    void viewLastZoomView();
    void clearZoomViews();

    double getZGroundPlate() const;
    void setZGroundPlate(bool aOn, double val);

    bool getProjectAllToZGroundPlate() const;
    void setProjectAllToZGroundPlate(bool aOn);
    bool getProjectAllToWPlane() const;
    void setProjectAllToWPlane(bool aOn);

    void enablePlaneMode();
    void enablePlaneMode(const Geom::Pln& aPln);
    void disablePlaneMode();
    bool getPlaneMode(Geom::Pln& p);
    void setPlaneMode(const Geom::Pln& aPln);
    void setActive(bool on);
    void loadVisibility() const;

    void viewAll(float animationTime = 0.f, const Geom::Dir& upVec = Geom::Dir(0, 1, 0), Geom::Bnd_Box* bbox = 0);
    void viewElement(std::shared_ptr<OpenLxApp::Element> e, float animationTime = 0.f, const Geom::Dir& upVec = Geom::Dir(0, 1, 0));
    void viewBoundingBox(Geom::Bnd_Box bbox, float animationTime = 0.f, const Geom::Dir& upVec = Geom::Dir(0, 1, 0));
    void view(EViewDirection direction,
              float animationTime = 0.f,
              const Geom::Dir& upVec = Geom::Dir(0, 1, 0),
              Geom::Bnd_Box* bbox = 0,
              double rotZ = 0);

    void viewOrthogonal();
    void viewPerspective();

    void zoom(const float diffvalue);
    void zoomToPoint(Geom::Pnt p, double radius, double animateTime);
    void redraw();

    /** Animates the active camera to this position and viewpoint */
    void animateActiveCamera(const Geom::Vec& toPosition,
                                     const Geom::Vec& toViewpoint,
                                     float animationLength,
                                     const double* toFov = 0,
                                     const double* toRotation = 0);
    /** Sets the background color of the viewer */
    void setBackgroundColor(const Base::Color& aColor);
    /** Returns the background color of the viewer */
    Base::Color getBackgroundColor() const;

    bool centeringZoom(float& ppdst, Geom::Ax2 coordsys, bool smallmode = false);
    void zoomToCursor(Geom::Ax2 coordsys, bool forward);
    void walkThruMove(int dir, bool orbit, double speed = 0.);

    void setElementVisibilityInViewer(std::shared_ptr<OpenLxApp::Element> e, bool visible);
    void setElementsVisibilityInViewer(const std::vector<std::shared_ptr<OpenLxApp::Element>>& elems, bool visible);

    void enableShading(bool on);
    bool isShading();

    /*void highlightDetail(bool aOn, CA_Detail::Type type);
    void highlightByType(bool aOn, Base::Type type);
    void setNotHighlightedNotSelectable(bool aOn);
    void setNoSelectedElement(bool on);
    void setOnlySelectedElement(bool on);
    void setOnlySelectedDetail(bool on);*/

    Geom::Pnt2d mapToGlobal(const Geom::Pnt2d& in);


    std::string getDefaultCursor();
    void setDefaultCursor(const std::string& c);
    void setDraggingRestriction(bool on);
    void checkForCameraUpConstrain();
    Geom::Bnd_Box getSceneBoundingBox();

    bool hasAutomaticFocalDistance() const;
    void setAutomaticFocalDistance(bool on);
    double getOldFocalDistance() const;
    void setOldFocalDistance(double d);

    void setBlockRedraw(bool on);
    void blockRedrawAfterRedrawing(bool on);

    /** @name Internal. Only use if you know what you are doing! */
    //@{
    bool __is2dTopViewer__() const;
    bool __hasSecondViewer__() const;

    int __getMultiViewerIndex__();
    int __getActiveMultiSecondViewerIndex__();
    //@}

private:
    std::unique_ptr<OpenLxUI::ViewerP> mPimpl;
};
}  // namespace OpenLxUI