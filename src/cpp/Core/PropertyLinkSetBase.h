#pragma once 

#include <Core/PropertyLinkBaseBase.h>


namespace Core
{
class DocObject;
class LX_CORE_EXPORT PropertyLinkSetBase : public PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(const std::unordered_set<Core::DocObject*>& set);
    bool setValueFromVariant(const Core::Variant& value) override;
    /// Sets a sub key in this property
    bool setKeyValue(const std::string& key, const Core::Variant& value) override;
    /// Returns all keys  and their values of this property
    std::map<std::string, Core::Variant> getKeyValueMap() const override;

    const std::unordered_set<Core::DocObject*>& getValue() const;
    Core::Variant getVariant() const override;

    void copyValue(Core::Property* p) override;
    void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap) override;

    virtual bool addLink(Core::DocObject* link) override;
    virtual void addLinks(const std::unordered_set<Core::DocObject*>& linkset);
    virtual bool removeLink(Core::DocObject* link) override;
    bool hasLink(const Core::DocObject* o) const;
    void setEmpty();
    bool isEmpty() const;
    size_t getSize() const;
    void rehash(long n);


    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    const Core::PropertyKind getPropertyKind(void) const override;
    bool isEqual(const Property* p) const override;
    bool isLink() const override { return true; }
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    virtual std::vector<Core::DocObject*> getLinks() override;

protected:
    std::unordered_set<Core::DocObject*> _linkSet;
};

}  // namespace Core
