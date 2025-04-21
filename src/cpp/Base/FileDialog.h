#pragma once
#include <QStringList>  // for QString, QStringList
#include <QJsonDocument>

class QWidget;


namespace Base
{

    struct LX_BASE_EXPORT FileDialogCustomDesc
    {
        enum class TypeEnum
        {
            QLineEdit,
            QCheckBox,
            
        };

        
        
        QString name;
        TypeEnum type;
        QString label;
        QVariant defaultValue;
    };

    struct LX_BASE_EXPORT FileDialogCustomReturn
    {
        struct CustomValue
        {
            QString name;
            QVariant value;
            
        };

        QString filename;
        std::vector<CustomValue> customValues;

        QVariant getValue(QString name) 
        {
            for( auto p : customValues )
            {
                if (p.name == name)
                    return p.value;
            }
            
            return QVariant();
            
        }
            

        
        
    };
    

    
class FileDialog
{
public:

    

    
    LX_BASE_EXPORT static QString getSaveFileName(const QString& dir,
                                               const QString& filter = QString(),
                                               QWidget* parent = 0,
                                               const char* name = 0,
                                               const QString& caption = QString(),
                                               QString* selectedFilter = 0,
                                               bool resolveSymlinks = true);

	LX_BASE_EXPORT static FileDialogCustomReturn getOpenFileNameCustom(const QString& dir,
                                                              std::vector<FileDialogCustomDesc> desc,
                                                              const QString& filter = QString(),
                                                              QWidget* parent = 0,
                                                              const char* name = 0,
                                                              const QString& caption = QString(),
                                                              QString* selectedFilter = 0,
                                                              bool resolveSymlinks = true);
    
    LX_BASE_EXPORT static QString getOpenFileName(const QString& dir,
                                                  const QString& filter = QString(),
                                                  QWidget* parent = 0,
                                                  const char* name = 0,
                                                  const QString& caption = QString(),
                                                  QString* selectedFilter = 0,
                                                  bool resolveSymlinks = true);

    

    LX_BASE_EXPORT static QStringList getOpenFileNames(const QString& dir,
                                                    const QString& filter = QString(),
                                                    QWidget* parent = 0,
                                                    const char* name = 0,
                                                    const QString& caption = QString(),
                                                    QString* selectedFilter = 0,
                                                    bool resolveSymlinks = true);

    LX_BASE_EXPORT static QString getExistingDirectory(QWidget* parent = 0, const QString& caption = QString(), const QString& dir = QString());

    LX_BASE_EXPORT static QString getSaveFileName(QWidget* parent = 0,
                                               const QString& caption = QString(),
                                               const QString& dir = QString(),
                                               const QString& filter = QString(),
                                               QString* selectedFilter = 0);

    LX_BASE_EXPORT static QString getOpenFileName(QWidget* parent = 0,
                                               const QString& caption = QString(),
                                               const QString& dir = QString(),
                                               const QString& filter = QString(),
                                               QString* selectedFilter = 0);
};


}  // namespace Base
