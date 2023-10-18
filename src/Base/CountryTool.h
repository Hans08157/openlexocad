#pragma once
#include <QLocale.h>

namespace Base
{
class LX_BASE_EXPORT CountryTool
{
public:
    static void init();  // is called automatically

    static QLocale::Country getCountryByNumeric(int numeric);
    static QLocale::Country getCountryByAlpha2(const QString& alpha2);
    static QLocale::Country getCountryByAlpha3(const QString& alpha3);
    static QString getCountryName(QLocale::Country country);

private:
    static std::map<int, QLocale::Country> _numericCountry;
    static std::map<QString, QLocale::Country> _alpha2Country;
    static std::map<QString, QLocale::Country> _alpha3Country;
    static std::map<QLocale::Country, int> _countryTranslation;

    static void _register(QLocale::Country country, int numeric, QString alpha2, QString alpha3, int translatorId = -1);
};

}  // namespace Base
