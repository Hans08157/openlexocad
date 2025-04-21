#pragma once

#include <QString>

#ifdef GRAY
#undef GRAY
#endif

#ifdef INCH
#undef INCH
#endif

namespace Base
{
enum class SIPrefix
{
    EXA,    // 10^18
    PETA,   // 10^15
    TERA,   // 10^12
    GIGA,   // 10^9
    MEGA,   // 10^6
    KILO,   // 10^3
    HECTO,  // 10^2
    DECA,   // 10.
    NONE,   // 1.
    DECI,   // 10^-1
    CENTI,  // 10^-2
    MILLI,  // 10^-3
    MICRO,  // 10^-6
    NANO,   // 10^-9
    PICO,   // 10^-12
    FEMTO,  // 10^-15
    ATTO    // 10^-18
};

enum class SIUnitName
{
    AMPERE,
    BECQUEREL,
    CANDELA,
    COULOMB,
    CUBIC_METRE,
    DEGREE_CELSIUS,
    FARAD,
    GRAM,
    GRAY,
    HENRY,
    HERTZ,
    JOULE,
    KELVIN,
    LUMEN,
    LUX,
    METRE,
    MOLE,
    NEWTON,
    OHM,
    PASCAL_UNIT,  // "PASCAL" causes weird problems when included in GUI dll
    RADIAN,
    SECOND,
    SIEMENS,
    SIEVERT,
    SQUARE_METRE,
    STERADIAN,
    TESLA,
    VOLT,
    WATT,
    WEBER
};

enum class Quantity
{
    // has base SI units (http://en.wikipedia.org/wiki/SI_base_unit)
    AMOUNT_OF_SUBSTANCE,
    ELECTRIC_CURRENT,
    LENGTH,
    LUMINOUS_INTENSITY,
    MASS,
    TIME,
    THERMODYNAMIC_TEMPERATURE,

    // has named SI derived units (http://en.wikipedia.org/wiki/SI_derived_unit)
    ABSORBED_DOSE,
    CATALYTIC_ACTIVITY,
    ELECTRIC_CAPACITANCE,
    ELECTRIC_CHARGE,
    ELECTRIC_RESISTANCE,
    ELECTRICAL_CONDUCTANCE,
    ELECTRICAL_POTENTIAL_DIFFERENCE,
    ELECTROMOTIVE_FORCE,
    ENERGY,
    EQUIVALENT_DOSE,
    FORCE,
    FREQUENCY,
    HEAT,
    ILLUMINANCE,
    IMPEDANCE,
    INDUCTANCE,
    LUMINOUS_FLUX,
    MAGNETIC_FIELD,
    MAGNETIC_FLUX,
    PLANE_ANGLE,
    POWER,
    PRESSURE,
    RADIANT_FLUX,
    RADIOACTIVITY,
    REACTANCE,
    SOLID_ANGLE,
    STRESS,
    TEMPERATURE,
    VOLTAGE,
    WEIGHT,
    WORK,

    // has compound units (http://en.wikipedia.org/wiki/SI_derived_unit)
    AREA,
    MASS_DENSITY,
    AREA_DENSITY,
    VOLUME

    // this last chapter is not complete, more can be found on the URL above
};

LX_BASE_EXPORT std::string getPrefixSymbol(Base::SIPrefix prefix);



class LX_BASE_EXPORT LengthUnit
{
public:
    enum LengthUnitEnum
    {
        METRE = 0,
        MILLIMETRE = 1,
        FOOT = 2,
        INCH = 3,
        CENTIMETRE = 4
    };

    LengthUnit();
    LengthUnit(double value, LengthUnitEnum unit = METRE);
    ~LengthUnit();

    void setValue(double value, LengthUnitEnum unit = METRE);

    static QString getSymbolFromUnit(LengthUnitEnum unit);
    static LengthUnitEnum getUnitFromSymbol(const QString& symbol);
    static LengthUnitEnum getDefaultUnit();
    static bool isImperial(LengthUnitEnum unit);

