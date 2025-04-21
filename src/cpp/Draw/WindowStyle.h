#pragma once
#include <Draw/OglMaterial.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>

namespace Draw
{
class LX_DRAW_EXPORT WindowStyle
{
public:
    WindowStyle() = default;

    void setFrameMaterial(const OglMaterial& mat);
    void setFrameBackMaterial(const OglMaterial& mat);
    void setSillMaterial(const OglMaterial& mat);
    void setGlassMaterial(const OglMaterial& mat);
    void setGlassTexture(const Texture2& tex);
    void setTexture(const Texture2& tex);
    void setTexture2(const Texture2& tex);
    void setSillTexture(const Texture2& tex);
    void setTextureTransform(const Texture2Transform& ttf);

    const Draw::OglMaterial& getFrameMaterial() const;
    const Draw::OglMaterial& getFrameBackMaterial() const;
    const Draw::OglMaterial& getSillMaterial() const;
    const Draw::OglMaterial& getGlassMaterial() const;
    const Texture2& getGlassTexture() const;
    const Texture2& getTexture() const;
    const Texture2& getTexture2() const;
    const Texture2& getSillTexture() const;
    Texture2Transform getTextureTransform() const;

private:
    OglMaterial _frameMaterial;
    OglMaterial _frameBackMaterial;
    OglMaterial _sillMaterial;
    OglMaterial _glassMaterial;
    Texture2 _texture;
    Texture2 _texture2;
    Texture2 _sillTexture;
    Texture2 _glassTexture;
    Texture2Transform _textureTransform;
};

}  // namespace Draw
