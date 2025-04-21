#pragma once
#include <Base/String.h>
#include <list>
#include <map>
#include <memory>


class CA_ColorP;

namespace Base
{
class Color;

class LX_BASE_EXPORT MColor
{
public:
    MColor(unsigned char r, unsigned char g, unsigned char b, unsigned char a);
    MColor();
    explicit MColor(const Base::Color& c);

    unsigned char red() const;
    unsigned char green() const;
    unsigned char blue() const;
    unsigned char alpha() const;

    unsigned char r;
    unsigned char g;
    unsigned char b;
    unsigned char a;

    bool operator==(const MColor& c) const;
    bool operator!=(const MColor& c) const;

    size_t hash() const;
};


class LX_BASE_EXPORT Color
{
public:
    friend class CA_ColorP;

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    enum Spec
    {
        Invalid,
        Rgb,
        Hsv,
        Cmyk
    };

    Color();
    Color(const Base::MColor& c);
    Color(int r, int g, int b, int a = 255);
    Color(const std::string& name);
    Color(const char* name);
    Color(const Color& rhs);
    Color(Spec spec);

    bool isValid() const;

    std::string name() const;
    void setNamedColor(const std::string& name);

    static std::list<std::string> colorNames();

    Spec spec() const;

    int alpha() const;
    void setAlpha(int alpha);

    double alphaF() const;
    void setAlphaF(double alpha);

    int red() const;
    int green() const;
    int blue() const;
    void setRed(int red);
    void setGreen(int green);
    void setBlue(int blue);

    double redF() const;
    double greenF() const;
    double blueF() const;
    void setRedF(double red);
    void setGreenF(double green);
    void setBlueF(double blue);

    void getRgb(int* r, int* g, int* b, int* a = nullptr) const;
    void setRgb(int r, int g, int b, int a = 255);

    void getRgbF(double* r, double* g, double* b, double* a = nullptr) const;
    void setRgbF(double r, double g, double b, double a = 1.0);

    int hue() const;  // 0 <= hue < 360
    int saturation() const;
    int value() const;

    double hueF() const;  // 0.0 <= hueF < 360.0
    double saturationF() const;
    double valueF() const;

    void getHsv(int* h, int* s, int* v, int* a = nullptr) const;
    void setHsv(int h, int s, int v, int a = 255);

    void getHsvF(double* h, double* s, double* v, double* a = nullptr) const;
    void setHsvF(double h, double s, double v, double a = 1.0);

    int cyan() const;
    int magenta() const;
    int yellow() const;
    int black() const;

    double cyanF() const;
    double magentaF() const;
    double yellowF() const;
    double blackF() const;

    void getCmyk(int* c, int* m, int* y, int* k, int* a = nullptr);
    void setCmyk(int c, int m, int y, int k, int a = 255);

    void getCmykF(double* c, double* m, double* y, double* k, double* a = nullptr);
    void setCmykF(double c, double m, double y, double k, double a = 1.0);

    Color toRgb() const;
    Color toHsv() const;
    Color toCmyk() const;

    Color convertTo(Spec colorSpec) const;

    static Color fromRgb(int r, int g, int b, int a = 255);
    static Color fromRgbF(double r, double g, double b, double a = 1.0);

    static Color fromHsv(int h, int s, int v, int a = 255);
    static Color fromHsvF(double h, double s, double v, double a = 1.0);

    static Color fromCmyk(int c, int m, int y, int k, int a = 255);
    static Color fromCmykF(double c, double m, double y, double k, double a = 1.0);

    Color light(int f = 150) const;
    Color lighter(int f = 150) const;
    Color dark(int f = 200) const;
    Color darker(int f = 200) const;

    Color& operator=(const Color&);

    bool operator==(const Color& c) const;
    bool operator!=(const Color& c) const;
    bool operator<(const Color& c) const;

    /// Provides access to the cadwork palette.
    static const std::map<std::pair<unsigned int, unsigned int>, Base::Color>& getCdwkPalette();

    /// Converts a Color to a cadwork color
    std::pair<unsigned int, unsigned int> toCdwkColor(bool* isPrecise = nullptr) const;
    unsigned toCdwkColor256(bool* isPrecise = nullptr) const;

    /// Converts a cadwork color to a Color
    static Color fromCdwkColor(const unsigned int integerPart, const unsigned int decimalPart = 0);

    /// Returns maximum number in cadwork palette. Classic cadwork palette has numbers [1-256].
    static unsigned int maximumCdwkColorIntegerNumber();
    /// Returns maximum number that is available in decimal part.
    static unsigned int maximumDecimalPartNumber();

    /// Returns tooltip for given color.
    static Base::String getToolTip(const Base::Color& color);

    /// Reloads Lcc colors from the file
    static void loadLccColors(const Base::String& filename, const unsigned int startIndex, const unsigned int endIndex);
    /// Sets 1 Lcc color
    static void setLccColor(const unsigned int index, const Base::Color& color, const Base::String& tooltip);
    /// Sets Lcc colors from the map
    static void setLccColors(const std::map<int, Base::Color>& colors, const std::map<Base::Color, Base::String>& tooltips);
    /// Clears all present Lcc colors (Lcc or user)
    static void clearLccColors(const unsigned int startIndex, const unsigned int endIndex);

    /// Returns true if the color is intended to be used for Lcc elements/components.
    bool isLcc() const;
    /// Returns true if the color is intended to be used for Lcc Lexocad elements/components.
    bool isLccLexocad() const;
    /// Returns true if the color is intended to be used for Lcc wood elements/components.
    bool isLccWood() const;
    /// Returns true if the color is intended to be used for Lcc user elements/components.
    bool isLccUser() const;
    /// Returns true if the color is intended to be used for main Lcc elements/components.
    bool isMainLcc() const;

    friend std::size_t hash_value(const Color& b) { return b.hash(); }

    size_t hash() const;

    /// Deprecated? static API, left here for compatibility -mh-
    static std::pair<unsigned int, unsigned int> toCdwkColor(const Color& color, bool* isPrecise = nullptr);
    static unsigned toCdwkColor256(const Color& color, bool* isPrecise = nullptr);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

    Color(unsigned int rgb);
    /// construct fully qualified cadwork palette color without checking anything, make this private? -mh-
    Color(int r, int g, int b, unsigned int integerPart, unsigned int decimalPart);
    ~Color();

    unsigned int rgb() const;
    unsigned int rgba() const;

    friend LX_BASE_EXPORT std::ostream& operator<<(std::ostream& o, const Base::Color& color);

    static constexpr unsigned int lccLexocadStart = 500;
    static constexpr unsigned int lccLexocadEnd = 1499;
    static constexpr unsigned int lccWoodStart = 2000;
    static constexpr unsigned int lccWoodEnd = 2999;
    static constexpr unsigned int lccUserStart = 5000;

private:
    std::unique_ptr<CA_ColorP> _pimpl;
};
LX_BASE_EXPORT std::ostream& operator<<(std::ostream& o, const Base::Color& color);
};  // namespace Base
