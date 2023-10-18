
/**
 * @file
 * ViewMgrInterface class declaration.
 *
 */

#pragma once

#include <Geom/Pnt.h>
#include <Geom/Rect.h>


namespace Core
{
class CViewport;
class CAbstractPreviewInt;

enum SpecialCursor
{
    CURSOR_DOT,
    CURSOR_DELETE
};



/**
 *
 *
 */
class LX_CORE_EXPORT ViewMgrInterface
{
public:
    virtual Geom::Rect map2Scene(const Core::CViewport& viewport) = 0;
    virtual Geom::Rect map2Scene(const Geom::Rect& rect) = 0;
    virtual Geom::Pnt map2Scene(const Geom::Pnt& p) = 0;
    virtual Geom::Pnt map2Scene(int x, int y) = 0;

    virtual Geom::Rect map2View(const Geom::Rect& rect) = 0;
    virtual Geom::Pnt map2View(const Geom::Pnt& p) = 0;
    virtual Geom::Pnt map2View(double x, double y) = 0;

    virtual void fit(const Geom::Rect& rect_scene) = 0;
    virtual void fit(double x, double y, double w, double h) = 0;

    virtual void centerView(const Geom::Pnt& p) = 0;
    virtual void centerView(double x, double y) = 0;
    virtual void translateView(const Geom::Pnt& dp) = 0;
    virtual void translateView(double dx, double dy) = 0;
    virtual void scaleView(double factor) = 0;

    virtual void zoom(double z, bool storeView = true) = 0;

    virtual void setTheSceneRect(const Geom::Rect& rect) = 0;
    virtual Geom::Rect getSceneRect() = 0;
    virtual CViewport getViewport() = 0;

    virtual void updateView() = 0;


    // cursor interface
    //
    virtual void setCursor_DefaultViewing() = 0;
    virtual void setCursor_DefaultDrawing() = 0;
    virtual void setCursor_Panning() = 0;
    virtual void setCursor_Blank() = 0;
    virtual void setCursor_DND() = 0;
    virtual void setCursor_Special(SpecialCursor c) = 0;

    virtual Geom::Pnt getCursorPosition_Viewport() = 0;
    virtual Geom::Pnt getCursorPosition_Scene() = 0;
    virtual void setCursorPosition(int local_x, int local_y) = 0;
    virtual void setTheFocus() = 0;

    virtual void pushCursor() = 0;
    virtual void popCursor() = 0;


    // preview interface
    //
    virtual CAbstractPreviewInt* startPreview(const std::string& type) = 0;
    virtual void updateAllPreviewsDest(double x, double y) = 0;
    virtual void stopAllPreviews() = 0;
    virtual void hideAllPreviews() = 0;
    virtual void showAllPreviews() = 0;

    virtual void startSelectionBand(int x, int y, int style = 0) = 0;
    virtual void stopSelectionBand() = 0;



// debugging interface
#ifndef NDEBUG

public:
    virtual void DEBUG_addRectangle(const Geom::Rect& rect, int r, int g, int b) = 0;
    virtual void DEBUG_addLine(const Geom::Pnt& p1, const Geom::Pnt& p2, int r, int g, int b) = 0;
    virtual void DEBUG_addLine(const Geom::Lin& l, int r, int g, int b) = 0;
    virtual void DEBUG_addArc(const Geom::Pnt& center, double radius, double startAngle_rad, double arcLengeth_rad, int r, int g, int b) = 0;
    virtual void DEBUG_clear(void) = 0;
#endif
};


/**
 *
 *
 */
class CViewport
{
public:
    int width;
    int height;


    CViewport()
    {
        width = 0;
        height = 0;
    }

    Geom::Rect toRect() { return Geom::Rect(0.0, 0.0, width, height); }

    bool isValid()
    {
        if (width > 0 && height > 0)
            return true;
        else
            return false;
    }

    bool contains(const Geom::Pnt& point)
    {
        if (!isValid())
            return false;

        if (point.x() < 0 || point.x() > width)
            return false;

        if (point.y() < 0 || point.y() > height)
            return false;
        else
            return true;
    }
};



}  // namespace Core

