#pragma once
LX_CORE_EXPORT void do_profile_core(bool on);
LX_CORE_EXPORT size_t get_profiled_mem_core();

namespace Core
{
class LX_CORE_EXPORT CoreInit
{
public:
    CoreInit() {}
    ~CoreInit() {}

public:
    static void init();
    static void release();

private:
    static bool isInit;
};

}  // namespace Core
