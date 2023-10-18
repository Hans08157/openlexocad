#pragma once

namespace Draw
{
class LX_DRAW_EXPORT DrawInit
{
public:
    static void init();
    static void release();

private:
    static bool isInit;
};
}  // namespace Draw
