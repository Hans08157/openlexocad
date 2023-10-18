#pragma once 

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyReal : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(double d);
    virtual bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    bool maybeSetValue(double d);

    double getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    double _dValue = 0.0;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyRealOpt, Core::PropertyReal);

/////////////////////////////////////////////////
//
//  Core::PropertyRealList
//
//  A list of real numbers
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyRealList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(const std::vector<double>& value);
    virtual bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    const std::vector<double>& getValue() const { return _listOfReal; }
    Core::Variant getVariant(void) const { return Core::Variant(_listOfReal); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

    double getValueAt(size_t index) const;
    bool isEmpty() const;
    size_t getSize() const;

protected:
    std::vector<double> _listOfReal;
};

/////////////////////////////////////////////////
//
//  Core::PropertyRealList
//
//  A list of list of real numbers
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyListRealList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<std::list<double>>& list);

    void setValue(int num_i,
                  int num_j,
                  const std::vector<double>& vector);
    // This sets the _list given a vector and the number of lines/rows of the _list itself

    bool setValueFromVariant(const Core::Variant& value) override;

    void copyValue(Core::Property* p) override;

    void setEmpty();

    bool isEmpty() const;

    const std::list<std::list<double>>& getValue() const;

    const std::vector<double> getValue(int& num_i,
                                       int& num_j) const;
    // This returns a copy of the _list encoded in a vector and the number of lines/rows of the multidimensional array

    Core::Variant getVariant() const override;

    void save(Base::AbstractWriter& writer,
              Base::PersistenceVersion& save_version) override;

    virtual void save(std::ofstream& writer); // For test purposes

    void restore(Base::AbstractXMLReader& reader,
                 Base::PersistenceVersion& version) override;

    bool isEqual(const Property*) const override;

    Core::Property* copy() const override;

    void paste(const Core::Property& from) override;

protected:
    std::list<std::list<double>> _list;
};

/////////////////////////////////////////////////
//
//  Core::PropertyLength
//
//  A length property contains the value of a distance.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyLength : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyLengthMeasure
//
//  A length property contains the value of a distance.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyLengthMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyLengthOpt
//
//  An optional length property: Can contain the value of a distance.
//
/////////////////////////////////////////////////

// DONOT USE MACRO HERE SINCE WE HAVE TO CONVERT DATA FROM
// AN OLDER VERSION
// DECLARE_OPTIONAL_PROPERTY_HEADER(Core::PropertyLengthOpt,Core::PropertyLength);

class LX_CORE_EXPORT PropertyLengthOpt : public Core::PropertyLength
{
    TYPESYSTEM_HEADER();

public:
    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    bool isOptional() const { return true; }
};

/////////////////////////////////////////////////
//
//  Core::PropertyPositiveLength
//
//  A positive length property is a length property with a value greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPositiveLength : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyPositiveLengthOpt, Core::PropertyPositiveLength);

/////////////////////////////////////////////////
//
//  Core::PropertyPositiveLengthMeasure
//
//  A positive length property is a length property with a value greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPositiveLengthMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyPlaneAngle
//
//  A plane angle property contains the value of an angle in a plane.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPlaneAngle : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyPlaneAngleOpt, Core::PropertyPlaneAngle);

/////////////////////////////////////////////////
//
//  Core::PropertyPositivePlaneAngle
//
//  Positive plane angle property is a plane angle property that is greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPositivePlaneAngle : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyPositivePlaneAngleOpt, Core::PropertyPositivePlaneAngle);

/////////////////////////////////////////////////
//
//  Core::PropertyRatio
//
//  A ratio property contains the value of the relation between two physical quantities that are of the same kind.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyRatio : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::RatioMeasure
//
//  A positive ratio property is a ratio property with a value greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyRatioMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyPositiveRatioMeasure
//
//  A positive ratio property is a ratio property with a value greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPositiveRatioMeasure : public Core::PropertyRatioMeasure
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyPositiveRatio
//
//  A positive ratio property is a ratio property with a value greater than zero.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPositiveRatio : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyNormalisedRatio
//
//  A property that contains a dimensionless measure
//  to express ratio values ranging from 0.0 to 1.0.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyNormalisedRatio : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyNormalisedRatioOpt, Core::PropertyNormalisedRatio);

