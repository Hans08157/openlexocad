#pragma once 

#include <Core/Property.h>

typedef std::pair<double, double> CA_Relaxation;

//    first  -> double relaxationValue;
//    second -> double initialStress;

namespace Core
{
class LX_CORE_EXPORT PropertyRelaxation : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const CA_Relaxation& r);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const CA_Relaxation& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    CA_Relaxation _value{0,0};
};

class LX_CORE_EXPORT PropertyRelaxationSet : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::set<CA_Relaxation>& relaxSet);
    bool setValueFromVariant(const Core::Variant& /*value*/) { return false; }
    void copyValue(Core::Property* p);

    void insert(const CA_Relaxation& r);
    const std::set<CA_Relaxation>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(0); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::set<CA_Relaxation> _relaxSet;
};

DECLARE_PROPERTY_FACTORY(PropertyRelaxation_Factory, Core::PropertyRelaxation);
DECLARE_PROPERTY_FACTORY(PropertyRelaxationSet_Factory, Core::PropertyRelaxationSet);

}  // namespace Core
