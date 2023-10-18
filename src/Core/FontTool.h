#pragma once 

class QFont;

namespace Core
{
class LX_CORE_EXPORT FontTool
{
public:
    static int getFixedStretch(
        const QFont& font);  // Qt changed default value for stretch from 100 to 0, if font.stretch() is 0, this method returns 100
};
}  // namespace Core