#pragma once

#include <QString>

class QFileInfo;

namespace Core
{
class LX_CORE_EXPORT FileTool
{
public:
    /// Removes all non-ASCII characters in a path.
    static void removeNonAsciiCharactersInPath(QString& path);
    /// Removes all characters that are prohibited in a filename (not a path).
    static void removeInvalidCharactersInFilename(QString& filename);
    /// Callback for qSort to sort filenames naturally, taking numbers like numbers, not strings.
    static bool byNumberSortCallback(const QFileInfo& f1, const QFileInfo& f2);
    /// Callback to sort tutorial filenames naturally, taking numbers like numbers, not strings.
    static bool tutorialsByNumberSortCallback(const QFileInfo& f1, const QFileInfo& f2);
    /// For sorting catalog naturally, taking numbers like numbers, not strings, case insensitive.
    static bool catalogSortCallback(const QFileInfo& fi1, const QFileInfo& fi2);
    /// Returns number part of tutorial filename.
    static QString getTutorialsNumberPart(const QString& filename);
    /// Compare files
    static bool filesAreEqual(const QString& path1, const QString& path2);
};

}  // namespace Core
