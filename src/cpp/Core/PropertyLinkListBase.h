#pragma once

#include <Core/PropertyLinkBaseBase.h>


namespace Core
{
class DocObject;
class LX_CORE_EXPORT PropertyLinkListBase : public PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(const std::list<Core::DocObject*>& /*list*/) {}
    const std::list<Core::DocObject*>& getValue() const;

    virtual bool hasLink(Core::DocObject* o) const;
    virtual void setEmpty() {}
    virtual bool isEmpty() const;
    virtual size_t getSize() const;

    // override from PropertyLinkBaseBase

    bool addLink(Core::DocObject* o) override;
    bool removeLink(Core::DocObject* o) override;
    std::vector<Core::DocObject*> getLinks() override;

    // override from Property

    Core::Variant getVariant() const override { return Core::Variant(_linkList); }
    bool setValueFromVariant(const Core::Variant&) override { return false; }
    Core::Property* copy() const override;
    void paste(const Core::Property& from) override;
    void copyValue(Core::Property* /*p*/) override {}
    void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap) override;
    const Core::PropertyKind getPropertyKind() const override;
    bool isEqual(const Property*) const override;
    bool isLink() const override { return true; }
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;

    // override from Persistence

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

protected:
    std::list<Core::DocObject*> _linkList;
};

}  // namespace Core
