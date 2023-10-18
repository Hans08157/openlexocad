#pragma once
#include <iosfwd>

namespace Draw
{
class LX_DRAW_EXPORT Texture2Transform
{
public:
    Texture2Transform();
    Texture2Transform(float translationX, float translationY, float rotation, float scaleFactorX, float scaleFactorY, float centerX, float centerY);
    ~Texture2Transform();

    void setValues(float translationX, float translationY, float rotation, float scaleFactorX, float scaleFactorY, float centerX, float centerY);
    void getValues(float& translationX,
                   float& translationY,
                   float& rotation,
                   float& scaleFactorX,
                   float& scaleFactorY,
                   float& centerX,
                   float& centerY) const;

    void setTranslation(float x, float y);
    void setRotation(float r);
    void setScaleFactor(float x, float y);
    void setCenter(float x, float y);

    void getTranslation(float& x, float& y) const;
    void getRotation(float& r) const;
    void getScaleFactor(float& x, float& y) const;
    void getCenter(float& x, float& y) const;

    bool operator==(const Texture2Transform& other) const;
    bool operator!=(const Texture2Transform& other) const;

    friend LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, const Texture2Transform& t2transform);

private:
    float _translationX;
    float _translationY;
    float _rotation;
    float _scaleFactorX;
    float _scaleFactorY;
    float _centerX;
    float _centerY;
};

}  // namespace Draw
