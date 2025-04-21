#pragma once
#include <QTextStream>

#include <iostream>
#include <memory>
#include <string>
#include <format>


#define LOGGING_ENABLED

namespace Base
{
enum LOGLEVEL
{
    D_OFF = 0,
    D_FATAL = 1,
    D_ERROR = 2,
    D_WARN = 3,
    D_INFO = 4,
    D_DEBUG = 5,
    D_ALL = 6
};

LX_BASE_EXPORT void setLogLevel(LOGLEVEL);
LX_BASE_EXPORT LOGLEVEL getLogLevel();

class LX_BASE_EXPORT LastError
{
public:
    static LastError& Instance();
    LastError& setError(std::string& where, std::string& msg);
    LastError& setError(const char* where, const char* msg, ...);
    LastError& append(std::string& msg);
    std::string getError();
    std::string getErrorMsg();
    LastError() = default;

private:
    std::string m_where;
    std::string m_msg;    
};

#define LASTERROR(msg, ...) Base::LastError::Instance().setError(__FUNCTION__, msg, __VA_ARGS__)
#define CLEARLASTERROR() Base::LastError::Instance().setError("", "")




class LX_BASE_EXPORT SpdLogger
{
public:
    SpdLogger();
    ~SpdLogger();

    static SpdLogger& getInstance()
    {
        static SpdLogger instance;
        return instance;
    }

    void logDebug(const std::string& str);
    void logInfo(const std::string& str);
    void logError(const std::string& str);
    void logTrace(const std::string& str);
    void logWarn(const std::string& str);
    void logCritical(const std::string& str);
};






class LX_BASE_EXPORT ScopedLogger
{
public:
    ScopedLogger(LOGLEVEL level, const std::string& s);
    ~ScopedLogger();

    static int getIndent();

    class ScopedLoggerP;
    ScopedLoggerP* _piml;
};


class LogBaseClass
{
public:
    virtual ~LogBaseClass() = default;
    virtual LogBaseClass& space() = 0;
    virtual LogBaseClass& nospace() = 0;
    virtual LogBaseClass& maybeSpace() = 0;
    virtual LogBaseClass& operator<<(QChar t) = 0;
    virtual LogBaseClass& operator<<(bool t) = 0;
    virtual LogBaseClass& operator<<(char t) = 0;
    virtual LogBaseClass& operator<<(signed short t) = 0;
    virtual LogBaseClass& operator<<(unsigned short t) = 0;
    virtual LogBaseClass& operator<<(signed int t) = 0;
    virtual LogBaseClass& operator<<(unsigned int t) = 0;
    virtual LogBaseClass& operator<<(signed long t) = 0;
    virtual LogBaseClass& operator<<(unsigned long t) = 0;
    virtual LogBaseClass& operator<<(qint64 t) = 0;
    virtual LogBaseClass& operator<<(quint64 t) = 0;
    virtual LogBaseClass& operator<<(float t) = 0;
    virtual LogBaseClass& operator<<(double t) = 0;
    virtual LogBaseClass& operator<<(const char* t) = 0;
    virtual LogBaseClass& operator<<(const QString& t) = 0;
    virtual LogBaseClass& operator<<(const QStringRef& t) = 0;
    virtual LogBaseClass& operator<<(const QLatin1String& t) = 0;
    virtual LogBaseClass& operator<<(const QByteArray& t) = 0;
    virtual LogBaseClass& operator<<(const void* t) = 0;
    virtual LogBaseClass& operator<<(QTextStreamFunction f) = 0;
    virtual LogBaseClass& operator<<(QTextStreamManipulator m) = 0;
};

class NoDebugClass
{
public:
    NoDebugClass& operator<<(QTextStreamFunction) { return *this; }
    NoDebugClass& operator<<(QTextStreamManipulator) { return *this; }
    NoDebugClass& space() { return *this; }
    NoDebugClass& nospace() { return *this; }
    NoDebugClass& maybeSpace() { return *this; }
    NoDebugClass& quote() { return *this; }
    NoDebugClass& noquote() { return *this; }
    NoDebugClass& maybeQuote(const char = '"') { return *this; }

