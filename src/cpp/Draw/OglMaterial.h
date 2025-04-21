///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once
#include <Base/Color.h>


namespace Draw
{
class LX_DRAW_EXPORT OglMaterial
{
public:
    OglMaterial() = default;
    ~OglMaterial() = default;

    OglMaterial(const Base::Color& diffuseColor);
    OglMaterial(const Base::Color& ambientColor,
                const Base::Color& diffuseColor,
                const Base::Color& specularColor,
                const Base::Color& emissiveColor,
                int shininess,
                int transparency);
    OglMaterial(const Base::Color& ambientColor,
                const Base::Color& diffuseColor,
                const Base::Color& specularColor,
                const Base::Color& emissiveColor,
                const Base::Color& reflection,
                int shininess,
                int transparency);

    OglMaterial& operator=(const OglMaterial& rhs);
    bool operator==(const OglMaterial& rhs) const;

    void setValues(const Base::Color& ambientColor,
                   const Base::Color& diffuseColor,
                   const Base::Color& specularColor,
                   const Base::Color& emissiveColor,
                   int shininess,
                   int transparency);
    void getValues(Base::Color& ambientColor,
                   Base::Color& diffuseColor,
                   Base::Color& specularColor,
                   Base::Color& emissiveColor,
                   int& shininess,
                   int& transparency) const;

    void setAmbientColor(const Base::Color& c);
    void setDiffuseColor(const Base::Color& c);
    void setSpecularColor(const Base::Color& c);
    void setEmissiveColor(const Base::Color& c);
    void setReflectiveColor(const Base::Color& c);
    void setReflectiveColor(const double& percent);
    Base::Color getAmbientColor() const;
    Base::Color getDiffuseColor() const;
    Base::Color getSpecularColor() const;
    Base::Color getEmissiveColor() const;
    Base::Color getReflectiveColor() const;

    void setShininess(int i);
    void setTransparency(int i);
    int getShininess() const;
    int getTransparency() const;

    bool hasSameValuesAs(const Draw::OglMaterial& mat) const;

    friend LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, const Draw::OglMaterial& material);

    friend std::size_t hash_value(OglMaterial const& b) { return b.hash(); }

    size_t hash() const;

private:
    Base::Color _ambientColor = Base::Color::fromCdwkColor(15);
    Base::Color _diffuseColor = Base::Color::fromCdwkColor(34);
    Base::Color _specularColor = Base::Color::fromCdwkColor(8);
    Base::Color _emissiveColor = Base::Color::fromCdwkColor(8);
    Base::Color _reflectiveColor = Base::Color::fromCdwkColor(8);  // for Lexolight, definition for POV-Ray
    int _shininess = 20;
    int _transparency = 0;
};
LX_DRAW_EXPORT std::ostream& operator<<(std::ostream& o, const Draw::OglMaterial& material);
}  // namespace Draw
