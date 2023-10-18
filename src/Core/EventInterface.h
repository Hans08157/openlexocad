#pragma once 

namespace Core
{
enum Key
{
    // values are the same as in the Qt (also ASCII),
    // DON'T CHANGE them

    KEY_NONE = 0x00,
    KEY_ESCAPE = 0x01000000,
    KEY_ENTER = 0x01000005,
    KEY_RETURN = 0x01000004,
    KEY_DELETE = 0x01000007,

    KEY_0 = 0x30,
    KEY_1 = 0x31,
    KEY_2 = 0x32,
    KEY_3 = 0x33,
    KEY_4 = 0x34,
    KEY_5 = 0x35,
    KEY_6 = 0x36,
    KEY_7 = 0x37,
    KEY_8 = 0x38,
    KEY_9 = 0x39,
    KEY_PLUS = 0x2b,
    KEY_MINUS = 0x2d,

    KEY_A = 0x41,
    KEY_B = 0x42,
    KEY_C = 0x43,
    KEY_D = 0x44,
    KEY_E = 0x45,
    KEY_F = 0x46,
    KEY_G = 0x47,
    KEY_H = 0x48,
    KEY_I = 0x49,
    KEY_J = 0x4a,
    KEY_K = 0x4b,
    KEY_L = 0x4c,
    KEY_M = 0x4d,
    KEY_N = 0x4e,
    KEY_O = 0x4f,
    KEY_P = 0x50,
    KEY_Q = 0x51,
    KEY_R = 0x52,
    KEY_S = 0x53,
    KEY_T = 0x54,
    KEY_U = 0x55,
    KEY_V = 0x56,
    KEY_W = 0x57,
    KEY_X = 0x58,
    KEY_Y = 0x59,
    KEY_Z = 0x5a
};

enum MouseButton
{
    // values are the same as in the Qt,
    // to make the conversion fast.
    // DON'T CHANGE them.

    NONE_BUTTON = 0x00000000,
    LEFT_BUTTON = 0x00000001,
    RIGHT_BUTTON = 0x00000002,
    MIDDLE_BUTTON = 0x00000004
};

enum KeyboardModifiers
{
    // DON'T CHANGE

    NO_MOD = 0x00000000,       // No modifier key is pressed.
    SHIFT = 0x02000000,        // A Shift key on the keyboard is pressed.
    CONTROL = 0x04000000,      // A Ctrl key on the keyboard is pressed.
    ALT = 0x08000000,          // An Alt key on the keyboard is pressed.
    META = 0x10000000,         // A Meta key on the keyboard is pressed.
    KEYPAD = 0x20000000,       // A keypad button is pressed.
    GROUP_SWITCH = 0x40000000  // X11 only. A Mode_switch key on the keyboard is pressed.
};



struct MouseEvent
{
    int x;
    int y;
    MouseButton buttons;
    MouseButton button;

    KeyboardModifiers modifiers;



    MouseEvent()
    {
        x = 0;
        y = 0;
        buttons = NONE_BUTTON;
        button = NONE_BUTTON;

        modifiers = NO_MOD;
    }

    MouseEvent(int gx, int gy, int gbutton, int gbuttons, int mods)
    {
        x = gx;
        y = gy;
        button = (MouseButton)gbutton;
        buttons = (MouseButton)gbuttons;
        modifiers = (KeyboardModifiers)mods;
    }
};

struct MWheelEvent
{
    int value;
    int x;
    int y;

    MWheelEvent()
    {
        value = 0;
        x = 0;
        y = 0;
    }

    MWheelEvent(int gvalue, int gx, int gy)
    {
        value = gvalue;
        x = gx;
        y = gy;
    }
};

struct KeyEvent
{
    Key key;

    KeyEvent() { key = KEY_NONE; }

    KeyEvent(int gkey) { key = (Key)gkey; }
};

struct ResizeEvent
{
    int new_width;
    int new_height;
    int old_width;
    int old_height;

    ResizeEvent()
    {
        new_width = 0;
        new_height = 0;
        old_width = 0;
        old_height = 0;
    }

    ResizeEvent(int wn, int hn, int wo, int ho)
    {
        new_width = wn;
        new_height = hn;
        old_width = wo;
        old_height = ho;
    }
};

}  // namespace Core
