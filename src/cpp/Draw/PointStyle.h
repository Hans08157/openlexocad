#pragma once
#include <Draw/OglMaterial.h>

namespace Draw
{
class LX_DRAW_EXPORT PointStyle
{
public:
    PointStyle();

    void setPointSize(double w);
    void setPointMaterial(const Draw::OglMaterial& mat);
    void setPointFixSize(bool fSize);
    void setPointType(int t);

    double getPointSize() const;
    const Draw::OglMaterial& getPointMaterial() const;
    bool getPointFixSize() const;
    int getPointType() const;

private:
    double _pointSize;
    Draw::OglMaterial _pointMaterial;
    bool _fixSize;
    int _pointType;
};

}  // namespace Draw
