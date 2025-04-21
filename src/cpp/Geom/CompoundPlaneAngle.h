#pragma once

#include <vector>



namespace Geom
{
/*!
@brief A compound measure of plane angle in degrees, minutes, seconds, and optionally millionth-seconds of arc.
*/
class LX_GEOM_EXPORT CompoundPlaneAngle
{
public:
    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Constructs a CompoundPlaneAngle at 0 degrees, 0 minutes, 0 seconds
    CompoundPlaneAngle();
    /// Constructs a CompoundPlaneAngle from degrees, minutes and seconds
    CompoundPlaneAngle(int degrees, int minutes, int seconds);
    /// Constructs a CompoundPlaneAngle from degrees, minutes, seconds and millionth-seconds
    CompoundPlaneAngle(int degrees, int minutes, int seconds, int millionthSeconds);

    /// The first integer measure is the number of degrees in the range {360; -360}. Throws Base::OutOfRange if degrees are out of range.
    void setDegrees(int degrees);
    /// Get degrees
    int getDegrees() const;
    /// The second integer measure is the number of minutes in the range {60; -60}. Throws Base::OutOfRange if minutes are out of range.
    void setMinutes(int minutes);
    /// Get minutes
    int getMinutes() const;
    /// The third integer measure is the number of seconds in the range {60; -60}. Throws Base::OutOfRange if seconds are out of range.
    void setSeconds(int seconds);
    /// Get seconds
    int getSeconds() const;
    /// The optional fourth integer measure is the number of millionth-seconds in the range {1 000 000; -1 000 000}. Throws Base::OutOfRange if
    /// millionth-seconds are out of range.
    void setMillionthSeconds(int millionthSeconds);
    /// Get third integer
    int getMillionthSeconds() const;
    /// Get values
    std::vector<int> getValues() const;

    bool operator==(const Geom::CompoundPlaneAngle& other) const;
    bool operator!=(const Geom::CompoundPlaneAngle& other) const;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


private:
    int _degrees;
    int _minutes;
    int _seconds;
    int _millionthSeconds;
};
}  // namespace Geom
