#pragma once 

namespace Geom
{
class LX_GEOM_EXPORT GeomInit
{
public:
    static void init();
    static void release();

private:
    static bool isInit;
};

}  // namespace Geom