#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyTexture2 : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::Texture2& mat);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::Texture2 getValue() const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    int _textureId = -1;
};

class LX_CORE_EXPORT PropertyTexture2Transform : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::Texture2Transform& ttf, bool calculateTextureScaleFactor = false);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::Texture2Transform& getValue() const;
    Core::Variant getVariant(void) const;

    void setCalculateTextureScaleFactor(bool onoff);
    bool isCalculateTextureScaleFactor() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Draw::Texture2Transform _texture2Transform;
    bool _calculateTextureScaleFactor = false;
};

class LX_CORE_EXPORT PropertyTextureCoordinateMapping : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::TextureCoordinateMapping& tcm);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::TextureCoordinateMapping& getValue() const;
    Core::Variant getVariant(void) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Draw::TextureCoordinateMapping _textureCoordinateMapping;
};

class LX_CORE_EXPORT PropertyTextureCoordinateFunction : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const Draw::TextureCoordinateFunction& tcf);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);

    const Draw::TextureCoordinateFunction& getValue() const;
    Core::Variant getVariant(void) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    Draw::TextureCoordinateFunction _textureCoordinateFunction;
};

class LX_CORE_EXPORT PropertyTexture2List : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::map<int, Draw::Texture2>& texList);
    bool setValueFromVariant(const Core::Variant&) { return false; }
    void copyValue(Core::Property* p);

    int addTexture(const Draw::Texture2& tex);
    bool hasTexture(const Draw::Texture2& tex);
    void setEmpty();

    const Draw::Texture2& getTextureById(int id);

    const std::map<int, Draw::Texture2>& getValue(void) const;
    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);

    virtual void saveDocFile(Base::AbstractWriter& writer, const Base::String& filename, const Base::String& tmpdir);
    virtual void restoreDocFile(Base::Reader& reader, const Base::String& tmpdir);
    virtual bool isEqual(const Property*) const;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

private:
    std::map<int, Draw::Texture2> _textureMap;
    Draw::Texture2 _defaultTexture;
    int _nextAvailableId = 1;
};


DECLARE_PROPERTY_FACTORY(PropertyTexture2_Factory, Core::PropertyTexture2);
DECLARE_PROPERTY_FACTORY(PropertyTexture2Transform_Factory, Core::PropertyTexture2Transform);
DECLARE_PROPERTY_FACTORY(PropertyTextureCoordinateMapping_Factory, Core::PropertyTextureCoordinateMapping);
DECLARE_PROPERTY_FACTORY(PropertyTextureCoordinateFunction_Factory, Core::PropertyTextureCoordinateFunction);
DECLARE_PROPERTY_FACTORY(PropertyTexture2List_Factory, Core::PropertyTexture2List);


}  // namespace Core
