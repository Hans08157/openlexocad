#pragma once

#include <string>

namespace Core
{
class LX_CORE_EXPORT SysInfo
{
public:
    static std::string getUserName();
    static std::string getComputerName();
};

}  // namespace Core