    template <typename T>
    NoDebugClass& operator<<(const T&)
    {
        return *this;
    }
};


class LX_BASE_EXPORT LogClass : public LogBaseClass
{
    struct Stream
    {
        Stream(QIODevice* device) : ts(device), ref(1), type(QtDebugMsg), space(true), message_output(false) {}
        Stream(QString* string) : ts(string, QIODevice::WriteOnly), ref(1), type(QtDebugMsg), space(true), message_output(false) {}
        Stream(QtMsgType t) : ts(&buffer, QIODevice::WriteOnly), ref(1), type(t), space(true), message_output(true) {}
        QTextStream ts;
        QString buffer;
        int ref;
        QtMsgType type;
        bool space;
        bool message_output;
    } * stream;

    LOGLEVEL mylevel = D_ERROR;
#if QT_VERSION >= 0x050000
    QMessageLogContext context;
#endif


public:
    LogClass(QIODevice* device) : stream(new Stream(device)) {}
    LogClass(QString* string) : stream(new Stream(string)) {}
    LogClass(LOGLEVEL level, QtMsgType t) : mylevel(level), stream(new Stream(t)) {}
    LogClass(const LogClass& o) : stream(o.stream) { ++stream->ref; }
    ~LogClass();
    
    LogClass& space()
    {
        stream->space = true;
        stream->ts << " ";
        return *this;
    }
    LogClass& nospace()
    {
        stream->space = false;
        return *this;
    }
    LogClass& maybeSpace()
    {
        if (stream->space)
            stream->ts << " ";
        return *this;
    }

