#pragma once

#include <Core/Property.h>


namespace Core
{
class LX_CORE_EXPORT PropertyEmbeddedFile : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertyEmbeddedFile(void);
    virtual ~PropertyEmbeddedFile(void);

    void setValue(const QByteArray& content);
    void setFilename(const Base::String& filepath);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    Base::String getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    bool hasContent();
    Base::String getFileName();
    QByteArray getContent();
    bool isSaveInLine();

protected:
    Base::String _filepath;
    QByteArray _content;
    MD5 _md5;
    bool _saveInline;
};



DECLARE_PROPERTY_FACTORY(PropertyEmbeddedFile_Factory, Core::PropertyEmbeddedFile);

}  // namespace Core
