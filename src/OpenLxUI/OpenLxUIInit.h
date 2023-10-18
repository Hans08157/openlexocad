#pragma once



namespace OpenLxUI
{
class LX_OPENLXUI_EXPORT OpenLxUIInit
{
public:
    OpenLxUIInit() {}
    ~OpenLxUIInit() {}

public:
    static void init();
    static void release();

private:
    static bool isInit;
};

}  // namespace OpenLxUI
