
/**
 * @file
 * GUIInterface class declaration.
 *
 */

#pragma once 

#include <string>


namespace Core
{
/**
 *
 *
 */
class LX_CORE_EXPORT GUIInterface
{
public:
    // bottom bar interface
    //
    virtual void bottomBar_showIdleMessage() = 0;
    virtual void bottomBar_showMessage(std::string message) = 0;
    virtual void bottomBar_showMessage(int id) = 0;
    virtual void bottomBar_showPrompt(std::string mess, double default_value = 0.0) = 0;
    virtual void bottomBar_showPrompt(int mess_id, double default_value = 0.0) = 0;
    virtual void bottomBar_eraseInput() = 0;



    // translator interface
    //
    virtual std::string translator_get(int id, bool forceEnglish = false) = 0;


    // common interface
    //
    virtual void uncheckMainToolbar() = 0;
    virtual void uncheckAll() = 0;


    // dialog interface
    //
    virtual std::string getOpenFileName(const char* title, const char* filter = nullptr, const char* selectedFilter = NULL) = 0;
    virtual std::string getSaveFileName(const char* title, const char* filter = nullptr, const char* selectedFilter = NULL) = 0;
    virtual int msgBox_critical(const char* title, const char* text) = 0;
    virtual int msgBox_warning(const char* title, const char* text) = 0;
    virtual int msgBox_info(const char* title, const char* text) = 0;
};



}  // namespace Core
