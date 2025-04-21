#pragma once

namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Shells.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT ShellTool
{
public:
    ShellTool(void);
    virtual ~ShellTool(void);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    // TODO

    // static pShell makeShell( const std::vector<pFace>& faces);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////


protected:
    // virtual pShell _makeShell( const std::vector<pFace>& faces);
    static Topo::ShellTool* _defaultTool;

    /// @endcond
};

}  // namespace Topo