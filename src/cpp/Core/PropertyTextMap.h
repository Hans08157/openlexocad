#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyTextMap : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::map<Base::String, Base::String>& textMap);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const std::map<Base::String, Base::String>& getValue() const;
    Core::Variant getVariant() const override { return Core::Variant(_textMap); }

    Base::String value(const Base::String& key) const;  // Returns empty string if the key is not found.
    bool contains(const Base::String& key) const;
    void clear();
    void erase(const Base::String& key);
    void insert(const Base::String& key, const Base::String& value);
    bool empty() const;
    size_t size() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property*) const override;

    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    std::map<Base::String, Base::String> _textMap;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyTextMapOpt, Core::PropertyTextMap)

DECLARE_PROPERTY_FACTORY(PropertyTextMap_Factory, Core::PropertyTextMap);

}  // namespace Core
