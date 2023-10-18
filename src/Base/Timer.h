#pragma once
#include <map>
#include <set>
#include <string>


#define PP_CAT(a, b) PP_CAT_I(a, b)
#define PP_CAT_I(a, b) PP_CAT_II(~, a##b)
#define PP_CAT_II(p, res) res

#define PP_UNIQUE_NAME(base) PP_CAT(base, __COUNTER__)

#define PROFILECLEAR \
    { \
        Base::Timer::clearAll(); \
    }
#define PROFILEENABLE(a) \
    { \
        Base::Timer::enable(a); \
    }
#define PROFILESTART(a) \
    { \
        Base::Timer::profileStart(a); \
    }
#define PROFILESTOP(a) \
    { \
        Base::Timer::profileStop(a); \
    }
#define PROFILESCOPED(a) Base::scopedProfile PP_UNIQUE_NAME(scopedProfile__)(a);


namespace Base
{
#if defined(_WIN32) || defined(__WIN32__) || defined(WIN32)

class LX_BASE_EXPORT timerIFace
{
public:
    virtual void resetTotal() = 0;
    virtual void reset() = 0;
    virtual double elapsedMS() = 0;
    virtual double elapsed() const = 0;
    virtual double start() = 0;
    virtual void restart() = 0;
    virtual double stop() = 0;
    virtual double totalSeconds() = 0;
    virtual double totalMS() = 0;
    virtual long count() = 0;
    virtual std::string getName() = 0;
    virtual timerIFace* getParent() = 0;
    virtual void setParent(timerIFace*) = 0;
    virtual void addChild(timerIFace*) = 0;
    virtual std::set<timerIFace*> getChildren() = 0;
};

class LX_BASE_EXPORT timer_dummy : public timerIFace
{
public:
    timer_dummy(){};
    void resetTotal(){};
    void reset(){};
    double elapsedMS() { return 0.0; };
    double elapsed() const { return 0.0; };
    double start() { return 0.0; };
    void restart(){};
    double stop() { return 0.0; };
    double totalSeconds() { return 0.0; };
    double totalMS() { return 0.0; };
    long count() { return 0; };
    std::string getName() { return std::string(); };
    timerIFace* getParent() { return 0; };
    void setParent(timerIFace*){};
    void addChild(timerIFace*){};
    std::set<timerIFace*> getChildren() { return std::set<timerIFace*>(); };
};

class TimerP;

class LX_BASE_EXPORT Timer : public timerIFace
{
public:
    Timer();
    Timer(std::string n);
    ~Timer();
    void resetTotal();
    void reset();
    double elapsedMS();
    double elapsed() const;
    double start();
    void restart();
    double stop();
    double totalSeconds();
    double totalMS();
    long count();
    double createdTime();
    std::string getName() { return _name; };
    void setParent(timerIFace*);
    timerIFace* getParent();
    ;

    void addChild(timerIFace* c) { _children.insert(c); };
    std::set<timerIFace*> getChildren() { return _children; };

    static timerIFace* getTimer(std::string name);
    static void stopTimer(std::string name);
    static std::map<std::string, timerIFace*> getTimerMap();
    static void setCurrent(timerIFace* p);
    static timerIFace* getCurrent();

    static void clearAll();
    double startTiming();
    static std::map<void*, double> TimeStorage;

    static void enable(bool v);
    static bool isEnabled();


    static void profileStart(const char* a);
    static void profileStop(const char* a);

    static void printTimer(const char* header);



private:
    TimerP* _pimpl;
    double _totalseconds;
    long _count;
    std::string _name;
    timerIFace* _parentTimer = 0;
    std::set<timerIFace*> _children;
    static timerIFace* _currentTimer;
    static bool _enabled;
    static std::map<std::string, timerIFace*> _timerMap;
};

static Base::timer_dummy my_timer_dummy;
static Base::timer_dummy* my_timer_dummy_ptr = &my_timer_dummy;

#else

class LX_BASE_EXPORT timer
{
    clock_t _start_time;

public:
    timer() { _start_time = clock(); }
    void restart() { _start_time = clock(); }
    double elapsed() const { return double(clock() - _start_time) / CLOCKS_PER_SEC; }
};

#endif


class LX_BASE_EXPORT scopedProfile
{
public:
    scopedProfile(const char* a) : m_name(a) { PROFILESTART(a); }
    ~scopedProfile() { PROFILESTOP(m_name.c_str()); }

    std::string m_name;
};


}  // namespace Base