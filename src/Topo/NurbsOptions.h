#pragma once

#include <Topo/Types.h>
#include <Geom/Dir.h>

namespace Topo
{
// SB - Acis options about skinning are a little bit "unclear". There are different methods to skin wires, but not all methods accept all parameters,
// that's why I'm trying to make different classes, each one that fits only a particular method, with only the parameters that are taken into account.
class LX_TOPO_EXPORT NurbsOptions
{
protected:
    NurbsOptions() = default;
    virtual ~NurbsOptions() = default;
};

/*
 * Topo::SkinningOptions
 */
class LX_TOPO_EXPORT SkinningOptions : public NurbsOptions
{
public:
    SkinningOptions();
    ~SkinningOptions() override = default;

    void setWiresU(const std::vector<pConstShape>& in);
    void setWiresU(const std::vector<pConstWire>& in);
    std::vector<pConstWire> getWiresU() const;

    enum class ClosedMode
    {
        Open = 0,
        Closed = 1,
        Loop = 2,
        Solid = 3
    };

    void setClosedMode(const ClosedMode& mode);
    ClosedMode getClosedMode() const;

    void setFlatShapes(bool force);

    void setSolid(bool solid);
    bool getSolid() const;

    void setUniformUV(bool uniform);
    bool getArcLen() const;
    bool getArcLenU() const;

    // These values are intentionally "readonly", since it is not clear when it would be useful to alter them.
    bool getAllowUV() const;
    bool getMerge() const;
    bool getSelfIntersect() const;
    bool getSimplify() const;

protected:

    bool _allowSameUv = true;     // SB 2011.12.16 - Very special case! http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Surface_Checks#allow_same_uv_.28false.29
    bool _arcLength = true;        // SB 2013.05.07 - http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Surface_Parameterization
    bool _arcLengthU = true;
    ClosedMode _closedMode = ClosedMode::Open;
    bool _forceFlatShapes = false;
    bool _mergeWireCoEdges = false;
    bool _selfIntTest = false;    // SB 2012.06.05 - When FALSE allow creation of self-intersecting surfaces: http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Surface_Checks#self_int_test_.281.29
                                    // No exception is thrown, NURBS is created (probably rubbish) and "selfIntersect" property can be detected later.
    bool _simplify = false;         // SB 2012.06.14 - Leave to FALSE or ACIS will try to build a simpler surface (if possible). For example, if set to TRUE and the
                                    // surface is exactly a cylinder, ACIS will not make a NURBS but a cylinder and the "api_accurate_bs3_approximation" won't work! See
                                    // http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Simplification

    std::vector<pConstWire> _uWires = {};

    void setWires(std::vector<pConstWire>& u_or_vWires, const std::vector<pConstShape>& in);
};

/*
 * Topo::BasicSkinningOptions
 */
class LX_TOPO_EXPORT BasicSkinningOptions final : public SkinningOptions
{
public:
    BasicSkinningOptions();
    ~BasicSkinningOptions() override = default;
};

/*
 * Topo::DraftSkinningOptions
 */
class LX_TOPO_EXPORT DraftSkinningOptions final : public SkinningOptions
{
public:
    DraftSkinningOptions();
    ~DraftSkinningOptions() override = default;

    enum class GapMode
    {
        Extended = 0,
        Rounded = 1,
        Chamfered = 2
    };  // SB - Pls match values in "skin_opts.hxx" => skin_gap_type

    void setGapMode(GapMode mode);
    GapMode getGapMode() const;

    double endAngle = 0.;
    double endMagnitude = 0.;
    double startAngle = 0.;
    double startMagnitude = 0.;

protected:
    GapMode _gapMode = GapMode::Extended;
};

/*
 * Topo::GuideSkinningOptions
 */
class LX_TOPO_EXPORT GuideSkinningOptions final : public SkinningOptions
{
public:
    GuideSkinningOptions();
    ~GuideSkinningOptions() override = default;

    void setWiresV(const std::vector<pConstShape>& in);
    void setWiresV(std::vector<pConstWire> in);
    std::vector<pConstWire> getWiresV() const;

    void setVirtualGuides(const bool& virtualGuides);
    bool getVirtualGuides() const;

protected:
    bool _virtualGuides = false;  // SB 2012.05.07 - http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Guide-related

    std::vector<pConstWire> _vWires = {};
};

/*
 * Topo::LinearSkinningOptions
 */
class LX_TOPO_EXPORT LinearSkinningOptions final : public SkinningOptions
{
public:
    LinearSkinningOptions();
    ~LinearSkinningOptions() override = default;
};

/*
 * Topo::PathSkinningOptions
 */
class LX_TOPO_EXPORT PathSkinningOptions final : public SkinningOptions
{
public:
    PathSkinningOptions();
    ~PathSkinningOptions() override = default;

