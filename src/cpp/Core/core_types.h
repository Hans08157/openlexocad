
/**
 * @file
 * Global types of The CORE!
 *
 * @author Tomáš Pafèo
 */


#pragma once 

#include <chrono>
#include <unordered_set>
#include <vector>

namespace Core
{
class DocObject;

using seconds = std::chrono::duration<double>;
using time_point = std::chrono::time_point<std::chrono::steady_clock, Core::seconds>;

enum SnapType
{
    NO_SNAP = 0x00,

    GRID_SNAP = 0x01,
    ENDPOINT_SNAP = 0x02,
    INTERSECT_SNAP = 0x04,
    MIDPOINT_SNAP = 0x08,
    TANGENT_SNAP = 0x16,
    PERPENDICULAR_SNAP = 0x32,

    ALL_SNAP = 0xFF
};


enum PickType
{
    NO_PICK = 0x00,

    PICK_STRAIGHT_SEGMENTS = 0x01,
    PICK_ARC_SEGMENTS = 0x02,
    PICK_CIRCLES = 0x04,
    PICK_AUX_LINES = 0x08,

    PICK_ALL = 0xFF
};



// Obsolete types. They are only used by the CGraphBuilder
// and CObjectManager, but both of these classes are not used in the
// application anymore. Use the Core::ObjectVector, Core::ObjectSet
// and Core::ObjectMap instead.
// tp 20101209
typedef std::vector<Core::DocObject*> ObjectVector;
typedef std::vector<const Core::DocObject*> ObjectConstVector;
typedef std::unordered_set<Core::DocObject*> ObjectSet;

}  // namespace Core
