#pragma once

#include <memory>


namespace Core
{
class LibraryLoader;
class VersionP;

/**
 * \brief A proxy class to conveniently get the automatically generated version of lexocad.
 *
 * This class serves for decoupling the generation of the version data by cmake by every configure
 * and compilation of Core. If you include the generated header file directly it will force the Core
 * to be recompiled every time the header is generated (e.g. when the svn revision number changes = every time).
 * And thus to possibly recompile everything that depends on the Core ( = almost everything).
 */
class Version
{
public:
    using PFN_LexocadVersion = void (*)(int*, int*, int*, int*);
    using PFN_LexocadVersionPart = int (*)();
    using PFN_LexocadVersionString = const char* (*)();


    Version(const Version& other) = delete;
    Version& operator=(const Version& other) = delete;

    static Version& instance();
    /*
     * NOTE! That the order of declaration of the class members IS very important!
     * Do not screw with this unless you know how the class initialization goes.
     * (ISO/IEC 14882:2003(E) section 12.6.2)
     * On the other hand it will fail in runtime during dll loading... so you will
     * know  :)
     *  - forry
     */
private:
    Version();
    std::unique_ptr<LibraryLoader> lxInfoDLL;

    //PFN_LexocadVersion getLexocadVersion;
    PFN_LexocadVersionPart getLexocadVersionMajor;
    PFN_LexocadVersionPart getLexocadVersionMinor;
    PFN_LexocadVersionPart getLexocadVersionPatch;
    PFN_LexocadVersionPart getLexocadVersionRevision;

    PFN_LexocadVersionString getLexocadBuildDateTime;
    PFN_LexocadVersionString getLexocadDocumentVersion;
    PFN_LexocadVersionString getLexocadProductVersionStr;

public:
    const unsigned major;
    const unsigned minor;
    const unsigned patch;
    const unsigned revision;

    const char* buildDateTime;
    const char* document;
    const char* product;

};

extern LX_CORE_EXPORT Version& version;  // = Version::instance();
}