    double getIn(LengthUnitEnum unit);
    double getInMetre(Base::SIPrefix prefix = Base::SIPrefix::NONE);
    double getInMilliMetre();
    double getInCentiMetre();
    double getInFoot();
    double getInInch();

private:
    double _foot2Metre(double value);
    double _inch2Metre(double value);
    double _metre2Foot(double value);
    double _metre2Inch(double value);

    /// internal always in metre
    double _value;
};

class LX_BASE_EXPORT PlaneAngleUnit
{
public:
    enum PlaneAngleUnitEnum
    {
        RADIAN = 0,
        DEGREE = 1,
        GON = 2,
        PERCENT = 3,
        PERMILLE = 4,
        V_H = 5
    };

    PlaneAngleUnit();
    PlaneAngleUnit(double value, PlaneAngleUnitEnum unit = DEGREE);
    ~PlaneAngleUnit();

    void setValue(double value, PlaneAngleUnitEnum unit = DEGREE);

    static QString getSymbolFromUnit(PlaneAngleUnitEnum unit);
    static PlaneAngleUnitEnum getUnitFromSymbol(const QString& symbol);
    static PlaneAngleUnitEnum getDefaultUnit();
    static bool isImperial(PlaneAngleUnitEnum unit);

    double getIn(PlaneAngleUnitEnum unit);
    double getInRadian();
    double getInDegree();
    double getInGon();
    double getInPercent();
    double getInPermille();
    double getInVH();

private:
    double _degree2Radian(double value);
    double _gon2Radian(double value);
    double _percent2Radian(double value);
    double _permille2Radian(double value);
    double _vh2Radian(double value);
    double _radian2Degree(double value);
    double _radian2Gon(double value);
    double _radian2Percent(double value);
    double _radian2Permille(double value);
    double _radian2Vh(double value);

    /// internal always in radian
    double _value;
};

class LX_BASE_EXPORT AreaUnit
{
public:
    enum AreaUnitEnum
    {
        SQUARE_METRE = 0,
        SQUARE_FOOT = 1,
        SQUARE_MILLIMETRE = 2,
        SQUARE_CENTIMETRE = 3
    };

    AreaUnit();
    AreaUnit(double value, AreaUnitEnum unit = SQUARE_METRE);
    ~AreaUnit();

    void setValue(double value, AreaUnitEnum unit = SQUARE_METRE);

    static QString getSymbolFromUnit(AreaUnitEnum unit);
    static AreaUnitEnum getUnitFromSymbol(const QString& symbol);
    static AreaUnitEnum getDefaultUnit();
    static bool isImperial(AreaUnitEnum unit);

    double getIn(AreaUnitEnum unit);
    double getInSquareMetre();
    double getInSquareMilliMetre();
    double getInSquareCentiMetre();
    double getInSquareFoot();

private:
    double _squareFoot2SquareMetre(double value);
    double _squareMetre2SquareFoot(double value);

    /// internal always in square metre
    double _value;
};

class LX_BASE_EXPORT VolumeUnit
{
public:
    enum VolumeUnitEnum
    {
        CUBIC_METRE = 0,
        BOARD_FOOT = 1,
        CUBIC_FOOT = 2,
        CUBIC_MILLIMETRE = 3,
        CUBIC_CENTIMETRE = 4
    };

    VolumeUnit();
    VolumeUnit(double value, VolumeUnitEnum unit = CUBIC_METRE);
    ~VolumeUnit();

    void setValue(double value, VolumeUnitEnum unit = CUBIC_METRE);

    static QString getSymbolFromUnit(VolumeUnitEnum unit);
    static VolumeUnitEnum getUnitFromSymbol(const QString& symbol);
    static VolumeUnitEnum getDefaultUnit();
    static bool isImperial(VolumeUnitEnum unit);

