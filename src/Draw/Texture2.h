#pragma once
#include <Base/Color.h>
#include <Base/String.h>


namespace Draw
{
class LX_DRAW_EXPORT Texture2
{
public:
    enum Model
    {
        // These should match GL_BLEND, GL_MODULATE and GL_DECAL for SGI
        // Inventor compatibility (these are also used by SoTexture2 and
        // SoTexture3).
        BLEND = 0x0be2,
        MODULATE = 0x2100,
        DECAL = 0x2101,
        REPLACE_ = 0x1E01  // must match GL_REPLACE
    };

    enum Wrap
    {
        // These should match GL_CLAMP and GL_REPEAT for SGI Inventor
        // compatibility (these are also used by SoTexture2 and
        // SoTexture3).
        CLAMP = 0x2900,
        REPEAT = 0x2901
    };

    Texture2(void);
    Texture2(const Base::String& textureFileName,
             const Base::String& textureOriginalFileName,
             Texture2::Model mappingModel,
             Texture2::Wrap wrapS,
             Texture2::Wrap wrapT,
             const Base::Color& blendColor,
             bool textureImageIsExternal);
    ~Texture2(void);

    Texture2& operator=(const Texture2& rhs);
    bool operator==(const Texture2& rhs) const;

    void setValues(const Base::String& textureFileName,
                   const Base::String& textureOriginalFileName,
                   Texture2::Model mappingModel,
                   Texture2::Wrap wrapS,
                   Texture2::Wrap wrapT,
                   const Base::Color& blendColor,
                   bool textureImageIsExternal);
    void getValues(Base::String& textureFileName,
                   Base::String& textureOriginalFileName,
                   Texture2::Model& mappingModel,
                   Texture2::Wrap& wrapS,
                   Texture2::Wrap& wrapT,
                   Base::Color& blendColor,
                   bool& textureImageIsExternal) const;

    void setTextureFileName(const Base::String& tfn) { _textureFileName = tfn; }
    void setTextureOriginalFileName(const Base::String& tfn) { _textureOriginalFileName = tfn; }
    void setTextureOriginalFileNameAbsolut(const Base::String& tfn) { _textureOriginalFileNameAbsolut = tfn; }
    void setMappingModel(const Model m) { _mappingModel = m; }
    void setWrapS(const Wrap w) { _wrapS = w; }
    void setWrapT(const Wrap w) { _wrapT = w; }
    void setBlendColor(const Base::Color& c) { _blendColor = c; }
    void setTextureImageIsExternal(bool external) { _textureImageIsExternal = external; }
    void setTextureImageIsSavedOptimized(bool onoff) { _textureImageIsSavedOptimized = onoff; }

    const Base::String& getTextureFileName() const { return _textureFileName; }
    const Base::String& getTextureOriginalFileName() const { return _textureOriginalFileName; }
    const Base::String& getTextureOriginalFileNameAbsolut() const { return _textureOriginalFileNameAbsolut; }
    Model getMappingModel() const { return _mappingModel; }
    Wrap getWrapS() const { return _wrapS; }
    Wrap getWrapT() const { return _wrapT; }
    const Base::Color& getBlendColor() const { return _blendColor; }
    bool isTextureImageExternal() const { return _textureImageIsExternal; }
    bool getTextureImageIsSavedOptimized() const { return _textureImageIsSavedOptimized; }

    static Texture2::Model getModelEnum(int i);
    static Texture2::Model getModelEnum(const std::string& str);
    static Texture2::Model getModelEnum(const Base::String& str);
    static Texture2::Wrap getWrapEnum(int i);
    static Texture2::Wrap getWrapEnum(const std::string& str);
    static Texture2::Wrap getWrapEnum(const Base::String& str);
    static std::string getStringFromModelEnum(Texture2::Model m);
    static std::string getStringFromWrapEnum(Texture2::Wrap w);

    std::string getTextureMD5();
    void setTextureMD5(std::string);

    bool hasTexture() const;
    std::string dump();

    friend LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, const Texture2& texture);

    size_t hash() const;

protected:
    Base::String _textureFileName;
    Base::String _textureOriginalFileName;
    Base::String _textureOriginalFileNameAbsolut;
    bool _textureImageIsExternal;
    bool _textureImageIsSavedOptimized = false;
    Model _mappingModel;
    // image field (SoSFImage) implementation not yet defined
    Wrap _wrapS;
    Wrap _wrapT;
    Base::Color _blendColor;  // SbColor
    std::string _md5;
};

}  // namespace Draw