    void setPath(pConstWire in);
    pConstWire getPath() const;

protected:
    pConstWire _path = nullptr;
};

/*
 * Topo::PlanarSkinningOptions
 */
class LX_TOPO_EXPORT PlanarSkinningOptions final : public SkinningOptions
{
public:
    PlanarSkinningOptions();
    ~PlanarSkinningOptions() override = default;

    enum class NormalsMode
    {
        First = 0,
        Last = 1,
        Ends = 2,
        All = 3
    };  // SB - Pls match values in "skin_opts.hxx" => skinning_normals

    void setNormalsMode(NormalsMode mode);
    NormalsMode getNormalsMode() const;

protected:
    NormalsMode _normalsMode = NormalsMode::All;
};

/*
 * Topo::SweepingOptions
 */
class LX_TOPO_EXPORT SweepingOptions : public NurbsOptions
{
public:
    SweepingOptions();
    ~SweepingOptions() override = default;

    void setShapeU(pConstShape in);
    void setShapeU(pConstFace in);
    void setShapeU(pConstWire in);
    pConstShape getShapeU() const;

    void setToFace(pConstFace face);
    pConstFace getToFace() const;

    void setSolid(const bool& solid);
    bool getSolid() const;

    void setSelfIntersect(const bool& allowSelfIntersect);
    bool getSelfIntersect() const;

    // This value is intentionally "readonly", since it is not clear when it would be useful to alter them.
    bool getSimplify() const;

protected:
    bool _selfIntTest = false;  // SB 2012.06.05 - When FALSE allow creation of self-intersecting surfaces:
                                // http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Surface_Checks#self_int_test_.281.29. No exception is
                                // thrown, NURBS is created (probably rubbish) and "selfIntersect" property can be detected later.
    bool _simplify =    false;  // SB 2012.06.14 - Leave to FALSE or ACIS will try to build a simpler surface (if possible). For example, if set to TRUE and the
                                // surface is exactly a cylinder, ACIS will not make a NURBS but a cylinder and the "api_accurate_bs3_approximation" won't work! See
                                // http://doc.spatial.com/index.php/Skinning_and_Lofting_Options/Simplification
    bool _solid = false;

    pConstShape _uShape = nullptr;
    pConstFace _toFace = nullptr;
};

class LX_TOPO_EXPORT VectorSweepingOptions final : public SweepingOptions
{
public:
    VectorSweepingOptions();
    ~VectorSweepingOptions() override = default;

    void setVector(const Geom::Vec& vec);
    Geom::Vec getVector() const;

protected:
    Geom::Vec _vec;
};

/*
 * Topo::PathSweepingOptions
 */
class LX_TOPO_EXPORT PathSweepingOptions final : public SweepingOptions
{
public:
    PathSweepingOptions();
    ~PathSweepingOptions() override = default;

    void setShapeV(pConstShape in);
    void setShapeV(pConstWire in);
    pConstShape getShapeV() const;

    void setFinalTwistAngle(double angleInDeg);
    double getFinalTwistAngle() const;

    void setRigid(bool rigid);
    bool getRigid() const;

    void setUseRail(bool rail, const Geom::Dir& railDir = Geom::Dir::ZDir());
    bool getUseRail(Geom::Dir& railDir) const;

protected:
    double _finalTwistAngle = 0.;
    bool _rail = false;
    Geom::Dir _railDir = Geom::Dir::ZDir();
    bool _rigid = false;

    pConstShape _vShape = nullptr;
};

class LX_TOPO_EXPORT PathExtrusionFixVerticalOptions final : public NurbsOptions
{
public:
    PathExtrusionFixVerticalOptions();
    ~PathExtrusionFixVerticalOptions() override = default;

    void setProfile(pConstFace in);
    void setProfile(const pConstWire& in);
    pShape getProfile() const;

    void setPath(pConstWire in);
    pConstWire getPath() const;

    void addDebugShape(pShape shape);
    std::vector<pShape> getDebugShapes() const;

    void setSolutionType(int value);
    int getSolutionType() const;

private:
    std::vector<pShape> _debugShapes;

    int _solutionType = 1; // <- This parameter allows for different solutions, achieved by adding intermediate profiles at specific positions

    pFace _uFace = nullptr;
    pWire _uWire = nullptr;

    pWire _vWire = nullptr;
};
}
