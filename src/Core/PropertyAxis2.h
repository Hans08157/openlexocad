#pragma once

#include <Core/Property.h>
namespace Base { class AbstractWriter; }
namespace Base { class AbstractXMLReader; }
namespace Core { class CoreDocument; }
namespace Core { class DbgInfo; }

namespace Core
{
class LX_CORE_EXPORT PropertyAxis2 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyAxis2(void);

    void setValue(const Geom::Ax2& ax2);
    bool setValueFromVariant(const Core::Variant& value);
    virtual bool setKeyValue(const std::string& name, const Core::Variant& value);

    void setLocation(const Geom::Pnt& loc);
    void setDirection(const Geom::Dir& zDir);
    void setXDirecetion(const Geom::Dir& xDir);
    void setYDirecetion(const Geom::Dir& yDir);

    void copyValue(Core::Property* p);

    const Geom::Ax2& getValue() const;
    Core::Variant getVariant(void) const;
    virtual std::map<std::string, Core::Variant> getKeyValueMap() const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    virtual bool isEqual(const Property*) const;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;

    bool isIdentity() const;

protected:
    Geom::Ax2 _ax2;
};

class LX_CORE_EXPORT PropertyAxis22D : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyAxis22D(void);
    ~PropertyAxis22D(void);

    void setValue(const Geom::Ax22d& ax2);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Geom::Ax22d& getValue() const;
    Core::Variant getVariant(void) const;

    Geom::Ax2 getAxis2() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;

protected:
    Geom::Ax22d _ax2;
};

class LX_CORE_EXPORT PropertyAxis2List : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyAxis2List() = default;

    void setValue(const std::list<Geom::Ax2>& ax2list);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addAx2(const Geom::Ax2& ax2);
    void setEmpty();
    bool isEmpty() const;

    const std::list<Geom::Ax2>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(0); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::list<Geom::Ax2> _ax2List;
};

DECLARE_PROPERTY_FACTORY(PropertyAxis2_Factory, Core::PropertyAxis2);
DECLARE_PROPERTY_FACTORY(PropertyAxis22D_Factory, Core::PropertyAxis22D);
DECLARE_PROPERTY_FACTORY(PropertyAxis2List_Factory, Core::PropertyAxis2List);


}  // namespace Core
