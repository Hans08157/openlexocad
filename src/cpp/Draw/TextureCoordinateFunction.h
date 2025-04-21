#pragma once
#include <Geom/Vec.h>

namespace Base
{
class String;
}

namespace Draw
{
class LX_DRAW_EXPORT TextureCoordinateFunction
{
public:
    enum Function
    {
        DEFAULT,     // Cleans out all previously defined texture coordinates and texture coordinate functions.
        PLANE,       // Generates texture coordinates by projecting onto a plane.
        ENVIRONMENT  // Generates texture coordinates by projecting onto a surrounding texture.
                     // The texture will be mapped onto the scenegraph taking camera position
                     // into account. This will lead to an object reflecting its enviroment.
    };

    TextureCoordinateFunction();
    virtual ~TextureCoordinateFunction() = default;
    Function getCoordinateFunction() const { return _coordinateFunction; }
    const Geom::Vec& getDirectionS() const { return _directionS; }
    const Geom::Vec& getDirectionT() const { return _directionT; }
    void setCoordinateFunction(const Function m) { _coordinateFunction = m; }
    void setDirectionS(const Geom::Vec dirS) { _directionS = dirS; }
    void setDirectionT(const Geom::Vec dirT) { _directionT = dirT; }

    static TextureCoordinateFunction::Function getTextureCoordinateFunctionEnum(int i);
    static TextureCoordinateFunction::Function getTextureCoordinateFunctionEnum(const std::string& str);
    static TextureCoordinateFunction::Function getTextureCoordinateFunctionEnum(const Base::String& str);
    static std::string getStringFromTextureCoordinateFunctionEnum(TextureCoordinateFunction::Function m);

    bool operator==(const TextureCoordinateFunction& other) const;
    bool operator!=(const TextureCoordinateFunction& other) const;

protected:
    Geom::Vec _directionS;
    Geom::Vec _directionT;
    Function _coordinateFunction;
};

}  // namespace Draw
