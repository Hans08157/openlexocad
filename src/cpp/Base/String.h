#pragma once
#include <string>



class QString;
namespace App
{
class StringTool;
}

namespace Base
{
/*!
@brief A Utf-16 (windows) or ucs4 (unix) encoded string class
*/
class LX_BASE_EXPORT String
{
public:
    friend class StringTool;
    friend class ::App::StringTool;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    /// Constructs an empty string
    String();
    /// Constructs a string from a std::wstring
    String(const std::wstring& s);
    /// Constructs a string from a QString
    String(const QString& s);
    /// Constructs a string from an array of wchar_t
    String(const wchar_t* s);
    /// Constructs a string from an array of wchar_t
    // String::String(unsigned short const * s);
    /// Copy constructor
    String(const Base::String& s);

    bool operator==(const Base::String& other) const;

    bool operator!=(const Base::String& other) const;
    bool operator<(const Base::String& other) const;
    bool operator>(const Base::String& other) const;
    Base::String& operator=(const Base::String& rhs);
    Base::String operator+(const Base::String& other) const;
    Base::String& operator+=(const Base::String& other);

    inline int size() const;
    inline int lenght() const;
    inline bool empty() const;
    // Returns a newly constructed Base::String object with its value initialized to a copy of a substring of this object.
    Base::String substr(size_t pos = 0, size_t len = std::string::npos) const;

    /// Returns Base::String as a std::wstring
    std::wstring toWString() const;
    /// Returns wchar_t array
    const wchar_t* c_str() const { return _utf16string.c_str(); }

    bool isEqual(const Base::String& other) const;

    // Refactoring, for the first, let do the compiler the work
    // inline operator std::string() const ;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    bool startsWith(const Base::String& other) const;
    bool contains(const Base::String& other) const;

    friend LX_BASE_EXPORT std::ostream& operator<<(std::ostream& o, const Base::String& s);

private:
    // Remark: Using wstring on windows OS is ok, since it uses 2bytes/UTF-16 only.
    // On Unix we should consider using a different string since it uses 4bytes/UCS-4.
    std::wstring _utf16string;
};
LX_BASE_EXPORT std::ostream& operator<<(std::ostream& o, const Base::String& s);
}  // namespace Base
