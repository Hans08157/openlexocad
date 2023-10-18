#pragma once
#include <string>


/* MACROS FOR THROWING EXCEPTIONS */

/// the macros do NOT mark any message for translation
/// If you want to mark text for translation, use the QT_TRANSLATE_NOOP macro
/// with the context "Exceptions" and the right throwing macro from below (the one ending in T)
/// example:
/// THROWMT(Base::ValueError,QT_TRANSLATE_NOOP("Exceptions","The multiplicity cannot be increased beyond the degree of the B-Spline."));
///
/// N.B.: The QT_TRANSLATE_NOOP macro won't translate your string. It will just allow lupdate to identify that string for translation so that
/// if you ask for a translation (and the translator have provided one) at that time it gets translated (e.g. in the UI before showing the message
/// of the exception).

#ifdef _MSC_VER

#define THROW(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        throw myexcp; \
    }
#define THROWM(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        throw myexcp; \
    }
#define THROWMF_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        throw myexcp; \
    }

#define THROWT(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMT(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMFT_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __FUNCSIG__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }

#elif defined(__GNUC__)

#define THROW(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        throw myexcp; \
    }
#define THROWM(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        throw myexcp; \
    }
#define THROWMF_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        throw myexcp; \
    }

#define THROWT(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMT(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMFT_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __PRETTY_FUNCTION__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }

#else

#define THROW(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        throw myexcp; \
    }
#define THROWM(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        throw myexcp; \
    }
#define THROWMF_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        throw myexcp; \
    }

