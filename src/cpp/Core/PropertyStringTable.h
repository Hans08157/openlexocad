#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyStringTable : public Core::Property
{
    TYPESYSTEM_HEADER();

    typedef std::vector<std::vector<Base::String>> stringTable;

public:

    void setValue(const stringTable& table);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    const stringTable& getValue() const { return _table; }
    Core::Variant getVariant() const override { return Core::Variant(_table); }

    void addRow(const std::vector<Base::String>& row);
    void setRow(int row, const std::vector<Base::String>& rowData);
    void insertRow(int row, const std::vector<Base::String>& rowData);
    void setData(int row, int column, const Base::String& data);
    void addData(int row, const Base::String& data);

    std::vector<Base::String> getRow(int row);
    Base::String getData(int row, int column);

    void clear();
    void removeRow(int row);
    void removeCsvRows(int paramMode);

    bool empty() const { return _table.empty(); }
    size_t rows() const { return _table.size(); }

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property* o) const override;

    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    stringTable _table;
};


DECLARE_PROPERTY_FACTORY(PropertyStringTable_Factory, Core::PropertyStringTable);

}  // namespace Core
