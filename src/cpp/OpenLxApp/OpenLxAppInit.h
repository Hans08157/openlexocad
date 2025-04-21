#pragma once

#include <Base/Translator.h>

class QWidget;


namespace OpenLxApp
{
class LX_OPENLXAPP_EXPORT OpenLxAppInit
{
public:
    OpenLxAppInit() {}
    ~OpenLxAppInit() {}

public:
    static void init();
    static int initFromCadwork3d(QWidget* aMainWindow, CTranslator::Language aLanguage);
    static void release();

private:
    static bool isInit;
};

}  // namespace OpenLxApp


extern "C" LX_OPENLXAPP_EXPORT int initOpenLxAppFromCadwork3d(QWidget* aMainWindow, int aLanguage);