#define THROWT(exception) \
    { \
        exception myexcp; \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMT(exception, message) \
    { \
        exception myexcp(message); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }
#define THROWMFT_FILEEXCEPTION(message, filenameorfileinfo) \
    { \
        FileException myexcp(message, filenameorfileinfo); \
        myexcp.setDebugInformation(__FILE__, __LINE__, __func__); \
        myexcp.setTranslatable(true); \
        throw myexcp; \
    }


#endif

#define FC_THROWM(_exception, _msg) \
    do \
    { \
        std::stringstream ss; \
        ss << _msg; \
        THROWM(_exception, ss.str().c_str()); \
    } while (0)

#define THROW_CON_ERR_IF(_condition_, _msg_) \
    if (_condition_) \
        throw Base::ConstructionError(_msg_);

#define THROW_FAIL_NDONE_IF(_condition_, _msg_) \
    if (_condition_) \
        throw Base::FailedNotDone(_msg_);

namespace Base
{
class LX_BASE_EXPORT Exception
{
public:
    Exception(const char* sMessage, const char* detail);
    Exception(void);
    Exception(const Exception& inst);
    virtual ~Exception() throw() {}

    Exception& operator=(const Exception& inst);

    virtual const char* what(void) const throw();
    virtual const char* detail(void) const throw();

    void ReportException(void) const;

    inline void SetMessage(const char* sMessage);

    inline std::string getFile() const;
    inline int getLine() const;
    inline std::string getFunction() const;
    inline bool getTranslatable() const;
    inline bool getReported() const { return _isReported; }

    /// setter methods for including debug information
    /// intended to use via macro for autofilling of debugging information
    inline void setDebugInformation(const std::string& file, const int line, const std::string& function);
    inline void setTranslatable(bool translatable);
    inline void setReported(bool reported) { _isReported = reported; }

protected:
#ifdef _MSC_VER
#pragma warning(disable : 4251)
#endif
    std::string _sErrMsg;
    std::string _sErrDetail;
    std::string _file{ "" };
    int _line{ -1 };
    std::string _function{ "" };
    bool _isTranslatable{ false };
    mutable bool _isReported{ false };
};


/**
 * The AbortException is thrown if a pending operation was aborted.
 * @author Werner Mayer
 */
class LX_BASE_EXPORT AbortException : public Exception
{
public:
    /// Construction
    AbortException(const char* sMessage);
    /// Construction
    AbortException();
    /// Construction
    AbortException(const AbortException& inst);
    /// Destruction
    virtual ~AbortException() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The MemoryException is thrown if not enough memory can be allocated.
 * @author Werner Mayer
 */
class LX_BASE_EXPORT MemoryException : public Exception
{
public:
    /// Construction
    MemoryException();
    /// Construction
    MemoryException(const MemoryException& inst);
    /// Destruction
    virtual ~MemoryException() throw() {}
};


inline void Exception::SetMessage(const char* sMessage)
{
    _sErrMsg = sMessage;
}

/**
 * The ConstructionError is thrown if the construction
 * of a geometry fails
 */
class LX_BASE_EXPORT ConstructionError : public Exception
{
public:
    /// Construction
    ConstructionError(const char* sMessage);
    /// Construction
    ConstructionError();
    /// Construction
    ConstructionError(const ConstructionError& inst);
    /// Destruction
    virtual ~ConstructionError() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The FailedNotDone is thrown if an algorithm failed
 */
class LX_BASE_EXPORT FailedNotDone : public Exception
{
public:
    /// Construction
    FailedNotDone(const char* sMessage);
    /// Construction
    FailedNotDone();
    /// Construction
    FailedNotDone(const FailedNotDone& inst);
    /// Destruction
    virtual ~FailedNotDone() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The ItemNotFound is thrown if an item was not found in a container
 */
class LX_BASE_EXPORT ItemNotFound : public Exception
{
public:
    /// Construction
    ItemNotFound(const char* sMessage);
    /// Construction
    ItemNotFound();
    /// Construction
    ItemNotFound(const ItemNotFound& inst);
    /// Destruction
    virtual ~ItemNotFound() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The OutOfRange is thrown if an algorithm failed
 */
class LX_BASE_EXPORT OutOfRange : public Exception
{
public:
    /// Construction
    OutOfRange(const char* sMessage);
    /// Construction
    OutOfRange();
    /// Construction
    OutOfRange(const OutOfRange& inst);
    /// Destruction
    virtual ~OutOfRange() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The OutOfRange is thrown if an algorithm failed
 */
class LX_BASE_EXPORT NotaNumber : public Exception
{
public:
    /// Construction
    NotaNumber(const char* sMessage);
    /// Construction
    NotaNumber();
    /// Construction
    NotaNumber(const NotaNumber& inst);
    /// Destruction
    virtual ~NotaNumber() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The FailedNotDone is thrown if an algorithm failed
 */
class LX_BASE_EXPORT FileException : public Exception
{
public:
    /// Construction
    FileException(const char* sMessage);
    /// Construction
    FileException();
    /// Construction
    FileException(const FileException& inst);
    /// Destruction
    virtual ~FileException() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The VectorWithNullMagnitude is thrown if a vector has a length of 0
 */
class LX_BASE_EXPORT VectorWithNullMagnitude : public Exception
{
public:
    /// Construction
    VectorWithNullMagnitude(const char* sMessage);
    /// Construction
    VectorWithNullMagnitude();
    /// Construction
    VectorWithNullMagnitude(const VectorWithNullMagnitude& inst);
    /// Destruction
    virtual ~VectorWithNullMagnitude() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

/**
 * The BadArguments is thrown if bad arguments are passed	to a function
 */
class LX_BASE_EXPORT BadArguments : public Exception
{
public:
    /// Construction
    BadArguments(const char* sMessage);
    /// Construction
    BadArguments();
    /// Construction
    BadArguments(const BadArguments& inst);
    /// Destruction
    virtual ~BadArguments() throw() {}
    /// Description of the exception
    virtual const char* what() const throw();
};

class LX_BASE_EXPORT GuidInUseException : public Base::Exception
{
public:
    GuidInUseException() { _sErrMsg = "GUID in use"; }

    GuidInUseException(const char* sMessage) : Base::Exception(sMessage, "") {}
};



class LX_BASE_EXPORT RuntimeError : public Base::Exception
{
public:
    /// Construction
    RuntimeError();
    RuntimeError(const char* sMessage);
    RuntimeError(const std::string& sMessage);
    /// Destruction
    virtual ~RuntimeError() throw() {}

};

class LX_BASE_EXPORT ValueError : public Base::Exception
{
public:
    /// Construction
    ValueError();
    ValueError(const char* sMessage);
    ValueError(const std::string& sMessage);
    /// Destruction
    virtual ~ValueError() throw() {}
};

class LX_BASE_EXPORT CADKernelError : public Base::Exception
{
public:
    /// Construction
    CADKernelError();
    CADKernelError(const char* sMessage);
    CADKernelError(const std::string& sMessage);
    /// Destruction
    virtual ~CADKernelError() throw() {}
};

class LX_BASE_EXPORT TypeError : public Exception
{
public:
    /// Construction
    TypeError();
    TypeError(const char* sMessage);
    TypeError(const std::string& sMessage);
    /// Destruction
    virtual ~TypeError() throw() {}
};

class LX_BASE_EXPORT NotImplementedError : public Exception
{
public:
    /// Construction
    NotImplementedError();
    NotImplementedError(const char* sMessage);
    NotImplementedError(const std::string& sMessage);
    /// Destruction
    virtual ~NotImplementedError() throw() {}
};


class LX_BASE_EXPORT DivisionByZeroError : public Exception
{
public:
    /// Construction
    DivisionByZeroError();
    DivisionByZeroError(const char* sMessage);
    DivisionByZeroError(const std::string& sMessage);
    /// Destruction
    virtual ~DivisionByZeroError() throw() {}
};

}  // namespace Base

#if !defined No_Exception && !defined No_Standard_OutOfRange
#define OutOfRange_Raise_if(CONDITION, MESSAGE) \
    if (CONDITION) \
        throw Base::OutOfRange(MESSAGE);
#else
#define OutOfRange_Raise_if(CONDITION, MESSAGE)
#endif

#if !defined No_Exception && !defined No_Standard_ConstructionError
#define ConstructionError_Raise_if(CONDITION, MESSAGE) \
    if (CONDITION) \
        throw Base::ConstructionError(MESSAGE);
#else
#define ConstructionError_Raise_if(CONDITION, MESSAGE)
#endif

#if !defined No_Exception && !defined No_gp_VectorWithNullMagnitude
#define VectorWithNullMagnitude_Raise_if(CONDITION, MESSAGE) \
    if (CONDITION) \
        throw Base::VectorWithNullMagnitude(MESSAGE);
#else
#define VectorWithNullMagnitude_Raise_if(CONDITION, MESSAGE)
#endif

#if !defined No_Exception
#define NotaNumber_if(CONDITION, MESSAGE) \
    if (CONDITION) \
        throw Base::NotaNumber(MESSAGE);
#else
#define NotaNumber_if(CONDITION, MESSAGE)
#endif
