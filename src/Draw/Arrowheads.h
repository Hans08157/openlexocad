#pragma once
#include <Base/String.h>

namespace Draw
{
class LX_DRAW_EXPORT Arrowheads
{
public:
    enum Style
    {
        NONE,
        ARROW,
        DOT,
        ARROWLINE
    };

    Arrowheads();
    Arrowheads(Style startStyle, Style endStyle, double startSize, double endSize, bool useFactor);

    bool operator==(const Arrowheads& other) const;
    bool operator!=(const Arrowheads& other) const;

    Style getStartStyle() const { return _startStyle; }
    Base::String getStartStyleAsString() const { return _getStyleAsString(_startStyle); }
    void setStartStyle(Style style) { _startStyle = style; }
    void setStartStyle(const Base::String& style) { _setStyle(_startStyle, style); }

    Style getEndStyle() const { return _endStyle; }
    Base::String getEndStyleAsString() const { return _getStyleAsString(_endStyle); }
    void setEndStyle(Style style) { _endStyle = style; }
    void setEndStyle(const Base::String& style) { _setStyle(_endStyle, style); }

    double getStartSize() const { return _startSize; }
    void setStartSize(double size) { _startSize = size; }

    double getEndSize() const { return _endSize; }
    void setEndSize(double size) { _endSize = size; }

    bool getUseFactor() const { return _useFactor; }
    void setUseFactor(bool useFactor) { _useFactor = useFactor; }

    static Style getStyleFromString(const Base::String& StyleStr);

private:
    Style _startStyle;
    Style _endStyle;
    double _startSize;
    double _endSize;
    bool _useFactor;  // if true, size is line thickness * start/endSize and it is in pixels instead of meters

    void _setStyle(Style& start_or_end, const Base::String& style);
    Base::String _getStyleAsString(const Style& start_or_end) const;
};

}  // namespace Draw