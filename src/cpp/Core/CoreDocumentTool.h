#pragma once

#include <Base/String.h>


namespace Core
{
class CoreDocument;

class LX_CORE_EXPORT CoreDocumentTool
{
public:
    // stuff related to the document lock-files mechanism
    static Base::String getLockFileName(Core::CoreDocument* cDoc);
    static Base::String getLockFileName(const Base::String& path);
    static bool createLockFile(Core::CoreDocument* cDoc);
    static bool createLockFile(const Base::String& path, const Base::String& docfileName, const Base::String& tempdirectory);
    static bool deleteLockFile(Core::CoreDocument* cDoc);
    static bool readLockFile(Core::CoreDocument* cDoc, bool& dataOk, Base::String& userName, Base::String& computerName, Base::String& dateTime);
    static bool readLockFile(const Base::String& path, bool& dataOk, Base::String& userName, Base::String& computerName, Base::String& dateTime);

    static bool isTutorial(Core::CoreDocument* cDoc);
    static bool isTutorial(const Base::String& path);
    static std::pair<int,int> getAppVersionFromDocument(const Base::String& path);
};

}  // namespace Core
