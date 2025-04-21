#pragma once
#include <Base/String.h>
#include <iomanip>
#include <sstream>
#include <QCollator>
#include <QString>        // for QString

class QUuid;

namespace Base
{
class GlobalId;
class LX_BASE_EXPORT StringTool
{
public:
    template <typename T>
    static std::string toStlString(const T& t)
    {
        std::stringstream ss;
        ss << t;
        return ss.str();
    }

    template <typename T>
    static std::string toStlString(const T& t, int precision)
    {
        std::stringstream ss;
        ss.precision(precision);
        ss << t;
        return ss.str();
    }

    template <typename T>
    static std::string toStlString(const T& t, int fieldWidth, char fillChar)
    {
        std::stringstream ss;
        ss << std::setfill(fillChar) << std::setw(fieldWidth) << t;
        return ss.str();
    }

    static std::string toStlString(const bool& b, int fieldWidth, char fillChar)
    {
        std::string str;
        if (b)
            str = std::string("true");
        else
            str = std::string("false");

        std::stringstream ss;
        ss << std::setfill(fillChar) << std::setw(fieldWidth) << str;
        return ss.str();
    }

    static std::string toStlString(const bool& b) { return b ? "true" : "false"; }

    static std::string toStlString(const QString& str);

    template <typename T>
    static Base::String toString(const T& t)
    {
        std::wstringstream ss;
        ss << t;
        return ss.str();
    }

    template <typename T>
    static Base::String toString(const T& t, int precision)
    {
        std::wstringstream ss;
        ss.precision(precision);
        ss << t;
        return ss.str();
    }

    template <typename T>
    static Base::String toString(const T& t, int fieldWidth, wchar_t fillChar)
    {
        std::wstringstream ss;
        ss << std::setfill(fillChar) << std::setw(fieldWidth) << t;
        return ss.str();
    }


    static Base::String toString(const bool& b, int fieldWidth, wchar_t fillChar)
    {
        Base::String str;
        if (b)
            str = L"true";
        else
            str = L"false";

        std::wstringstream ss;
        ss << std::setfill(fillChar) << std::setw(fieldWidth) << str._utf16string;
        return ss.str();
    }


    static Base::String toString(const bool& b)
    {
        if (b)
            return L"true";
        else
            return L"false";
    }

    struct CmpByCollator
    {
        CmpByCollator() { collator.setNumericMode(true); }
        bool operator()(const QString& a, const QString& b) const
        {
            return collator.compare(a, b) < 0;
        }

    private:
        QCollator collator;
    };

    /// Returns a copy of string which is converted to upper case
    static std::string toUpper(const std::string& str);
    /// Returns a copy of string which is converted to lower case
    static std::string toLower(const std::string& str);
    /// Returns a copy of string which is converted to upper case
    static Base::String toUpper(const Base::String& str);
    /// Returns a copy of string which is converted to lower case
    static Base::String toLower(const Base::String& str);

    /// Returns a copy of string with leading spaces removed.
    static std::string trimLeft(const std::string& str);
    /// Returns a copy of string with trailing spaces removed.
    static std::string trimRight(const std::string& str);
    /// Returns a copy of string with leading and trailing spaces removed.
    static std::string trim(const std::string& str);
    /// Returns a copy of string with leading spaces removed.
    static Base::String trimLeft(const Base::String& str);
    /// Returns a copy of string with trailing spaces removed.
    static Base::String trimRight(const Base::String& str);
    /// Returns a copy of string with leading and trailing spaces removed.
    static Base::String trim(const Base::String& str);

    /// Returns a copy of the string. Replaces given text with something else.
    static std::string replace(const std::string& str, const std::string& src, const std::string& rpl);
    /// Returns a copy of the string. Replaces given text with something else.
    static Base::String replace(const Base::String& str, const Base::String& src, const Base::String& rpl);

    /// Checks if a string contains characters.
    static bool isEmpty(const std::string& str);
    /// Checks if a string contains characters.
    static bool isEmpty(const Base::String& str);

