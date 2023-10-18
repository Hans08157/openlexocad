#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyString2DoubleMap : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::map<Base::String, double>& string2doubleMap);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const std::map<Base::String, double>& getValue() const;
    Core::Variant getVariant() const override { return Core::Variant(_map); }

    double value(const Base::String& key) const;  // Returns 0 if the key is not found.
    bool contains(const Base::String& key) const;
    void clear();
    void erase(const Base::String& key);
    void insert(const Base::String& key, double value);
    bool empty() const;
    size_t size() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property*) const override;

    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    std::map<Base::String, double> _map;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyString2DoubleMapOpt, Core::PropertyString2DoubleMap)

DECLARE_PROPERTY_FACTORY(PropertyString2DoubleMap_Factory, Core::PropertyString2DoubleMap);

}  // namespace Core
