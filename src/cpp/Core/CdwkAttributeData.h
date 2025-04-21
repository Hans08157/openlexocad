#pragma once

#include <Base/Color.h>
#include <Base/GlobalId.h>
#include <Geom/Ax2.h>


namespace Core
{
class LX_CORE_EXPORT CdwkAttributeData
{
public:
    CdwkAttributeData();
    ~CdwkAttributeData() = default;

    enum ElemType
    {
        BEAM,
        ROUND_BEAM,
        PLATE,
        NODE,
        BOLT,
        LINE,
        SURFACE,
        WALL,
        OPENING,
        ROOF,
        FLOOR,
        FASTENER
    };

    enum OutputType
    {
        OT_NONE = 0,
        OT_RAFTER = 1,         // = BEA_SPARREN,
        OT_PURLIN = 2,         // = BEA_PFETTE,
        OT_JACKRAFTER = 3,     // = BEA_SCHIFTER,
        OT_LOG = 4,            // = BEA_BLOCKBAU,
        OT_PANEL = 5,          // = BEA_PLATTE,
        OT_STUD = 6,           // = BEA_STIEL,
        OT_TRUSS = 7,          // = BEA_BINDER,
        OT_HIPVALLEY = 11,     // = BEA_GRAT,
        OT_USER1 = 20,         // = BEA_USER1,
        OT_USER2 = 21,         // = BEA_USER2,
        OT_USER3 = 22,         // = BEA_USER3,
        OT_USER4 = 23,         // = BEA_USER4,
        OT_USER5 = 24,         // = BEA_USER5,
        OT_STEP = 30,          // = BEA_STUFE,
        OT_COVERMASSIVE = 50,  // = BEA_COVER_MASSIVE,   // Hülle massiv
        OT_COVERPANEL = 51,    // = BEA_COVER_PANEL,  // Hülle Holzrahmenbau
        OT_COVERLOG = 52
    };


    Base::String name = L"";
    Base::String group = L"";
    Base::String subgroup = L"";
    Base::Color color = Base::Color(0, 255, 255);
    Geom::Ax2 lcs = Geom::Ax2(Geom::Pnt(0, 0, 0), Geom::Dir(0, 0, 1), Geom::Dir(1, 0, 0));
    ElemType element_type = BEAM;
    OutputType processing_type = OT_NONE;
    double supplement_drilling = 0.;
    double bolt_diameter = 0.;
    double length = 0.;
    double connectorHoleDiameter = 0.;
    double connectorThreadLength = 0.;
    double connectorSize = 0.;
    double buildingStoreyElevation = 0.;

    Base::String material_name = L"";
    Base::String comment = L"";
    Base::String sku = L"";  // stock-keeping-unit
    Base::String usertext_1 = L"";
    Base::String usertext_2 = L"";
    Base::String usertext_3 = L"";
    Base::String usertext_4 = L"";
    Base::String usertext_5 = L"";
    Base::String usertext_6 = L"";
    Base::String usertext_7 = L"";
    Base::String usertext_8 = L"";
    Base::String usertext_9 = L"";
    Base::String usertext_10 = L"";
    int material_id = -1;
    int production_nb = 0;

    Base::GlobalId IfcGuid;
    Base::String IfcBuilding = L"";
    Base::String IfcBuildingStorey = L"";
    Base::String IfcBuildingElement = L"";
    Base::String IfcConnectorItemType = L"";
    Base::String IfcLayer = L"";
    Base::String IfcEntityType = L"";

    // semi-regular
    /*explicit*/
    CdwkAttributeData(const CdwkAttributeData& other);

    CdwkAttributeData& operator=(const CdwkAttributeData& other);

    // regular
    friend bool LX_CORE_EXPORT operator==(const CdwkAttributeData& x, const CdwkAttributeData& y);
    friend bool LX_CORE_EXPORT operator!=(const CdwkAttributeData& x, const CdwkAttributeData& y);

    bool isEmpty() const;
};

}  // namespace Core
