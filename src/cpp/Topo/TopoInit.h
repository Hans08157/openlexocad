#pragma once

/** @defgroup TOPO_SHAPES Shapes
 */


/** @defgroup TOPO_SHAPETOOLS Shape Tools
 */


namespace Topo
{
class LX_TOPO_EXPORT TopoInit
{
public:
    static void init();
    static void release();

private:
    static bool isInit;
};

}  // namespace Topo