/////////////////////////////////////////////////
//
//  Core::PropertyDynamicViscosity
//
//  A property that contains the viscous resistance of a medium.
//  Usually measured in Pascal second (Pa s).
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyDynamicViscosity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyModulusOfElasticity
//
//  A property that contains the modulus of elasticity
//  Usually measured in N/m2.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyModulusOfElasticity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyThermalExpansionCoefficient
//
//  A property that contains the thermal expansion coefficient of a material,
//  which expresses its elongation (as a ratio) per temperature difference.
//  It is usually measured in 1/K. A positive elongation per (positive)
//  rise of temperature is expressed by a positive value.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyThermalExpansionCoefficient : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};


/////////////////////////////////////////////////
//
//  Core::PropertyPressure
//
//  A property that contains the quantity of a medium acting on a unit area.
//  Usually measured in Pascals (Pa, N/m2).
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPressure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyThermodynamicTemperature
//
//  A thermodynamic temperature property contains the value for the degree of heat of a body.
//  Usually measured in degrees Kelvin (K).
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyThermodynamicTemperature : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertySpecificHeatCapacity
//
//  Defines the specific heat of material: The heat energy absorbed per temperature unit.
//  Usually measured in J / kg Kelvin.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertySpecificHeatCapacity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyThermalConductivity
//
//  A property containing the thermal conductivity.
//  Usually measured in Watt / m Kelvin.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyThermalConductivity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyIsothermalMoistureCapacity
//
//  A property containing the isothermal moisture capacity.
//  Usually measured in m3/kg.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyIsothermalMoistureCapacity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyVaporPermeability
//
//  A property containing the vapor permeability.
//  Usually measured in kg / s m Pascal.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyVaporPermeability : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyMoistureDiffusivity
//
//  A property containing the moisture diffusivity.
//  Usually measured in m3/s.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyMoistureDiffusivity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyMolecularWeight
//
//  A property containing the molecular weight of material (typically gas).
//  Usually measured in g/mole.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyMolecularWeight : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyMassDensity
//
//  A property containing the density of a medium.
//  Usually measured in kg/m3.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyMassDensity : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyIonConcentration
//
//  A property containing the particular ion concentration in a liquid, given in mg/L.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyIonConcentration : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyPHMeasure
//
//  A property containing the molar hydrogen ion concentration in a liquid (usually defined as the measure of acidity).
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyPHMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

/////////////////////////////////////////////////
//
//  Core::PropertyHeatingValue
//
//  Defines the amount of energy released (usually in MJ/kg) when a fuel is burned.
//
/////////////////////////////////////////////////

class LX_CORE_EXPORT PropertyHeatingValue : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

class LX_CORE_EXPORT PropertyThermalTransmittance : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

class LX_CORE_EXPORT PropertyThermalTransmittanceMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};

class LX_CORE_EXPORT PropertyVolumetricFlowRateMeasure : public Core::PropertyReal
{
    TYPESYSTEM_HEADER();
};


