#pragma once

#include <Core/Property.h>

class QUuid;

namespace Core
{
/**
 * @brief    The PropertyGUID class saves and restores GUIDs. It also handles
 *           the management of GUIDs in the Document and makes sure that
 *           GUIDs are really unique within the Document and that
 *           the GUID corresponds to exactly one DocObject.
 *
 * @since    24.0
 * @author   HPK
 * @date
 */

class LX_CORE_EXPORT PropertyGUID : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Base::GlobalId& id);  // throws Base::GuidInUseException if GUID is already in use.
    void setValue(const QUuid& id);
    /// Set value from Base64 String
    void setValue(const Base::String& base64);
    /// Set value from const char*. Expected format is '{A921A948-076F-4EAA-8203-DF69585D9491}'
    void setValue(const char* aGuid);
    bool setValueFromVariant(const Core::Variant& value) override;

    void copyValue(Core::Property* p) override;

    /// Creates and a new GUID and sets the value. No notification or checking is done.
    Base::GlobalId createAndSetGUID();

    const Base::GlobalId& getValue() const;
    Core::Variant getVariant(void) const override;

    unsigned int getData1() const;
    unsigned short getData2() const;
    unsigned short getData3() const;
    void getData4(unsigned char value[8]) const;

    virtual bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    virtual bool isEqual(const Property*) const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

    void toUuid(QUuid& uuid) const;
    Base::String toBase64String() const;
    Base::String toString() const;

    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;

protected:
    void check_and_save_or_throw(const Base::GlobalId& id);
    Base::GlobalId _value;
};



DECLARE_PROPERTY_FACTORY(PropertyGUID_Factory, Core::PropertyGUID);

}  // namespace Core