    LogClass& operator<<(QChar t)
    {
        stream->ts << "\'" << t << "\'";
        return maybeSpace();
    }
    LogClass& operator<<(bool t)
    {
        stream->ts << (bool(t) ? "true" : "false");
        return maybeSpace();
    }
    LogClass& operator<<(char t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(signed short t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(unsigned short t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(signed int t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(unsigned int t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(signed long t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(unsigned long t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(qint64 t)
    {
        stream->ts << QString::number(t);
        return maybeSpace();
    }
    LogClass& operator<<(quint64 t)
    {
        stream->ts << QString::number(t);
        return maybeSpace();
    }
    LogClass& operator<<(float t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(double t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(const char* t)
    {
        stream->ts << qPrintable(t);
        return maybeSpace();
    }
    LogClass& operator<<(const QString& t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(const QStringRef& t) { return operator<<(t.toString()); }
    LogClass& operator<<(const QLatin1String& t)
    {
        stream->ts << t.latin1();
        return maybeSpace();
    }
    LogClass& operator<<(const QByteArray& t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(const void* t)
    {
        stream->ts << t;
        return maybeSpace();
    }
    LogClass& operator<<(QTextStreamFunction f)
    {
        stream->ts << f;
        return *this;
    }

    LogClass& operator<<(QTextStreamManipulator m)
    {
        stream->ts << m;
        return *this;
    }

    static bool is_activated;
};

#ifdef LOGGING_ENABLED
void LogV(LOGLEVEL level, const QString& s, va_list ap);
LX_BASE_EXPORT LogClass Log(Base::LOGLEVEL level);
LX_BASE_EXPORT LogClass Log(Base::LOGLEVEL level, const char* msg, ...);
#endif


#define LOGCOMMAND_DEBUG(x) Base::ScopedLogger _____scopedLogger(Base::D_DEBUG, x);
#define LOGCOMMAND_INFO(x) Base::ScopedLogger _____scopedLogger(Base::D_INFO, x);
#define LOGCOMMAND(x) Base::ScopedLogger _____scopedLogger(Base::D_WARN, x);
#define LOGCOMMAND_WARN(x) Base::ScopedLogger _____scopedLogger(Base::D_WARN, x);
#define cUserDebug(...) \
    if (Base::Settings::getInstance()->getDebugUser()) \
    { \
        cWarn(__VA_ARGS__); \
    }
#define LOGVAR(var) cDebug() << QString("%1 = %2").arg(#var).arg(var);

class LX_BASE_EXPORT AssertSingleton
{
public:
    static AssertSingleton& getInstance()
    {
        static AssertSingleton instance;
        // volatile int dummy{};
        return instance;
    }

    void setCallBack(std::function<bool(std::string)> f) { mCallback = f; }
    bool callCallBack(std::string s)
    {
        if (mCallback)
            return mCallback(s);
        return false;
    }

private:
    std::function<bool(std::string)> mCallback;
    AssertSingleton() = default;
    AssertSingleton(const AssertSingleton&) = delete;
    AssertSingleton& operator=(const AssertSingleton&) = delete;
};

class LX_BASE_EXPORT Logger
{
public:
    static Logger& instance();
    static void log(const char* format, ...);
    static void log(QString s);


private:
    Logger(QString path) : logFilePath(path) {}

    QString logFilePath;
};

class LX_BASE_EXPORT ScopedLog
{
public:
    ScopedLog(QString a) : m_msg(a) {}
    ~ScopedLog() { Logger::instance().log(m_msg); }
    QString m_msg;
};

}  // namespace Base

#define myLog(a) Logger::instance().writeToLog(a);
#define myLogAtFinish(a) ScopedLog(a);





/*

template <typename... Args>
void LogInfo(const std::string& fmt, const Args&... args)
{
    Base::SpdLogger::getInstance().logInfo(fmt, args...);
}

template <typename... Args>
void LogError(const std::string& fmt, const Args&... args)
{
    Base::SpdLogger::getInstance().logError(fmt, args...);
}

template <typename... Args>
void LogTrace(const std::string& fmt, const Args&... args)
{
    Base::SpdLogger::getInstance().logTrace(fmt, args...);
}

template <typename... Args>
void LogWarn(const std::string& fmt, const Args&... args)
{
    Base::SpdLogger::getInstance().logWarn(fmt, args...);
}

template <typename... Args>
void LogCritical(const std::string& fmt, const Args&... args)
{
    Base::SpdLogger::getInstance().logCritical(fmt, args...);
}
*/


#ifdef LOGGING_ENABLED

#define cAssert(condition, message) \
    do \
    { \
        if (!(condition)) \
        { \
            std::stringstream ss; \
            ss << "Assertion: `" #condition << "` --> '" << message << "' failed in \n" << __FILE__ << ":" << __LINE__ << "\n"; \
            std::cerr << ss.str(); \
            if (Base::AssertSingleton::getInstance().callCallBack(ss.str())) \
                exit(1); \
        } \
    } while (false)


LX_BASE_EXPORT void cDebuggerBreak(const char* message);
LX_BASE_EXPORT Base::LogClass cDebug();
LX_BASE_EXPORT Base::LogClass cInfo();
LX_BASE_EXPORT Base::LogClass cError();
LX_BASE_EXPORT Base::LogClass cWarn();

LX_BASE_EXPORT Base::LogClass cDebug(const QString s);
LX_BASE_EXPORT Base::LogClass cInfo(const QString s);
LX_BASE_EXPORT Base::LogClass cError(const QString s);
LX_BASE_EXPORT Base::LogClass cWarn(const QString s);

LX_BASE_EXPORT Base::LogClass cDebug(const char* msg, ...);
LX_BASE_EXPORT Base::LogClass cInfo(const char* msg, ...);
LX_BASE_EXPORT Base::LogClass cError(const char* msg, ...);
LX_BASE_EXPORT Base::LogClass cWarn(const char* msg, ...);


template <typename... Args>
void lDebug(std::string_view rt_fmt_str, Args&&... args)
{
    auto p = std::vformat(rt_fmt_str, std::make_format_args(args...));
    Base::SpdLogger::getInstance().logDebug(p);
}

template <typename... Args>
void lWarn(std::string_view rt_fmt_str, Args&&... args)
{
    auto p = std::vformat(rt_fmt_str, std::make_format_args(args...));
    Base::SpdLogger::getInstance().logWarn(p);
}

template <typename... Args>
void lError(std::string_view rt_fmt_str, Args&&... args)
{
    auto p = std::vformat(rt_fmt_str, std::make_format_args(args...));
    Base::SpdLogger::getInstance().logError(p);
}

template <typename... Args>
void lInfo(std::string_view rt_fmt_str, Args&&... args)
{
    auto p = std::vformat(rt_fmt_str, std::make_format_args(args...));
    Base::SpdLogger::getInstance().logInfo(p);
}






#else

LX_CORE_EXPORT Base::NoDebugClass noDebug();
LX_CORE_EXPORT void noDebug(const char*, ...);
LX_CORE_EXPORT void noDebug(const QString&);

#define cAssert(condition, message) \
    do \
    { \
    } while (false)
#define cDebug \
    while (false) \
    noDebug
#define cInfo \
    while (false) \
    noDebug
#define cError \
    while (false) \
    noDebug
#define cWarn \
    while (false) \
    noDebug


#endif