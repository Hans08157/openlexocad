///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once
#include <Base/String.h>

namespace Draw
{
class LX_DRAW_EXPORT DrawStyle
{
public:
    enum Style
    {
        FILLED,
        LINES,
        FILLEDWITHLINES,
        FILLEDWITHBLACKLINES,
        POINTS,
        HALFTRANSPARENT,
        VERTICES,
        HIDDENLINES,
        DASHEDHIDDENLINES
    };
    DrawStyle() = default;
    DrawStyle(Style style, float pointSize = 0.0f, float lineWidth = 1.0f, uint16_t linePattern = 0xffff, int linePatternScaleFactor = 1);

    bool operator==(const DrawStyle& other) const;
    bool operator!=(const DrawStyle& other) const;

    Style getStyle() const;
    void setStyle(Style style);
    void setStyle(const Base::String& style);
    Base::String getStyleAsString() const;
    float getPointSize() const;
    void setPointSize(float size);
    float getLineWidth() const;
    void setLineWidth(float width);
    uint16_t getLinePattern() const;
    void setLinePattern(short pattern);
    bool getShowVertices() const;
    void setShowVertices(bool on);
    bool getShowControlPoints() const;
    void setShowControlPoints(bool on);
    int getLinePatternScaleFactor() const;
    void setLinePatternScaleFactor(int linePatternScaleFactor);
    static Style getStyleFromString(const Base::String& mystyle);

    friend LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, DrawStyle& ds);

    size_t hash() const;


private:
    Style _style = DrawStyle::FILLED;
    float _pointSize = 0.0f;
    float _lineWidth = 1.0f;
    uint16_t _linePattern = 0xffff;
    bool _showVertices = false;
    bool _showControlPoints = false;
    int _linePatternScaleFactor = 1;
};
LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, DrawStyle& ds);
LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, const DrawStyle& ds);
}  // namespace Draw