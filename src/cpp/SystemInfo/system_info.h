/**
 *  @file
 *  CSystemInfo class header.
 *
 *  CSystemInfo class provides system information on both Windows and Mac OS X.
 *
 *  @author Boris "mondzi" Kudlaè
 */

#ifndef SYSTEM_INFO__H
#define SYSTEM_INFO__H

#ifdef SYSTEMINFO_EXPORTS
#define SYSTEMINFO_API __declspec(dllexport)
#else
#define SYSTEMINFO_API __declspec(dllimport)
#endif

#if defined(__APPLE__)
#include <AGL/AGL.h>
#include <ApplicationServices/ApplicationServices.h>
#include <sys/sysctl.h>
#include <sys/utsname.h>
#elif defined(_WIN32)

#endif
#include <map>
#include <QString>


class GLContext;
#include <windef.h>
// QT



class CSystemInfo
{
public:
    enum eForcedSetting
    {
        AA,
        AF,
        VSYNC
    };

    SYSTEMINFO_API static CSystemInfo* instance();

    // summary info
    SYSTEMINFO_API QString getSystemInfo();
    SYSTEMINFO_API QString getOpenGLInfo();

    // system info
    SYSTEMINFO_API QString getOS() { return _os; }
    SYSTEMINFO_API QString getCPU() { return _cpu; }
    SYSTEMINFO_API QString getDisplayInfo() { return _display_info; }
    SYSTEMINFO_API double getHDDTotalSpace() { return _hdd_total_space; }
    SYSTEMINFO_API double getHDDFreeSpace();
    SYSTEMINFO_API int getRAM() { return _ram; }
    SYSTEMINFO_API int getMemoryLoad();

    // OpenGL info
    SYSTEMINFO_API QString getOpenGLVendor() { return _gl_vendor; }
    SYSTEMINFO_API QString getOpenGLRenderer() { return _gl_renderer; }
    SYSTEMINFO_API QString getOpenGLVersion() { return _gl_version; }
    SYSTEMINFO_API int getMaxTextureSize() { return _gl_max_texture_size; }
    SYSTEMINFO_API int getDepthBits() { return _gl_depth_bits; }
    SYSTEMINFO_API int getStencilBits() { return _gl_stencil_bits; }
    SYSTEMINFO_API int getVRAMDedicated() { return _vram.dedicatedVRAM; }
    SYSTEMINFO_API int getVRAMDedicatedSystem() { return _vram.dedicatedSystem; }
    SYSTEMINFO_API int getVRAMShared() { return _vram.sharedSystem; }
    SYSTEMINFO_API int getMaxMultisample() { return _max_multisample; }
    SYSTEMINFO_API int getDriverForcedSetting(const eForcedSetting setting);
    SYSTEMINFO_API void print();


    // BIOS info cadwork, for licence
    SYSTEMINFO_API QString getBiosID_Cadwork() { return _bios_id_cadwork; }

    // DISPLAY info cadwork, for licence
    SYSTEMINFO_API QString getDisplayName_Cadwork() { return _display_name_cadwork; }


protected:
    CSystemInfo();
    ~CSystemInfo();

private:
    /** Name and version of the operating system. */
    QString _os;
    /** Name of the operating system. */
    QString _os_name;
    /** Version of the operating system. */
    QString _os_version;

    /** CPU model name and frequency. */
    QString _cpu;
    /** CPU model name. */
    QString _cpu_model;
    /** CPU frequency. */
    QString _cpu_frequency;

    /** Amount of system RAM in MB. */
    int _ram;

    /** Amount of video RAM in MB. */
    struct sVRAM
    {
        int dedicatedVRAM;    // Dedicated Video Memory
        int dedicatedSystem;  // System Video Memory
        int sharedSystem;     // Shared System Memory

        sVRAM() : dedicatedVRAM(0), dedicatedSystem(0), sharedSystem(0){};
        sVRAM(int a_dedicatedVRAM, int a_dedicatedSystem, int a_sharedSystem)
            : dedicatedVRAM(a_dedicatedVRAM), dedicatedSystem(a_dedicatedSystem), sharedSystem(a_sharedSystem){};
    };
    sVRAM _vram;

    /** Maximum antialiasing (multisample) samples. */
    int _max_multisample;

    /** HDD total space in MB. */
    double _hdd_total_space;

    /** Display info (screen id, resolution, mode) */
    QString _display_info;
    QString _gpu_driver;

    /** OpenGL info. */
    QString _gl_vendor;
    QString _gl_renderer;
    QString _gl_version;
    QString _gl_shader_version;
    int _gl_max_texture_size;
    int _gl_depth_bits;
    int _gl_stencil_bits;

    /** Driver forced settings. */
    std::map<eForcedSetting, int> _forced;

    // special cadwork licence
    QString _bios_id_cadwork;
    QString _display_name_cadwork;

#ifdef __APPLE__
    static double mac_get_dict_value(CFDictionaryRef refDict, CFStringRef key);
    QString mac_get_os_name(enum QSysInfo::MacVersion a_mac_version);
#elif defined(_WIN32)
    int win_get_vram(int& dedicatedVRAM, int& dedicatedSystem, int& sharedSystem);
    int win_get_max_multisample(GLContext glcontext);
    QString win_get_os_name(enum QSysInfo::WinVersion a_win_version);
#endif
    void detect_forced_settings();
};


class GLContext
{
public:
    GLContext();
    ~GLContext();

    bool isValid() { return _isValid; }

// protected:
#if defined(_WIN32)
    HWND m_hwnd;
    HDC m_dc;
    HGLRC m_rc;
#elif defined(__APPLE__)
    AGLContext m_ctx;
    AGLContext m_octx;
    int _max_multisample;

    int getMaxMultisample() { return _max_multisample; }
#endif
private:
    bool _isValid;
};

#endif  // SYSTEM_INFO__H