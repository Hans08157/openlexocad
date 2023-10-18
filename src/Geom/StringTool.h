#pragma once

#include <Base/String.h>
#include <Geom/Dir.h>
#include <Geom/Pnt.h>
#include <Geom/Vec.h>

#include <iomanip>
#include <sstream>

namespace Geom
{
class LX_GEOM_EXPORT StringTool
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



    template <>
    static std::string toStlString<Geom::Pnt>(const Geom::Pnt& p, int precision)
    {
        std::stringstream ss;
        ss.precision(precision);
        ss << "x: " << p.x() << " y: " << p.y() << " z: " << p.z();
        return ss.str();
    }

    template <>
    static std::string toStlString<Geom::Vec>(const Geom::Vec& v, int precision)
    {
        std::stringstream ss;
        ss.precision(precision);
        ss << "x: " << v.x() << " y: " << v.y() << " z: " << v.z();
        return ss.str();
    }

    template <>
    static std::string toStlString<Geom::XYZ>(const Geom::XYZ& xyz, int precision)
    {
        std::stringstream ss;
        ss.precision(precision);
        ss << "x: " << xyz.x() << " y: " << xyz.y() << " z: " << xyz.z();
        return ss.str();
    }

    template <>
    static std::string toStlString<Geom::Dir>(const Geom::Dir& dir, int precision)
    {
        std::stringstream ss;
        ss.precision(precision);
        ss << "x: " << dir.x() << " y: " << dir.y() << " z: " << dir.z();
        return ss.str();
    }

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

    template <>
    static Base::String toString<Geom::Pnt>(const Geom::Pnt& p, int precision)
    {
        std::wstringstream ss;
        ss.precision(precision);
        ss << "x: " << p.x() << " y: " << p.y() << " z: " << p.z();
        return ss.str();
    }

    template <>
    static Base::String toString<Geom::Vec>(const Geom::Vec& v, int precision)
    {
        std::wstringstream ss;
        ss.precision(precision);
        ss << "x: " << v.x() << " y: " << v.y() << " z: " << v.z();
        return ss.str();
    }

    template <>
    static Base::String toString<Geom::XYZ>(const Geom::XYZ& xyz, int precision)
    {
        std::wstringstream ss;
        ss.precision(precision);
        ss << "x: " << xyz.x() << " y: " << xyz.y() << " z: " << xyz.z();
        return ss.str();
    }

    template <>
    static Base::String toString<Geom::Dir>(const Geom::Dir& dir, int precision)
    {
        std::wstringstream ss;
        ss.precision(precision);
        ss << "x: " << dir.x() << " y: " << dir.y() << " z: " << dir.z();
        return ss.str();
    }
    void to_do();
};

}  // namespace Geom