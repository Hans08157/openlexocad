#pragma once
#include <Draw/OglMaterial.h>

namespace Draw
{
class LX_DRAW_EXPORT SolidStyle
{
public:
    SolidStyle()=default;

    void setSolidMaterial(const Draw::OglMaterial& mat);

    const Draw::OglMaterial& getSolidMaterial() const;

private:
    Draw::OglMaterial _solidMaterial;
};

}  // namespace Draw
