#pragma once
#include <Draw/OglMaterial.h>

namespace Draw
{
class LX_DRAW_EXPORT ExtrusionStyle
{
public:
    ExtrusionStyle();

    void setExtrusionMaterial(const Draw::OglMaterial& mat);
    void setExtrusionDashType(int t);

    const Draw::OglMaterial& getExtrusionMaterial() const;
    int getExtrusionDashType() const;

private:
    Draw::OglMaterial _extrusionMaterial;
    int _extrusionDashedType;
};

}  // namespace Draw