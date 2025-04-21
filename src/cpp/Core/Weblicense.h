#pragma once

#include <QString>
namespace  Core
{

	struct LX_CORE_EXPORT WeblicenseResponse
	{
        int error_code = 0;		
        QString error_message = "";
        QString license_is_in_use_by = "";
        QString message_from_server;

		bool isOK() const;
        bool isInUseByAnotherUser() const;
        bool isNotActivated() const;
        bool isNoLicenseFound() const;
        bool isOffline() const;

		
	};

    enum class logLevel
    {
        debug,
        info,
        trace,
        warn,
        critical,
        error,
        off
        

    };

	
	struct LX_CORE_EXPORT Weblicense
	{	
		static QString getLastActivatedWeblicenseID();
        static QString getCurrentDisplay();
        static QString getLoginName();
        static WeblicenseResponse forcedeactivateLicense(int applicationversion_main, int revision_number, QString weblicense_id, QString password);
        static WeblicenseResponse deactivateLicense(int applicationversion_main, int revision_number);
        static WeblicenseResponse activateLicense(int applicationversion_main, int revision_number, QString weblicense_id, QString password);
        static WeblicenseResponse getCode(int applicationversion_main, int revision_number, QString weblicense_id);
		
		static void enableWeblicense(bool enable);
        static bool isWeblicenseEnabled();

        static void saveSetting(QString key, QString value);
        static QString getSetting(QString key);

        static void log(logLevel level, QString message);
        static void setLogLevel(logLevel level);

        static QString getReport(int applicationversion_main);
        static QString getLogFileContent();
        
	};
}

