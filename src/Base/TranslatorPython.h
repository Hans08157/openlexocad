#pragma once
#include <Base/Translator.h>

/**
 * Translator provides translated version of the string identified by the
 * unique ID.
 */
class LX_BASE_EXPORT PTranslator
{
public:
    typedef QMap<QString, int> CustomTranslationsTable;

    static QString get(int id, bool forceEnglish = false);
    static QString getSpecial(int id, bool forceEnglish = false);
    static QStringList getInAllLanguages(int id);

    static void setLanguage(CTranslator::Language lang);
    static CTranslator::Language getLanguage();
    static QString getLanguageAsString();
    static void setLanguageFromString(const QString& lang);

    static CustomTranslationsTable readCustomTranslationsTable(const QString& filename);
    static QString translate(const CustomTranslationsTable& table, const QString& source, bool emptyIfNotInTable = false);

    static void showMessageId(bool onoff);
    static void showCodeId(bool onoff);

    static QString getCdwkStringFromLanguage(CTranslator::Language lang);
    static CTranslator::Language getLanguageFromCdwkString(const QString& lang);

private:
    static class QTranslator _qtinstance;
    static void setQTranslatorLanguage(CTranslator::Language lang);
    static PTranslator& Instance();

    /** Currently selected language. */
    CTranslator::Language _lang;

    /** List of German strings. */
    std::map<int, QString> _de;
    /** List of English strings. */
    std::map<int, QString> _en;
    /** List of French strings. */
    std::map<int, QString> _fr;
    /** List of Spanish strings. */
    std::map<int, QString> _sp;
    /** List of Portuguese strings. */
    std::map<int, QString> _po;
    /** List of Romanian strings. */
    std::map<int, QString> _ro;
    /** List of Hungarian strings. */
    std::map<int, QString> _hu;
    /** List of Russian strings. */
    std::map<int, QString> _ru;
    /** List of Polish strings. */
    std::map<int, QString> _pl;
    /** List of Italian strings. */
    std::map<int, QString> _it;
    /** List of Czech strings. */
    std::map<int, QString> _cz;
    /** List of Ukranine strings. */
    std::map<int, QString> _uk;

    // Note: when adding new language, don't forget to modify getInAllLanguages(). -mh-

    struct Flags
    {
        bool html;
        QString code;
    };

    /** List of flags saying whether the message should be parsed for HTML. And list of protection codes.*/
    std::map<int, Flags> _flags;

    bool _showMessageId = false;
    bool _showCodeId = false;

    // internal private methods
    PTranslator();

    void init();

    bool loadFile(CTranslator::Language lang);

    QString _getPathToTranslation(wchar_t* dllName) const;
};