    double getIn(VolumeUnitEnum unit);
    double getInCubicMetre();
    double getInCubicMilliMetre();
    double getInCubicCentiMetre();
    double getInBoardFoot();
    double getInCubicFoot();

private:
    double _boardFoot2CubicMetre(double value);
    double _cubicFoot2CubicMetre(double value);
    double _cubicMetre2BoardFoot(double value);
    double _cubicMetre2CubicFoot(double value);

    /// internal always in cubic metre
    double _value;
};

class LX_BASE_EXPORT MassUnit
{
public:
    enum MassUnitEnum
    {
        KILOGRAM = 0,
        TONNE = 1,
        POUND = 2
    };

    MassUnit();
    MassUnit(double value, MassUnitEnum unit = KILOGRAM);
    ~MassUnit();

    void setValue(double value, MassUnitEnum unit = KILOGRAM);

    static QString getSymbolFromUnit(MassUnitEnum unit);
    static MassUnitEnum getUnitFromSymbol(const QString& symbol);
    static MassUnitEnum getDefaultUnit();
    static bool isImperial(MassUnitEnum unit);

    double getIn(MassUnitEnum unit);
    double getInKilogram();
    double getInTonne();
    double getInPound();

private:
    double _tonne2Kilogram(double value);
    double _pound2Kilogram(double value);
    double _kilogram2Tonne(double value);
    double _kilogram2Pound(double value);

    /// internal always in kilogram
    double _value;
};

class LX_BASE_EXPORT MassDensityUnit
{
public:
    enum MassDensityUnitEnum
    {
        KILOGRAM_CUBICMETRE = 0,
        TONNE_CUBICMETRE = 1,
        POUND_CUBICFOOT = 2
    };

    MassDensityUnit();
    MassDensityUnit(double value, MassDensityUnitEnum unit = KILOGRAM_CUBICMETRE);
    ~MassDensityUnit();

    void setValue(double value, MassDensityUnitEnum unit = KILOGRAM_CUBICMETRE);

    static QString getSymbolFromUnit(MassDensityUnitEnum unit);
    static MassDensityUnitEnum getUnitFromSymbol(const QString& symbol);
    static MassDensityUnitEnum getDefaultUnit();
    static bool isImperial(MassDensityUnitEnum unit);

    double getIn(MassDensityUnitEnum unit);
    double getInKilogramCubicMetre();
    double getInTonneCubicMetre();
    double getInPoundCubicFoot();

private:
    double _tonneCubicMetre2KilogramCubicMetre(double value);
    double _poundCubicFoot2KilogramCubicMetre(double value);
    double _kilogramCubicMetre2TonneCubicMetre(double value);
    double _kilogramCubicMetre2PoundCubicFoot(double value);

    /// internal always in kilogram/m3
    double _value;
};

class LX_BASE_EXPORT AreaDensityUnit
{
public:
    enum AreaDensityUnitEnum
    {
        KILOGRAM_SQUAREMETRE = 0,
        TONNE_SQUAREMETRE = 1,
        POUND_SQUAREFOOT = 2
    };

    AreaDensityUnit();
    AreaDensityUnit(double value, AreaDensityUnitEnum unit = KILOGRAM_SQUAREMETRE);
    ~AreaDensityUnit();

    void setValue(double value, AreaDensityUnitEnum unit = KILOGRAM_SQUAREMETRE);

    static QString getSymbolFromUnit(AreaDensityUnitEnum unit);
    static AreaDensityUnitEnum getUnitFromSymbol(const QString& symbol);
    static AreaDensityUnitEnum getDefaultUnit();
    static bool isImperial(AreaDensityUnitEnum unit);

    double getIn(AreaDensityUnitEnum unit);
    double getInKilogramSquareMetre();
    double getInTonneSquareMetre();
    double getInPoundSquareFoot();

private:
    double _tonneSquareMetre2KilogramSquareMetre(double value);
    double _poundSquareFoot2KilogramSquareMetre(double value);
    double _kilogramSquareMetre2TonneSquareMetre(double value);
    double _kilogramSquareMetre2PoundSquareFoot(double value);

    /// internal always in kilogram/m2
    double _value;
};

}  // namespace Base
