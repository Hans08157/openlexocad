#pragma once
#include <Base/String.h>
#include <memory>


class QFont;

namespace Draw
{
class OglMaterial;
class LX_DRAW_EXPORT TextStyle
{
public:
    TextStyle();
    TextStyle(const TextStyle& o);
    TextStyle& operator=(const TextStyle& o);
    ~TextStyle();

    void setTextMaterial(const Draw::OglMaterial& mat);
    void setTextFont(const QFont& font);
    void setTextScaleFactor(double s);
    void setTextPointSize(int aTextPointSize);
    void setTextItalic(bool i);
    void setTextBold(bool b);
    void setTextFrame(bool f);
    void setTextBackground(bool bg);
    void setTextMaterialBackground(const Draw::OglMaterial& matbg);
    void setTextSpec(const Base::String& specText);

    const Draw::OglMaterial& getTextMaterial() const;
    const QFont& getTextFont() const;
    double getTextScaleFactor() const;
    int  getTextPointSize() const;
    bool getTextItalic() const;
    bool getTextBold() const;
    bool getTextFrame() const;
    bool getTextBackground() const;
    Base::String getTextSpec() const;
    const Draw::OglMaterial& getTextMaterialBackground() const;

private:
    class Impl;
    std::unique_ptr<Impl> _M_impl;
};

}  // namespace Draw
