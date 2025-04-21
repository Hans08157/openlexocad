#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyVector : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Vec& v);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Vec& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Vec _vec{0,0,0};
};


class LX_CORE_EXPORT PropertyVectorList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<Geom::Vec>& list);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addVector(const Geom::Vec& v);
    void setEmpty();
    bool isEmpty() const;

    const std::list<Geom::Vec>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_vectorList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::list<Geom::Vec> _vectorList;
};


class LX_CORE_EXPORT PropertyListVectorList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<std::list<Geom::Vec>>& list);

    void setValue(int num_i,
                  int num_j,
                  const std::vector<Geom::Vec>& vector);
    // This sets the _list given a vector and the number of lines/rows of the _list itself

    bool setValueFromVariant(const Core::Variant& value) override;

    void copyValue(Core::Property* p) override;

    void setEmpty();

    bool isEmpty() const;

    const std::list<std::list<Geom::Vec>>& getValue() const;

    const std::vector<Geom::Vec> getValue(int& num_i,
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
    std::list<std::list<Geom::Vec>> _list;
};


DECLARE_PROPERTY_FACTORY(PropertyVector_Factory, Core::PropertyVector);
DECLARE_PROPERTY_FACTORY(PropertyVectorList_Factory, Core::PropertyVectorList);
DECLARE_PROPERTY_FACTORY(PropertyListVectorList_Factory, Core::PropertyListVectorList);

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyVectorOpt, Core::PropertyVector);
}  // namespace Core
