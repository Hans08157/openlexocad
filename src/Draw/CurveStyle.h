#pragma once
#include <Draw/OglMaterial.h>

namespace Draw
{
class LX_DRAW_EXPORT CurveStyle
{
public:
    CurveStyle();

    void setCurveWidth(double w);
    void setCurveMaterial(const Draw::OglMaterial& mat);
    void setCurveDashType(int t);
    void setCurveArrow(bool ar);
    void setCurveScaleFactor(double scalef);
    double getCurveWidth() const;
    const Draw::OglMaterial& getCurveMaterial() const;
    int getCurveDashType() const;
    bool getCurveArrow() const;
    double getCurveScaleFactor() const;


private:
    double _curveWidth = 1;
    Draw::OglMaterial _curveMaterial = Draw::OglMaterial(Base::Color(0, 0, 255));
    int _curveDashedType = 0;
    bool _curveArrow = false;
    double _curveScaleFactor = 100;
};

}  // namespace Draw
