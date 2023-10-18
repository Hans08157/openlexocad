#pragma once

#include <Core/Property.h>


namespace Core
{
class LX_CORE_EXPORT PropertyTransform : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::Trsf& v);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void setIdentity();

    const Geom::Trsf& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::Trsf _trsf;
};


class LX_CORE_EXPORT PropertyGTransform : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Geom::GTrsf& v);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void setIdentity();

    const Geom::GTrsf& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);

    /// Throws Base::FileException
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Geom::GTrsf _trsf;
};

DECLARE_PROPERTY_FACTORY(PropertyTransform_Factory, Core::PropertyTransform);
DECLARE_PROPERTY_FACTORY(PropertyGTransform_Factory, PropertyGTransform);

}  // namespace Core
