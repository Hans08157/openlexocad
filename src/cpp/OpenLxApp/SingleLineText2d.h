#pragma once

#include <App/TextStylePreset.h>
#include <Base/String.h>
#include <Draw/TextStyle.h>
#include <OpenLxApp/Geometry.h>

FORWARD_DECL(Mesh, SingleLineText2d)

namespace OpenLxApp
{
/*!
 * @brief A single line two-dimensional text.
 * @ingroup OPENLX_GEOMETRIC_ITEMS
 */

class LX_OPENLXAPP_EXPORT SingleLineText2d : public Geometry
{
    PROXY_HEADER(SingleLineText2d, Mesh::SingleLineText2d, IFCTEXTLITERAL)

    DECL_PROPERTY(SingleLineText2d, Text, Base::String)
    DECL_PROPERTY(SingleLineText2d, TextStyle, Draw::TextStyle)

public:
    void setColor(const Base::Color& color) const;
    void setFontBold(bool enable = true) const;
    void setFontItalic(bool enable = true) const;
    void setFontName(const std::string& family) const;
    void setFontSize(int pointSize) const;
    void setFontStretch(double factor) const;
    void setScale(double factor) const;
    void setText(const std::string& text) const;

    ~SingleLineText2d() = default;

private:
    SingleLineText2d() = default;
};
} // namespace OpenLxApp
