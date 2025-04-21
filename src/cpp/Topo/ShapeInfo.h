#pragma once
#include <string>

namespace Topo
{
class ShapeInfo
{
public:
    enum class ShapeInfoStatus
    {
        OKAY,
        ERRORS
    };


    ShapeInfoStatus status;
    std::string status_info;
    std::string detail_info;
};
}  // namespace Topo