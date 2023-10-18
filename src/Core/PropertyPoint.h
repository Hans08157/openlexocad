#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyPoint : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Pnt& p);
    virtual bool setValueFromVariant(const Core::Variant& value);
    /// 'x' sets x coordinate, 'y' sets y coordinate, 'z' sets z coordinate
    virtual bool setKeyValue(const std::string& name, const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    const Geom::Pnt& getValue() const;
    virtual Core::Variant getVariant(void) const;
    /// Returns all keys  and their values of this property
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Pnt _pnt{0,0,0};
};

class LX_CORE_EXPORT PropertyPointList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<Geom::Pnt>& list);
    virtual bool setValueFromVariant(const Core::Variant& value);
    virtual void copyValue(Core::Property* p);

    void addPoint(const Geom::Pnt& v);
    void setEmpty();
    bool isEmpty() const;

    const std::vector<Geom::Pnt>& getValue() const;
    const size_t getSize() const;

    virtual Core::Variant getVariant(void) const { return Core::Variant(_pointList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

    static void save_static(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, const std::vector<Geom::Pnt>& pointList);
    static void restore_static(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version, std::vector<Geom::Pnt>& pointList);

protected:
    std::vector<Geom::Pnt> _pointList;
};

class LX_CORE_EXPORT PropertyListPointList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<std::list<Geom::Pnt>>& list);

    void setValue(int num_i,
                  int num_j,
                  const std::vector<Geom::Pnt>& vector);
    // This sets the _list given a vector and the number of lines/rows of the _list itself

    bool setValueFromVariant(const Core::Variant& value) override;

    void copyValue(Core::Property* p) override;

    void setEmpty();

    bool isEmpty() const;

    const std::list<std::list<Geom::Pnt>>& getValue() const;

    const std::vector<Geom::Pnt> getValue(int& num_i,
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
    std::list<std::list<Geom::Pnt>> _list;
};

class LX_CORE_EXPORT PropertyPoint2d : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Pnt2d& p);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Pnt2d& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Pnt2d _pnt{0,0};
};

class LX_CORE_EXPORT PropertyPoint2dList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::vector<Geom::Pnt2d>& list);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addPoint(const Geom::Pnt2d& v);
    void setEmpty();
    bool isEmpty() const;

    const std::vector<Geom::Pnt2d>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_pointList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<Geom::Pnt2d> _pointList;
};

DECLARE_PROPERTY_FACTORY(PropertyPoint_Factory, Core::PropertyPoint);
DECLARE_PROPERTY_FACTORY(PropertyPointList_Factory, Core::PropertyPointList);
DECLARE_PROPERTY_FACTORY(PropertyListPointList_Factory, Core::PropertyListPointList);
DECLARE_PROPERTY_FACTORY(PropertyPoint2d_Factory, Core::PropertyPoint2d);
DECLARE_PROPERTY_FACTORY(PropertyPoint2dList_Factory, Core::PropertyPoint2dList);


}  // namespace Core