#pragma once
#include <mutex>
extern LX_BASE_EXPORT std::mutex global_modeller_mutex;
#define MODELLERLOCK(myop) myop