
/**
 * @file
 * ServiceInterface class declaration.
 *
 */

#pragma once

#include <Geom/Pnt.h>
#include <set>
namespace Core { class DocObject; }


namespace Geom
{
class Dir;
class Rect;
}

namespace Core
{
/**
 * Common definition of the segment of an arbitrary geometry.
 *
 * Variables have usually these values:
 * LINE_SEGMENT:
 * p1, p2 - boundary points
 * p3 - unused
 * parameter1, parameter2, parameter3 - unused
 *
 * CIRCLE_SEGMENT
 * p1 - top left corner of the bounding rectangle
 * p2 - bottom right corner of the bounding rectangle
 * p3 - center of the circle (arc)
 * parameter1 - starting angle of the arc (rads)
 * parameter2 - length of the circle (rads)
 * parameter3 - passage point of the arc (rads, optional)
 *
 * ENDLESS_LINE:
 * p1 - base point
 * p2 = p1 + D, where D is a normalized direction vector of the line
 * p3 - unused
 * parameter1, parameter2, parameter3 - unused
 *
 */
struct CommonGeometryDefinition
{
    enum CGS_Type
    {
        LINE_SEGMENT,
        ENDLESS_LINE,
        CIRCLE_SEGMENT

    } type;

    Geom::Pnt p1;
    Geom::Pnt p2;
    Geom::Pnt p3;

    double parameter1;
    double paremeter2;
    double parameter3;


    CommonGeometryDefinition()
    {
        type = LINE_SEGMENT;

        parameter1 = 0.0;
        paremeter2 = 0.0;
        parameter3 = 0.0;
    }
};



/**
 *
 *
 */
class CSnapperContext
{
public:
    CSnapperContext() { valid = false; }

    bool valid;
    Geom::Pnt refPoint;
};


/**
 *
 *
 */
class LX_CORE_EXPORT ServiceInterface
{
public:
    // selector interface
    virtual void selectByHit(const Geom::Rect& area) = 0;
    virtual void selectByRect(const Geom::Rect& area) = 0;

    virtual void selectByHitPlus(const Geom::Rect& area) = 0;
    virtual void selectByRectPlus(const Geom::Rect& area) = 0;

    virtual void unselectAll(void) = 0;
    virtual std::set<Core::DocObject*> getSelectedElements(void) = 0;

    virtual bool activePoint_Exists(void) = 0;
    virtual Core::DocObject* activePoint_Element(void) = 0;
    virtual Geom::Pnt activePoint_Position(void) = 0;

    virtual bool activeSegment_Exists(void) = 0;
    virtual Core::DocObject* activeSegment_Element(void) = 0;



    // snapping interface
    virtual void enableSnapper(int options, CSnapperContext context = CSnapperContext()) = 0;
    virtual void disableSnapper(void) = 0;
    virtual bool isSnap(void) = 0;
    virtual void hideSnapMark(void) = 0;

    virtual Geom::Pnt getSnapPoint(void) = 0;



    // picking interface
    virtual void enablePicker(int options) = 0;
    virtual void disablePicker(void) = 0;
    virtual bool isPick(void) = 0;
    virtual void unpick(void) = 0;
    virtual void hidePickedSegmentMark(void) = 0;

    virtual CommonGeometryDefinition getPickedSegment(void) = 0;
    virtual Core::DocObject* getPickedElement(void) = 0;



    // general
    virtual void showEndlessHelper(const Geom::Pnt& p, const Geom::Dir& d) = 0;
    virtual void hideEndlessHelper(void) = 0;

    virtual void addGeneralMark(const Geom::Pnt& p) = 0;
    virtual void removeGeneralMarks(void) = 0;

    virtual void getElementsIntersectingArea(std::vector<Core::DocObject*>& elements, const Geom::Rect& area) = 0;
};

}  // namespace Core