    /// Converts the string representation of a bool to a boolean value. ok = 'false' if conversion fails
    static bool toBool(const std::string& str, bool* ok = 0);
    /// Converts the string representation of a bool to a boolean value. ok = 'false' if conversion fails
    static bool toBool(const char* str, bool* ok = 0);
    /// Converts the string representation of a bool to a boolean value. ok = 'false' if conversion fails
    static bool toBool(const Base::String& str, bool* ok = 0);
    /// Converts the string representation of a double to a double value. ok = 'false' if conversion fails
    static double toDouble(const std::string& str, bool* ok = 0);
    /// Converts the string representation of a double to a double value. ok = 'false' if conversion fails
    static double toDouble(const char* str, bool* ok = 0);
    /// Converts the string representation of a double to a double value. ok = 'false' if conversion fails
    static double toDouble(const Base::String& str, bool* ok = 0);
    /// Converts the string representation of a float to a float value. ok = 'false' if conversion fails
    static float toFloat(const std::string& str, bool* ok = 0);
    /// Converts the string representation of an int to an int value. ok = 'false' if conversion fails
    static uint8_t toUInt8(const std::string& str, bool* ok);
    static uint8_t toUInt8(const Base::String& str, bool* ok);
    static uint32_t toUInt32(const std::string& str, bool* ok);
    static uint32_t toUInt32(const Base::String& str, bool* ok);
    static uint64_t toUInt64(const std::string& str, bool* ok);
    static uint64_t toUInt64(const Base::String& str, bool* ok);
    static int toInt(const std::string& str, bool* ok = 0);
    static int toInt(const Base::String& str, bool* ok = 0);
    /// Converts the string representation of a char to a char value. ok = 'false' if conversion fails
    static char toChar(const std::string& str, bool* ok = 0);
    /// Converts a UTF-8 encoded string to a UTF-16 encoded string. Throws std::exception on failure.
    static Base::String toUtf16(const std::string& utf8string);
    /// Converts a UTF-16 encoded string to a UTF-8 encoded string. Throws std::exception on failure.
    static std::string toUtf8(const Base::String& widestring);
    /// Returns Base::String as a std::wstring
    static std::wstring toWString(const Base::String& str);
    /// Converts a std::string to a Base::String
    static Base::String toString(const std::string& str);
    static std::string toStlString(const Base::String& str);


    /// Replaces all characters from the string which are not letters or numbers with a '_'
    static std::string toLegal(const std::string& str);
    /// Creates a compressed GUID string. This version uses a number system with base 64 to obtain a string with 22 characters
    static std::string createGuidString();
    /// Creates a QUuid from an IFC GUID (base 64) string
    static bool toUuid(const std::string& ifcguid, QUuid& uuid);
    /// Create a GUID string (p.e. {53FD4419-39F9-4211-AD37-29DA1D3E9AF8} ) from base64 string
    static bool toGUID(const std::string& ifcguid, std::string& guid);
    /// Create a IFCGUID string (p.e. 10YjwXGv9FPhDS3ghximXO ) from a GUID string
    static bool toBase64String(const std::string& in, std::string& out);
    /// Create a IFCGUID string (p.e. 10YjwXGv9FPhDS3ghximXO ) from a QUuid
    static bool toBase64String(const QUuid& in, std::string& out);
    /// Create a IFCGUID string (p.e. 10YjwXGv9FPhDS3ghximXO ) from a Base::GlobalId
    static bool toBase64String(const Base::GlobalId& in, Base::String& out);
    /// Checks if the base64 string was generated from a valid GUID 
    static bool isValidIfcBase64String(const std::string& ifcguid);
    /// Converts a Base::String to a QString
    static QString toQString(const Base::String& str);
    /// Converts a QString to a Base::String
    static Base::String toString(const QString& str);

    static std::string toMultiByteString(const Base::String& str);
};


}  // namespace Base