#pragma once

#include <QDateTime>
#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyDateTime : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const QDateTime& t);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const QDateTime& getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;


protected:
    QDateTime _datetime;
};

class LX_CORE_EXPORT PropertyDateTimeList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyDateTimeList();
    virtual ~PropertyDateTimeList();

    void setValue(const std::list<QDateTime>& dtlist);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    void addDateTime(const QDateTime& t);
    void setEmpty();
    bool isEmpty() const;

    const std::list<QDateTime>& getValue() const;

    Core::Variant getVariant(void) const { return Core::Variant(_dateTimeList); }

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::list<QDateTime> _dateTimeList;
};

DECLARE_PROPERTY_FACTORY(PropertyDateTime_Factory, Core::PropertyDateTime);
DECLARE_PROPERTY_FACTORY(PropertyDateTimeList_Factory, Core::PropertyDateTimeList);


}  // namespace Core
