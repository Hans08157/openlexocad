#pragma once
#include <sys/timeb.h>
#include <string>

namespace Base
{
class LX_BASE_EXPORT TimeInfo
{
public:
    TimeInfo();

    /// sets the object to the actual system time
    void setToActual(void);
    uint64_t getSeconds(void) const;
    unsigned short getMiliseconds(void) const;

    void operator=(const TimeInfo& time);
    bool operator==(const TimeInfo& time) const;
    bool operator!=(const TimeInfo& time) const;

    bool operator<(const TimeInfo& time) const;
    bool operator<=(const TimeInfo& time) const;
    bool operator>=(const TimeInfo& time) const;
    bool operator>(const TimeInfo& time) const;

    static const char* currentDateTimeString();
    static std::string diffTime(const TimeInfo& timeStart, const TimeInfo& timeEnd = TimeInfo());
    static float diffTimeF(const TimeInfo& timeStart, const TimeInfo& timeEnd = TimeInfo());
    bool isNull() const;
    static TimeInfo null();

protected:
    struct _timeb timebuffer;
};


inline bool TimeInfo::operator!=(const TimeInfo& time) const
{
    return (timebuffer.time != time.timebuffer.time || timebuffer.millitm != time.timebuffer.millitm);
}

inline void TimeInfo::operator=(const TimeInfo& time)
{
    timebuffer = time.timebuffer;
}

inline bool TimeInfo::operator==(const TimeInfo& time) const
{
    return (timebuffer.time == time.timebuffer.time && timebuffer.millitm == time.timebuffer.millitm);
}

inline bool TimeInfo::operator<(const TimeInfo& time) const
{
    if (timebuffer.time == time.timebuffer.time)
        return timebuffer.millitm < time.timebuffer.millitm;
    else
        return timebuffer.time < time.timebuffer.time;
    //  return (timebuffer.time < time.timebuffer.time && timebuffer.millitm < time.timebuffer.millitm);
}

inline bool TimeInfo::operator<=(const TimeInfo& time) const
{
    if (timebuffer.time == time.timebuffer.time)
        return timebuffer.millitm <= time.timebuffer.millitm;
    else
        return timebuffer.time <= time.timebuffer.time;
    //  return (timebuffer.time <= time.timebuffer.time && timebuffer.millitm <= time.timebuffer.millitm);
}

inline bool TimeInfo::operator>=(const TimeInfo& time) const
{
    if (timebuffer.time == time.timebuffer.time)
        return timebuffer.millitm >= time.timebuffer.millitm;
    else
        return timebuffer.time >= time.timebuffer.time;
    //  return (timebuffer.time >= time.timebuffer.time && timebuffer.millitm >= time.timebuffer.millitm);
}

inline bool TimeInfo::operator>(const TimeInfo& time) const
{
    if (timebuffer.time == time.timebuffer.time)
        return timebuffer.millitm > time.timebuffer.millitm;
    else
        return timebuffer.time > time.timebuffer.time;
    //  return (timebuffer.time > time.timebuffer.time && timebuffer.millitm > time.timebuffer.millitm);
}



}  // namespace Base
