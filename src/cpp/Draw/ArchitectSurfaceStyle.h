#pragma once
#include <memory>


class QFont;

namespace Draw
{
class OglMaterial;
class LX_DRAW_EXPORT ArchitectSurfaceStyle
{
public:
    ArchitectSurfaceStyle();
    ArchitectSurfaceStyle(const ArchitectSurfaceStyle& o);
    ArchitectSurfaceStyle& operator=(const ArchitectSurfaceStyle& o);
    ~ArchitectSurfaceStyle();

    void setArchitectSurfaceMaterial(const Draw::OglMaterial& mat);
    void setArchitectSurfaceFont(const QFont& font);  // font,size
    void setArchitectSurfaceHeight(double h);
    void setArchitectSurfaceRoof(bool r);
    void setArchitectSurfaceTextMaterial(const Draw::OglMaterial& matT);
    void setArchitectSurfaceAlignment(int a);

    const Draw::OglMaterial& getArchitectSurfaceMaterial() const;
    const QFont& getArchitectSurfaceFont() const;
    double getArchitectSurfaceHeight() const;
    bool getArchitectSurfaceRoof() const;
    const Draw::OglMaterial& getArchitectSurfaceTextMaterial() const;
    int getArchitectSurfaceAlignment() const;

private:
    class Impl;
    std::unique_ptr<Impl> _M_impl;

    //;
};

}  // namespace Draw
