#pragma once
#include <string>

namespace Base
{
class String;
}

namespace Draw
{
class LX_DRAW_EXPORT TextureCoordinateMapping
{
public:
    enum Mapping
    {
        NONE,      //
        CUBE,      // Autogenerates cubemapped texture coordinated for shapes.
        SPHERE,    // Autogenerates spheremapped texture coordinated for shapes.
        CYLINDER,  // Autogenerates cylinder mapped texture coordinated for shapes.
    };

    TextureCoordinateMapping();
    virtual ~TextureCoordinateMapping() = default;
    Mapping getCoordinateMapping() const { return _coordinateMapping; }
    void setCoordinateMapping(const Mapping m) { _coordinateMapping = m; }

    static TextureCoordinateMapping::Mapping getTextureCoordinateMappingEnum(int i);
    static TextureCoordinateMapping::Mapping getTextureCoordinateMappingEnum(const std::string& s);
    static TextureCoordinateMapping::Mapping getTextureCoordinateMappingEnum(const Base::String& s);
    static std::string getStringFromTextureCoordinateMappingEnum(TextureCoordinateMapping::Mapping m);

    bool operator==(const TextureCoordinateMapping& other) const;
    bool operator!=(const TextureCoordinateMapping& other) const;

protected:
    Mapping _coordinateMapping;
};

}  // namespace Draw
