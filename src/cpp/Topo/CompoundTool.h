#pragma once

namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Compounds.
 *
 * @ingroup TOPO_SHAPETOOLS
 */
class LX_TOPO_EXPORT CompoundTool
{
public:
    virtual ~CompoundTool() = default;

    static void __setDefaultTool__(Topo::CompoundTool* tool) { _defaultTool = tool; }

private:
    static Topo::CompoundTool* _defaultTool;
};

}  // namespace Topo