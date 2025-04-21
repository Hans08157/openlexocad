#pragma once

class LX_BASE_EXPORT Memory_Usage
{
public:
    static long long usageBytes();
    static unsigned long usageMegaBytes();
    static unsigned long systemMemoryMegaBytes();
    static unsigned long availMemoryMegaBytes();
};