#pragma once
#include <functional>
#include <map>
#include <set>
#include <Base/String.h>
#include <QString>
#include <QColor>

namespace Base
{
class LX_BASE_EXPORT ProgressInfo
{
public:
    enum ProgressObserverInfoID
    {
        ACIS_PROGRESS,
    };


    ProgressInfo(ProgressObserverInfoID id, std::string de, int percent) : m_id(id), m_desc(de), m_percent(percent) {}


    int m_percent;
    std::string m_desc;
    ProgressObserverInfoID m_id;
};

class LX_BASE_EXPORT ProgressObserver
{
public:
    ProgressObserver() = default;
    virtual ~ProgressObserver() = default;
    virtual void notify(ProgressInfo info) = 0;
};


typedef std::function<void(ProgressInfo)> ProgressHandler;

class LX_BASE_EXPORT Progress
{
public:
    void notify(ProgressInfo info)
    {
        for (auto o : m_observer)
            o->notify(info);
        for (auto o : m_handlers)
            o.second(info);
    }

    std::set<ProgressObserver*> m_observer;
    std::map<std::string, ProgressHandler> m_handlers;

    void attach(std::string key, ProgressHandler hd) { m_handlers[key] = hd; }

    void attach(ProgressObserver* o) { m_observer.insert(o); }

    void detach(ProgressObserver* o) { m_observer.erase(o); }

    void detach(std::string key)
    {
        auto it = m_handlers.find(key);
        if (it != m_handlers.end())
            m_handlers.erase(it);
    }

    void detachAll()
    {
        m_observer.clear();
        m_handlers.clear();
    }
};

LX_BASE_EXPORT Progress& ProgressSingleton();


typedef std::function<void(int)> SequencerCallBackFunc;
LX_BASE_EXPORT void SequencerCallBackFunc_Default(int);


class LX_BASE_EXPORT SequencerBase
{
public:
    static SequencerBase& instance(void);
    static void setInstance(SequencerBase* p);

    static void setFactory(std::function<Base::SequencerBase*()> func);
    static Base::SequencerBase* create(bool callStopInDestructor = true);

    virtual bool startbusy(const std::string& caption, const std::string& message, bool forceShow);
    virtual bool startbusy(const Base::String& caption, const Base::String& message, bool forceShow);
    virtual bool start(const std::string& caption, const std::string& message, int steps, int from, int to, bool /*forceShow*/);
    virtual bool start(const Base::String& caption, const Base::String& message, int steps, int from, int to, bool /*forceShow*/);
    virtual void stop();
    virtual void setStep(int step, bool canAbort = true);
    virtual void setStepContinuous(int step, bool canAbort = true);
    virtual void setMessage(const std::string& message);
    virtual void setMessage(const Base::String& message);
    virtual void setMinimumDuration(int milliseconds);
    virtual int  getMinimumDuration() const;
    virtual void busy1();
    virtual void busy10();
    virtual void busy100();
    virtual void busy1000();
    virtual void busy10000();


    virtual Base::String getMessage();
    virtual void setHidden(bool hidden);
    virtual void show(bool onoff);

    virtual void move(){};


    

    /// Throws Base::AbortException
    void abort();

    bool isRunning() const;
    void setRunning(bool b);
    int getCurrentStep() const;
    void setCurrentStep(int s);
    int getSteps() const;
    void setSteps(int steps);
    void setNextBlock(int from, int to);
    void getNextBlock(int& from, int& to);
    void setThisBlock(int from, int to);
    int getFrom();
    int getTo();
    bool canAbort() const;
    void setCanAbort(bool p);


    /// setters/getters for indiate if the Lexocad window mode is NO_WINDOW
    void setNoWindowModeInfoFlag(bool aValue);
    bool getNoWindowModeInfoFlag();

    /// enable writing sequencer progress to std::cout, disabled automatically when stop method of this class is called
    bool setWriteStepToStdout(bool aEnabled, std::string aOutputStepPrefixString);
    bool isWriteStepToStdout() const;
    std::string getWriteStepToStdcoutPrefixString() const;

    virtual void pushState();
    virtual void popState();

    virtual ~SequencerBase();

protected:
    SequencerBase();
    bool _callStopInDestructor = false;

private:
    SequencerBase(const SequencerBase&){};
    static SequencerBase* _instance;
    static std::function<Base::SequencerBase*()> _factory;

    struct SequencerBaseData
    {
        bool _isRunning = false;
        bool _canAbort = true;
        int _currentStep = 0;
        int _steps = 0;

        int _thisBlockFrom = 0;
        int _thisBlockTo = 0;
        int _nextBlockFrom = 0;
        int _nextBlockTo = 100;
        int _minimumDuration = 2000;
        Base::String _message;

        bool _windowModeActiveFlag = false;
        bool _writeStepToStdout = false;
        std::string _writeStepToStdcoutPrefixString;
    } internalData;

    std::vector<SequencerBaseData> sequencerBaseDataStack;

};



/// Singleton getter of the Sequencer
inline LX_BASE_EXPORT Base::SequencerBase& Sequencer(void)
{
    return Base::SequencerBase::instance();
}

class LX_BASE_EXPORT WaitingSpinner
{
public:
    static WaitingSpinner& instance(void);
    static void setInstance(WaitingSpinner* p);

public:
    virtual void start();
    virtual void stop();
    virtual void setText(const Base::String& txt);
    virtual void setColor(QColor c);

public:
private:
    static WaitingSpinner* _instance;
};

class LX_BASE_EXPORT ScopedWaitingSpinner
{
public:
    ScopedWaitingSpinner() { Base::WaitingSpinner::instance().start(); }
    ScopedWaitingSpinner(QString txt)
    {
        Base::WaitingSpinner::instance().setText(txt);
        Base::WaitingSpinner::instance().start();
    }
    ScopedWaitingSpinner(QString txt, QColor c)
    {
        Base::WaitingSpinner::instance().setText(txt);
        Base::WaitingSpinner::instance().setColor(c);
        Base::WaitingSpinner::instance().start();
    }
    ~ScopedWaitingSpinner() { Base::WaitingSpinner::instance().stop(); }
};


}  // namespace Base
