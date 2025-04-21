#include <Shlobj.h>

namespace unregisterSettings
{

/*!
* Delete the application settings from the system registry.
* For now, works only on Windows platform.
*/
void unregisterSettings()
{
    QSettings settings("HKEY_CLASSES_ROOT", QSettings::NativeFormat);
    settings.remove(".lxz");
    settings.remove("Lexocad.lxz");
    settings.remove(".caz");
    settings.remove("Lexocad.caz");
    settings.remove(".cas");
    settings.remove("Lexocad.cas");
    settings.remove(".ifc");
    settings.remove("Lexocad.ifc");
    settings.remove(".obz");
    settings.remove("Lexocad.obz");
    settings.remove(".obcaz");
    settings.remove("Lexocad.obcaz");

    QSettings settings2("Cadwork Informatik", "Lexocad");
    settings2.clear();

    #if defined(_WIN32) || defined(_WIN64)
        SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, NULL, NULL);
        //SendMessage(HWND_BROADCAST, WM_SETTINGCHANGE, NULL, NULL);
    #endif
}

} // namespace
