#pragma once
#include <Draw/OglMaterial.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>


namespace Draw
{
class LX_DRAW_EXPORT SurfaceStyle
{
public:
    SurfaceStyle() = default;

    void setSurfaceMaterial(const OglMaterial& mat);
    void setTexture(const Texture2& tex);
    void setTextureTransform(const Texture2Transform& ttf);

    const Draw::OglMaterial& getSurfaceMaterial() const;
    const Texture2& getTexture() const;
    Texture2Transform getTextureTransform() const;

private:
    OglMaterial _surfaceMaterial;
    Texture2 _texture;
    Texture2Transform _textureTransform;
};

}  // namespace Draw
