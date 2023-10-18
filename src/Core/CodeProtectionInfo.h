#pragma once

#include <array>
#include <Core/cw32_extendedInfoType.h>
namespace Core
{

    struct LX_CORE_EXPORT CodeProtectionInfo
    {
        CodeProtectionInfo();
        CodeProtectionInfo(const CodeExtendedInfoType& flags);


        QString displayName;
        QString SW_ID;
        QString LicenseName;
        QString Code_Valid;
        QString CODE_NORM;
        QString CODE_DEMO;
        std::array<char, 129> OPTION;
        std::array<char, 129> OPTION2;
        int NB_DAY_UNTIL_EXPIRATION;
        QString DATE_LIM;
        QString Node_Dir;
        int floatingLicense;
        int dataValid;
        int webLicense;

        int errValue;
        
        void initFromFlags(const CodeExtendedInfoType& flags);
        void reset();

        enum class weblicensestate
        {
            S_OKAY = 0,
            NOT_ACTIVATED,
            LICENSE_ALREADY_IN_USE,  // weblicense is in use by another computer/user
            UNKNOWN_ERROR
        };

        // New Weblicense
        struct LX_CORE_EXPORT weblicense
        {            
            QString weblicense_id;
            QString valid_until;
            QString date_server;
            QString license_is_in_use_by;            
            QString errorstring;
            int errorcode;
            
            QString current_login;
            QString current_biosID;
            QString current_message;

            weblicensestate state;  

            bool isOkay() const;

            

            
        } newWebLicense;
        

    };
}  // namespace Core
