#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyString2IntegerSetMap : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::map<Base::String, std::set<int>>& string2integerSetMap);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const std::map<Base::String, std::set<int>>& getValue() const;
    Core::Variant getVariant() const override { return Core::Variant(_map); }

    std::set<int> value(const Base::String& key) const;  // Returns {} if the key is not found.
    bool contains(const Base::String& key) const;
    bool contains(const Base::String& key, int value) const;
    void clear();
    void erase(const Base::String& key);
    void erase(const Base::String& key, int value);
    void insert(const Base::String& key, std::set<int>& value);
    void insert(const Base::String& key, int value);
    bool empty() const;
    bool empty(const Base::String& key) const;
    size_t size() const;
    size_t size(const Base::String& key) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property*) const override;

    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    std::map<Base::String, std::set<int>> _map;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyString2IntegerSetMapOpt, Core::PropertyString2IntegerSetMap)

DECLARE_PROPERTY_FACTORY(PropertyString2IntegerSetMap_Factory, Core::PropertyString2IntegerSetMap);

}  // namespace Core
