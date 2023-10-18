#pragma once 

#include <windows.h>
#include <iostream>

namespace Core
{
/** Library loader can safely load DLL and provides safe unload in destructor.
 *  Calling of FreeLibrary is important during application tear-down, otherwise there is risk of crash.
 *  The class is header-only.
 */
class LibraryLoader final
{
public:
    HMODULE handle;

    LibraryLoader() : handle(nullptr) {}
    LibraryLoader(const wchar_t* fileName) : handle(LoadLibrary(fileName))
    {
        if (!handle)
            std::wcerr << "ERROR: unable to load library " << fileName<< ". Reason: " << GetLastError() << std::endl;
    }
    LibraryLoader(HMODULE h) : handle(h) {}
    LibraryLoader(LibraryLoader&& ll) : handle(ll.handle) { ll.handle = nullptr; }
    LibraryLoader& operator=(LibraryLoader&& ll)
    {
        if (handle)
            FreeLibrary(handle);
        handle = ll.handle;
        ll.handle = nullptr;
    }
    ~LibraryLoader()
    {
        if (handle)
            FreeLibrary(handle);
    }

    LibraryLoader(const LibraryLoader&) = delete;
    LibraryLoader& operator=(const LibraryLoader&) = delete;

    bool valid() const { return handle != nullptr; }
    bool load(const wchar_t* filename)
    {
        if (handle)
            FreeLibrary(handle);
        handle = LoadLibrary(filename);
        return handle != nullptr;
    }
    void free()
    {
        if (handle)
        {
            FreeLibrary(handle);
            handle = nullptr;
        }
    }
    template <typename T>
    T resolve(const char* funcName)
    {
        return reinterpret_cast<T>(GetProcAddress(handle, funcName));
    }
};


}  // namespace Core
