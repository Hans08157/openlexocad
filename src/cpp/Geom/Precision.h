
/**
 *
 * @author Tomáš Pafèo
 */

#pragma once
#include <qmath.h>
#include <limits> 



#define L_RES 1.e-6
#define A_RES 1.e-10


namespace Geom
{
class Precision
{
public:
    // Compare 2 points, samePoint etc, same as acsi: SPAresabs
    static constexpr double linear_Resolution() { return L_RES; }
    // minimal angle, parallel, same as acis: SPAresnor
    static constexpr double angle_Resolution() { return A_RES; }

    static constexpr double tolerance() { return L_RES; }

    static constexpr double confusion() { return L_RES; }

    static constexpr double angular() { return A_RES; }



    static constexpr double infinite() { return std::numeric_limits<double>::infinity(); }

    /// Shapes with bounding boxes larger than this value
    /// are considered 'infinite'.
    static constexpr double shape_infinite() { return 1E06; }

    // Note:
    // If you want to use the std::numeric_limits min/max feature,
    // you need to undefine the symbols named min and max first.
    // These macros probably come from the windows.h.
    // (tp) 20111213

    static constexpr double min_double()
    {
        //				return std::numeric_limits<double>::min();
        return DBL_MIN;
    }

    static constexpr double max_double()
    {
        //				return std::numeric_limits<double>::max();
        return DBL_MAX;
    }

    /**
     * Returns the minimum positive real e such that 1.0 + e is not equal to 1.0
     *
     */
    static constexpr double epsilon() { return std::numeric_limits<double>::epsilon(); }

    /**
     * This is an "adaptive" epsilon - the minimum real e such that
     * v + e is not equal to the v.
     *
     */
    static constexpr double epsilon(double v)
    {
        if (v >= 0.0)
            return std::nextafter(v, max_double()) - v;
        else
            return v - std::nextafter(v, min_double());
    }
};


}  // namespace Geom
