#pragma once
#include <Draw/OglMaterial.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>

namespace Draw
{
class LX_DRAW_EXPORT DoorStyle
{
public:
    DoorStyle() = default;

    void setFrameMaterial(const OglMaterial& mat);
    void setFrameBMaterial(const OglMaterial& mat);
    void setSillMaterial(const OglMaterial& mat);
    void setGlassMaterial(const OglMaterial& mat);
    void setPanelMaterial(const OglMaterial& mat);
    void setPlateTexture(const Texture2& tex);
    void setSillTexture(const Texture2& tex);
    void setFrontTexture(const Texture2& tex);
    void setBackTexture(const Texture2& tex);
    void setTextureTransform(const Texture2Transform& ttf);

    const Draw::OglMaterial& getFrameMaterial() const;
    const Draw::OglMaterial& getFrameBMaterial() const;
    const Draw::OglMaterial& getSillMaterial() const;
    const Draw::OglMaterial& getGlassMaterial() const;
    const Draw::OglMaterial& getPanelMaterial() const;
    const Texture2& getPlateTexture() const;
    const Texture2& getSillTexture() const;
    const Texture2& getFrontTexture() const;
    const Texture2& getBackTexture() const;
    Texture2Transform getTextureTransform() const;

private:
    OglMaterial _frameMaterial;
    OglMaterial _frameBMaterial;
    OglMaterial _sillMaterial;
    OglMaterial _glassMaterial;
    OglMaterial _panelMaterial;
    Texture2 _plateTexture;
    Texture2 _sillTexture;
    Texture2 _frontTexture;
    Texture2 _backTexture;
    Texture2Transform _textureTransform;
};

}  // namespace Draw
