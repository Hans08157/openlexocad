#pragma once
#include <Core/Settings.h>

namespace Topo
{
class LX_TOPO_EXPORT ShapeTessellationQuality
{
public:
    Core::Settings::ShapeTessellationQuality quality;
    Core::Settings::ShapeTessellationMode mode;
    bool globalMeshMode;
    ShapeTessellationQuality()
        : quality(Core::Settings::medium_fine), mode(Core::Settings::facet_options_visualization), globalMeshMode(false)
    {
    }
};
}