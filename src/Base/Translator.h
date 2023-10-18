/**
 * @file
 * CTranslator class header.
 *
 * @author Martin "martyn" Havlíèek and Petr "zero" Maštera
 */
#pragma once
#include <QLocale>
#include <map>

//----------------------------------------------------------------------------
// DECLARATIONs
//----------------------------------------------------------------------------

/**
 * Translator provides translated version of the string identified by the
 * unique ID.
 */
class LX_BASE_EXPORT CTranslator
{
public:
    /** Supported languages enumeration. */
    enum Language
    {
        ENGLISH,    /**<  [0] English is the default language. */
        GERMAN,     /**<  [1] German. */
        FRENCH,     /**<  [2] French. */
        SPANISH,    /**<  [3] Spanish. */
        PORTUGUESE, /**<  [4] Portuguese. */
        ROMANIAN,   /**<  [5] Romanian. */
        HUNGARIAN,  /**<  [6] Hungarian. */
        RUSSIAN,    /**<  [7] Russian. */
        POLISH,     /**<  [8] Polish. */
        ITALIAN,    /**<  [9] Italian. */
        CZECH,      /**< [10] Czech. */
        UKRAINE     /**< [11] Ukraine. */
    };

    typedef QMap<QString, int> CustomTranslationsTable;

public:
    static QString get(int id, bool forceEnglish = false);
    static QString getSpecial(int id, bool forceEnglish = false);

    /* convenience method, lookup for the english word, get the id and return the current translation */
    static QString getByEnglish(QString eng);
    static QStringList getInAllLanguages(int id);

    static void setLanguage(Language lang);
    static Language getLanguage();
    static QString getLanguageAsString();
    static void setLanguageFromString(const QString& lang);

    static CustomTranslationsTable readCustomTranslationsTable(const QString& filename);
    static QString translate(const CustomTranslationsTable& table, const QString& source, bool emptyIfNotInTable = false);

    static void showMessageId(bool onoff);
    static bool messageIdVisible();

    static QString getCdwkStringFromLanguage(Language lang);
    static Language getLanguageFromCdwkString(const QString& lang);

    static QLocale getQLocale();

    static QString getTranslatorDirPath();

private:
    /** Singleton instance. */
    static CTranslator& Instance();
    static class QTranslator _qtinstance;
    static void setQTranslatorLanguage(Language lang);

    /** Currently selected language. */
    Language _lang = ENGLISH;

    /** List of German strings. */
    // QStringList _de;
    std::map<int, QString> _de;
    /** List of English strings. */
    // QStringList _en;
    std::map<int, QString> _en;
    /** List of French strings. */
    // QStringList _fr;
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

    // QStringList reverse_en;
    std::map<QString, int> _reverse_en;

    struct Flags
    {
        bool html;
    };
    /** List of flags saying whether the message should be parsed for HTML.*/
    std::map<int, Flags> _flags;

    bool _showMessageId = false;

    // internal private methods
    CTranslator();

    void init();

    bool loadFile(Language lang);

    static QString _getPathToTranslation(wchar_t* dllName);
};
