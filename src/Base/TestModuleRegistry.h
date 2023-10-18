#pragma once
#include <vector>
#include <string>

namespace Base
{
struct TestModuleRegistry;

//< Global registry for test module names. These should be loaded by test runner at the start. 
extern LX_BASE_EXPORT TestModuleRegistry testModuleRegistry;

/**
 * \brief This class is holds the name of test modules that should be loaded for testing.
 */
struct LX_BASE_EXPORT TestModuleRegistry
{
    void registerABUTestModule(const wchar_t* moduleName);

    //assuming that deregistering is not needed

    const std::vector<std::wstring>& getModuleNames() const {return ABUTestModules;}

protected:
    std::vector<std::wstring> ABUTestModules;
};
}
