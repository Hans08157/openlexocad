#pragma once
#include <QFile>
#include <QTextStream>

namespace Base
{
class LX_BASE_EXPORT CsvTool
{
public:
    CsvTool() = default;

    bool writeCsv(const std::vector<std::vector<QString>>& table, const QString& path, QWidget* widget);

    bool openForReading(const QString& fileName);
    bool readLine(std::vector<QString>& items);

    bool openForWriting(const QString& fileName);
    bool writeLine(const std::vector<QString>& items);

    void setSeparator(QChar separator) { _separator = separator; }
    bool seek(int64_t pos);
    QChar guessSeparator();
    QString fileName() const;

    static QString cleanNumber(const QString& text);

private:
    QFile _file;
    QTextStream _ts;
    QChar _separator = ';';
};

}  // namespace Base