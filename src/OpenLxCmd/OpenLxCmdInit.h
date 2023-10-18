#pragma once


/** @defgroup OPENLX_CMD Commands
 */

namespace OpenLxCmd
{
class LX_OPENLXCMD_EXPORT OpenLxCmdInit
{
public:
    OpenLxCmdInit() {}
    ~OpenLxCmdInit() {}

public:
    static void init();
    static void release();

private:
    static bool isInit;
};

}  // namespace OpenLxCmd
