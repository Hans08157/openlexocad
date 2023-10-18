#pragma once

namespace Base
{
struct LX_BASE_EXPORT Int
{
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    int value;

    // Semi-regular
    explicit Int(int x) : value(x) {}
    explicit Int(const Int& x) : value(x.value) {}
    Int() {}
    ~Int() {}
    Int& operator=(const Int& x)
    {
        value = x.value;
        return *this;
    }

    // Regular
    friend bool operator==(const Int& x, const Int& y) { return x.value == y.value; }

    friend bool operator!=(const Int& x, const Int& y) { return !(x == y); }

    // TotallyOrdered
    friend bool operator<(const Int& x, const Int& y) { return x < y; }

    friend bool operator>(const Int& x, const Int& y) { return y < x; }

    friend bool operator<=(const Int& x, const Int& y) { return !(y < x); }

    friend bool operator>=(const Int& x, const Int& y) { return !(x < y); }


    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////
};
}  // namespace Base
