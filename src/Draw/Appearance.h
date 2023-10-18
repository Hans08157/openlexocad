#pragma once
#include <Draw/OglMaterial.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>
#include <Draw/TextureCoordinateFunction.h>
#include <Draw/TextureCoordinateMapping.h>


namespace Draw
{
class LX_DRAW_EXPORT Appearance
{
public:
    Appearance();

    const QString& getName() const;
    void setName(const QString& name);

    OglMaterial& getMaterial();
    void setMaterial(OglMaterial mat);

    Texture2& getTexture2();
    void setTexture2(Texture2 texture);

    Texture2Transform& getTexture2Transform();
    void setTexture2Transform(Texture2Transform tt);

    TextureCoordinateMapping& getTextureCoordinateMapping();
    void setTextureCoordinateMapping(TextureCoordinateMapping tcm);

    TextureCoordinateFunction& getTextureCoordinateFunction();
    void setTextureCoordinateFunction(TextureCoordinateFunction tcf);



protected:
    QString _name;
    OglMaterial _matColors;
    Texture2 _texture2;
    Texture2Transform _texture2Transform;
    TextureCoordinateMapping _coordinateMapping;
    TextureCoordinateFunction _coordinateFunction;
};

}  // namespace Draw
