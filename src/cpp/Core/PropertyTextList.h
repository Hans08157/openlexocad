#pragma once 

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyTextList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::list<Base::String>& textList);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    void addText(const Base::String& text);
    void removeText(const Base::String& text);

    bool contains(const Base::String& text) const;

    void setEmpty();
    bool isEmpty() const;
    size_t getSize() const;

    const std::list<Base::String>& getValue() const;
    /// Returns empty string if index is out of bounds.
    const Base::String getValueAt(size_t index) const;
    /// Returns all entries as one string, joined by given separator.
    const Base::String join(const Base::String& separator) const;

    Core::Variant getVariant() const override { return Core::Variant(_textList); }

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;

    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;

protected:
    std::list<Base::String> _textList;
};

DECLARE_OPTIONAL_PROPERTY_HEADER(PropertyTextListOpt, Core::PropertyTextList)

DECLARE_PROPERTY_FACTORY(PropertyTextList_Factory, Core::PropertyTextList);

}  // namespace Core
