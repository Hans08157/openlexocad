#pragma once

#ifndef END_OF_LOOP
#define END_OF_LOOP -2
#endif

#ifndef END_OF_FACE
#define END_OF_FACE -1
#endif

#undef DOOR
#define UNUSED(expr) \
    do \
    { \
        (void)(expr); \
    } while (0)

namespace Base
{
class String;
}

namespace Base
{
///////////////////////////////////////////////////////////
//                                                       //
// --------------------- BEGIN API --------------------- //
//                                                       //
// ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
//                                                       //
///////////////////////////////////////////////////////////


enum class FormworkType
{
    PANEL,
    INNERCORNER,
    OUTERCORNER
};

enum class FillingType
{
    NOFILLING,
    WINDOW,
    DOOR,
    BASICWINDOW,
    BASICDOOR
};

enum class OpeningType  // !!!!!!   NEW ENTRIES MUST BE AT THE END, BECAUSE OF SAVING AS INT   !!!!!!!
{
    WALL,
    RECTANGLE = 0,
    TRAPEZOID,
    ARCHED,
    OCTAGON,
    TRIANGLE,
    CIRCLE_WIN,
    ELLIPSE_WIN,
    SEMICIRCLE,
    FRENCHWINDOW,
    DOOR,
    GARAGEDOOR,
    FLOOR,          // for Openings
    ROOF,           // for Openings
    GENERAL,        // for Openings
    TYPE_FOR_COPY,  // fast solution
    ARCHDOOR,
    ARCHTOP,
    PENTAGON,
    QUARTERCIRCLE,
    TRANSOMDOOR,
    NOTDEFINED
};

enum class PurposeGroup  // because Doors are divided to user groups according e.g. directories with textures
{
    DOOR,
    GARAGE,
    FRENCHWINDOW,
    ARCHDOOR,
    TRANSOMDOOR,
    NOTDEFINED
};

enum class DoorTypeOperationEnum
{
    SINGLE_SWING_LEFT = 0,
    SINGLE_SWING_RIGHT = 1,
    DOUBLE_DOOR_SINGLE_SWING = 2,
    DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_LEFT = 3,
    DOUBLE_DOOR_SINGLE_SWING_OPPOSITE_RIGHT = 4,
    DOUBLE_SWING_LEFT = 5,
    DOUBLE_SWING_RIGHT = 6,
    DOUBLE_DOOR_DOUBLE_SWING = 7,
    SLIDING_TO_LEFT = 8,
    SLIDING_TO_RIGHT = 9,
    DOUBLE_DOOR_SLIDING = 10,
    FOLDING_TO_LEFT = 11,
    FOLDING_TO_RIGHT = 12,
    DOUBLE_DOOR_FOLDING = 13,
    REVOLVING = 14,
    ROLLINGUP = 15,
    SWING_FIXED_LEFT = 16,
    SWING_FIXED_RIGHT = 17,
    USERDEFINED = 18,
    NOTDEFINED = 19,
    // INVERT_SINGLE_SWING_RIGHT = 20,       // Deprecated, use 'placeDoorOnReferenceSide' property in Doors.
    // INVERT_SINGLE_SWING_LEFT = 21,        // Deprecated, use 'placeDoorOnReferenceSide' property in Doors.
    // INVERT_SWING_FIXED_RIGHT = 22,        // Deprecated, use 'placeDoorOnReferenceSide' property in Doors.
    // INVERT_SWING_FIXED_LEFT = 23,         // Deprecated, use 'placeDoorOnReferenceSide' property in Doors.
    TRIPLE_DOOR_SWING_RIGHT = 24,         // Lexocad only
    TRIPLE_DOOR_SWING_LEFT = 25,          // Lexocad only
    TRIPLE_DOOR_TRIPLE_SWING_RIGHT = 26,  // Lexocad only
    TRIPLE_DOOR_TRIPLE_SWING_LEFT = 27    // Lexocad only
};

enum class Divider
{
    NONE,
    VERTICAL,
    CROSS,
    HORIZONTAL,
    TWOVERTICAL
};

// used for CmdBooleanSplitShapeWithPlane
enum class SplitStatus
{
    PLANE,
    HORIZONTAL,
    VERTICAL_X,
    VERTICAL_Y,
    VIEWER_PERPENDICULAR_2P,
    TWO_SURFACES,
    MESH_SPLIT,
    PLANE_3P,
    VERTICAL_LINE,
    VERTICAL_FACE_FOR_TERRAIN,
    PROJECT_VERTICAL_LINE,
    LINE_ON_MESH,
    CUT_AND_FILL_MESH,
    CUT_BIM_ACC_LINE,
    CUT_BY_RECTANGLE,
    CUT_BY_CONTOUR,
    BOOLEAN_CUT,
    PARAMETRIC_CUT,
    CUT_IN_TWO,  // just to pass in constructor, to avoid bool
    CUT_TERRAIN,
    CUT_BY_SURFACESS_ACC_COLOR,
};

///////////////////////////////////////////////////////////
//                                                       //
// ---------------------- END API ---------------------- //
//                                                       //
///////////////////////////////////////////////////////////


}  // namespace Base