#pragma once

#include <Core/Property.h>

typedef std::shared_ptr<Geom::BrepData> pBrepData;

namespace Core
{
class LX_CORE_EXPORT PropertyBrepData : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyBrepData();

    void setValue(pBrepData data);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    pConstBrepData getValue() const;
    void setEmpty();

    Core::Variant getVariant(void) const { return Core::Variant(_data); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    pBrepData _data;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyBrepDataOpt, Core::PropertyBrepData)

class LX_CORE_EXPORT PropertyBrepDataSet : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyBrepDataSet();
    ~PropertyBrepDataSet();

    void setValue(const std::vector<pBrepData>& dataSet);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addBrepData(pBrepData data);

    const std::vector<pBrepData>& getValue() const;
    void setEmpty();

    Core::Variant getVariant(void) const { return Core::Variant(_dataSet); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<pBrepData> _dataSet;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyBrepDataSetOpt, Core::PropertyBrepDataSet)
DECLARE_PROPERTY_FACTORY(PropertyBrepData_Factory, Core::PropertyBrepData);
DECLARE_PROPERTY_FACTORY(PropertyBrepDataSet_Factory, Core::PropertyBrepDataSet);

}  // namespace Core
