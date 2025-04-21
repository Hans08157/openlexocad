#pragma once

namespace Base
{
class LX_BASE_EXPORT BaseInit
{
public:
    static void init();
    static void release();

private:
    static bool isInit;
};
}  // namespace Base
