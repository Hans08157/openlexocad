#pragma once 

#include <Base/String.h>
#include <QJsonDocument>
#include <functional>
#include <map>

class QWidget;

namespace Geom
{
class Pnt;
}

namespace Core
{
class LX_CORE_EXPORT Proj4Detail
{
public:
    std::string id;
    std::string desc;
    std::string proj4;
};

class LX_CORE_EXPORT Proj4
{
public:
    std::string ccid;
    std::string id;
    std::map<std::string, Proj4Detail> proj4s;
};

class LX_CORE_EXPORT Util
{
public:
    static Base::String createTempName(const Base::String& dir, const Base::String& temp);
    static void* getClassFromDLL(const Base::String& dllname, const Base::String& classname);
    static void loadDLL(const Base::String& dllname);
    static void removeDirectory(const Base::String& name);
    static unsigned long long getDiskFreeSpaceOfDirectoryInMB(const Base::String& dir);
    static unsigned long long getDiskFreeSpaceOfDirectoryInKB(const Base::String& dir);
    static bool isMainThread();
    static bool isBigEndian();

    static Base::String getDirectoryFromPath(const Base::String& aFilePath);
    static Base::String getAbsolutePath(const Base::String& aPath, const Base::String& aAbsModelPath);
    static bool removeDirContent(const Base::String& aDirName);
    static bool proj4Convert(const std::string& inProjection,
                             const std::string& outProjection,
                             const std::vector<Geom::Pnt>& inPoints,
                             std::vector<Geom::Pnt>& outPoints);

    static std::vector<Proj4> getProj4Converter();

    static void printCallStack(int maxFrames = 0);
    static bool runApp(const QString& appPath, std::map<QString, QString> env, std::vector<QString> args);


    static bool downloadFile(QString url, QString saveFilePath, QWidget* parent = 0, std::function<void(int, int)> callback = 0);
    static bool unzip(QString zipFile, QString destDir);

    static auto getHttpResponse(QString url, QWidget* parent = 0) ->std::pair<QString, QJsonDocument>;
};

}  // namespace Core