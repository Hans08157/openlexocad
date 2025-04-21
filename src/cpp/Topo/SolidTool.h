#pragma once

#include <Topo/Types.h>
#include <Geom/Pnt.h>

namespace Topo
{
/**
 * @brief Tools for creating, manipulating and querying Solids.
 *
 * @ingroup TOPO_SHAPETOOLS
 */

class LX_TOPO_EXPORT SolidTool
{
public:
    SolidTool(void);
    virtual ~SolidTool(void);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // --------------------- BEGIN API --------------------- //
    //                                                       //
    // ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
    //                                                       //
    ///////////////////////////////////////////////////////////

    // Makes a solid from a model description and a vector of points
    static pSolid makeSolid(const std::vector<int>& model,
                            const std::vector<Geom::Pnt>& vertices,
                            std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    // Makes a solid from a model description and a vector of points
    static pSolid makeSolid_by_Face_stiching(const std::vector<int>& model,
                                             const std::vector<Geom::Pnt>& vertices,
                                             std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    /// Makes a solid from a closed shape. Returns nullptr on failure.
    static pSolid makeSolid(pConstShape shape);
    /// Returns centre of mass (centre of gravity) of the solid
    static Geom::Pnt getCentre(pConstSolid solid);
    // Makes a box
    static pSolid makeBox(double length, double width, double height);
    // Makes a box
    static pSolid makeCylinder(double radius, double height);

    // Makes a shape of a 4-angle-roof
    static pSolid
    makeFourAngleRoof(double length, double width, double height, double leftSlope, double rightSlope, double leftHipSlope, double rightHipSlope);
    // Makes a shape of a hip roof with wall
    static pSolid makeHipRoofWithWall(double length, double width, double height, double wallHeight, double slope, double hipSlope, bool halfRoof);
    // Makes a shape of roof and opening with beveled bottom and/or upper faces
    static pSolid makeBeveledPlate(double length, double width, double height, int bottomType, int upperType, double slope, double angleRot);
    // Makes shape of stairs ascending in U-shape
    static pSolid makeStairsU(double length,
                              double width,
                              double height,
                              double stepWidth,
                              const std::vector<Geom::Pnt>& points,
                              const std::vector<double>& angles,
                              bool mirrored);
    // Makes shape of stairs ascending in L-shape
    static pSolid makeStairsL(double length,
                              double width,
                              double height,
                              double stepWidth,
                              const std::vector<Geom::Pnt>& points,
                              const std::vector<double>& angles,
                              bool mirrored);
    // Makes shape of stairs ascending in I-shape
    static pSolid makeStairsI(double length, double width, double height, const std::vector<Geom::Pnt>& points);
    // Makes shape of arch, intended in particular for windows
    static pSolid makeWindowArch(double majorRadius, double minorRadius, double frameWidth, double sectorWidth, double depth, bool cutOut = true);

    ///////////////////////////////////////////////////////////
    //                                                       //
    // ---------------------- END API ---------------------- //
    //                                                       //
    ///////////////////////////////////////////////////////////

#ifndef LXAPI  // INTERFACES BELOW ARE -NOT- PART OF THE LEXOCAD API
               /// @cond INTERNAL
               /// Sets the default SolidTool. For internal use only.
    static void __setDefaultSolidTool__(Topo::SolidTool* tool) { _defaultTool = tool; }

protected:
    virtual pSolid _makeSolid(const std::vector<int>& model,
                              const std::vector<Geom::Pnt>& vertices,
                              std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    virtual pSolid _makeSolid_by_Face_stiching(const std::vector<int>& model,
                                               const std::vector<Geom::Pnt>& vertices,
                                               std::vector<std::vector<Geom::Pnt> >& defectPolygons);
    virtual pSolid _makeSolid(pConstShape shape);
    virtual pSolid _makeCylinder(double radius, double height);
    virtual Geom::Pnt _getCentre(pConstSolid solid);
    virtual pSolid
    _makeFourAngleRoof(double length, double width, double height, double leftSlope, double rightSlope, double leftHipSlope, double rightHipSlope);
    virtual pSolid _makeHipRoofWithWall(double length, double width, double height, double wallHeight, double slope, double hipSlope, bool halfRoof);
    virtual pSolid _makeBeveledPlate(double length, double width, double height, int bottomType, int upperType, double slope, double angleRot);
    virtual pSolid _makeStairsU(double length,
                                double width,
                                double height,
                                double stepWidth,
                                const std::vector<Geom::Pnt>& points,
                                const std::vector<double>& angles,
                                bool mirrored);
    virtual pSolid _makeStairsL(double length,
                                double width,
                                double height,
                                double stepWidth,
                                const std::vector<Geom::Pnt>& points,
                                const std::vector<double>& angles,
                                bool mirrored);
    virtual pSolid _makeStairsI(double length, double width, double height, const std::vector<Geom::Pnt>& points);
    virtual pSolid _makeWindowArch(double majorRadius, double minorRadius, double frameWidth, double sectorWidth, double depth, bool cutOut);

    static Topo::SolidTool* _defaultTool;
    /// @endcond
#endif
};

}  // namespace Topo