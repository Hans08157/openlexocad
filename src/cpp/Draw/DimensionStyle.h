#pragma once
#include <Geom/Ax1.h>
#include <Geom/Dir.h>
#include <Geom/Pnt.h>
#include <Geom/Trsf.h>
#include <memory>

class QFont;

namespace Base
{
class Color;
}

namespace Draw
{
class LX_DRAW_EXPORT DimensionStyle
{
public:
    enum TerminatorSymbol
    {
        DiagonalLine = 0,
        FilledArrow = 1,
    };

    enum AltitudeSymbol
    {
        FilledDownwards = 0,
        FilledUpwards = 1,
    };

    DimensionStyle();
    DimensionStyle(const DimensionStyle& o);
    DimensionStyle& operator=(const DimensionStyle&);
    ~DimensionStyle();

    const Base::Color& getTextColor() const;
    void setTextColor(const Base::Color& c);

    const QFont& getTextFont() const;
    void setTextFont(const QFont& font);

    double getTextScaleFactor() const;
    void setTextScaleFactor(double textScaleFactor);

    bool getTextIsCameraAligned() const;
    void setTextIsCameraAligned(bool onoff);

    int getNumberOfDecimals() const;
    void setNumberOfDecimals(int numberOfDecimals);

    TerminatorSymbol getTerminatorSymbol() const;
    void setTerminatorSymbol(TerminatorSymbol ts);

    AltitudeSymbol getAltitudeSymbol() const;
    void setAltitudeSymbol(AltitudeSymbol as);

    double getAnchorLength() const;
    void setAnchorLength(const double& anchorLength);

    double getAnchorDistance() const;
    void setAnchorDistance(const double& anchorDistance);

    double getMinimumDistance() const;
    void setMinimumDistance(const double& minimumDistance);

    bool getAnchorDistanceOpt() const;
    void setAnchorDistanceOpt(const bool& onoff);

    int getLengthUnits() const;
    void setLengthUnits(const int& unit);

    bool getTextLayout() const;
    void setTextLayout(const bool& textLayout);

    bool getUnitsCurrent() const;
    void setUnitsCurrent(const bool& _unitsCurrent);

    bool getTextVertical() const;  // 90 degree rotation along the dimension
    void setTextVertical(const bool& rotated);

    bool getTextOnNegativeSide() const;  // side of dimension, where the text is displayed
    void setTextOnNegativeSide(const bool& on);

private:
    class Impl;
    std::unique_ptr<Impl> _M_impl;
};


// only for passing as argument, to avoid many arguments
struct LX_DRAW_EXPORT DimensionParams
{
    std::vector<Geom::Pnt> points;
    Geom::Pnt dimensionCurvePassingPoint;
    Geom::Dir dimensionCurveDirection;
    Geom::Pnt textPositionOffset;
    double secondValue{};
    DimensionStyle ds;
    size_t variableParamIdx{};
    Geom::Trsf transform;
    bool projectToPlane{};
    Geom::Ax1 projectionPlane;
    bool showSumDimension = false;
    bool planeZY = false;
    int verticalPlaneMode = 0;
    bool textLayout = false;
    bool unitsCurrent = false;
    bool keepInPlane = false;
};


}  // namespace Draw