DECLARE_PROPERTY_FACTORY(PropertyReal_Factory, Core::PropertyReal);
DECLARE_PROPERTY_FACTORY(PropertyRealOpt_Factory, Core::PropertyRealOpt);
DECLARE_PROPERTY_FACTORY(PropertyRealList_Factory, Core::PropertyRealList);
DECLARE_PROPERTY_FACTORY(PropertyListRealList_Factory, Core::PropertyListRealList);
DECLARE_PROPERTY_FACTORY(PropertyLength_Factory, Core::PropertyLength);
DECLARE_PROPERTY_FACTORY(PropertyLengthMeasure_Factory, Core::PropertyLengthMeasure);
DECLARE_PROPERTY_FACTORY(PropertyPositiveLength_Factory, Core::PropertyPositiveLength);
DECLARE_PROPERTY_FACTORY(PropertyLengthOpt_Factory, Core::PropertyLengthOpt);
DECLARE_PROPERTY_FACTORY(PropertyPlaneAngle_Factory, Core::PropertyPlaneAngle);
DECLARE_PROPERTY_FACTORY(PropertyPositivePlaneAngle_Factory, Core::PropertyPositivePlaneAngle);
DECLARE_PROPERTY_FACTORY(PropertyRatio_Factory, Core::PropertyRatio);
DECLARE_PROPERTY_FACTORY(PropertyPositiveRatio_Factory, Core::PropertyPositiveRatio);
DECLARE_PROPERTY_FACTORY(PropertyRatioMeasure_Factory, Core::PropertyRatioMeasure);
DECLARE_PROPERTY_FACTORY(PropertyPositiveRatioMeasure_Factory, Core::PropertyPositiveRatioMeasure);
DECLARE_PROPERTY_FACTORY(PropertyNormalisedRatio_Factory, Core::PropertyNormalisedRatio);
DECLARE_PROPERTY_FACTORY(PropertyDynamicViscosity_Factory, Core::PropertyDynamicViscosity);
DECLARE_PROPERTY_FACTORY(PropertyModulusOfElasticity_Factory, Core::PropertyModulusOfElasticity);
DECLARE_PROPERTY_FACTORY(PropertyThermalExpansionCoefficient_Factory, Core::PropertyThermalExpansionCoefficient);
DECLARE_PROPERTY_FACTORY(PropertyPressure_Factory, Core::PropertyPressure);
DECLARE_PROPERTY_FACTORY(PropertyThermodynamicTemperature_Factory, Core::PropertyThermodynamicTemperature);
DECLARE_PROPERTY_FACTORY(PropertySpecificHeatCapacity_Factory, Core::PropertySpecificHeatCapacity);
DECLARE_PROPERTY_FACTORY(PropertyThermalConductivity_Factory, Core::PropertyThermalConductivity);
DECLARE_PROPERTY_FACTORY(PropertyIsothermalMoistureCapacity_Factory, Core::PropertyIsothermalMoistureCapacity);
DECLARE_PROPERTY_FACTORY(PropertyVaporPermeability_Factory, Core::PropertyVaporPermeability);
DECLARE_PROPERTY_FACTORY(PropertyMoistureDiffusivity_Factory, Core::PropertyMoistureDiffusivity);
DECLARE_PROPERTY_FACTORY(PropertyMolecularWeight_Factory, Core::PropertyMolecularWeight);
DECLARE_PROPERTY_FACTORY(PropertyMassDensity_Factory, Core::PropertyMassDensity);
DECLARE_PROPERTY_FACTORY(PropertyIonConcentration_Factory, Core::PropertyIonConcentration);
DECLARE_PROPERTY_FACTORY(PropertyPHMeasure_Factory, Core::PropertyPHMeasure);
DECLARE_PROPERTY_FACTORY(PropertyHeatingValue_Factory, Core::PropertyHeatingValue);
DECLARE_PROPERTY_FACTORY(PropertyThermalTransmittance_Factory, Core::PropertyThermalTransmittance);
DECLARE_PROPERTY_FACTORY(PropertyThermalTransmittanceMeasure_Factory, Core::PropertyThermalTransmittanceMeasure);
DECLARE_PROPERTY_FACTORY(PropertyVolumetricFlowRateMeasure_Factory, Core::PropertyVolumetricFlowRateMeasure);
DECLARE_PROPERTY_FACTORY(PropertyPositiveLengthMeasure_Factory, Core::PropertyPositiveLengthMeasure);
}  // namespace Core
