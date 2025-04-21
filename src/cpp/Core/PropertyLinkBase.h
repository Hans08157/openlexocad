#pragma once 

#include <Core/Object_Hnd.h>
#include <Core/PropertyLinkBaseBase.h>


namespace Core
{
class DbgInfo;
class DocObject;



class LX_CORE_EXPORT PropertyLinkBase : public PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();

public:
    virtual void setValue(Core::DocObject* o);
    bool setValueFromVariant(const Core::Variant& value) override;
    bool setKeyValue(const std::string& key, const Core::Variant& value) override;
    std::map<std::string, Core::Variant> getKeyValueMap() const override;

    Core::DocObject* getValue() const;
    Core::Variant getVariant(void) const override;

    /// Copies the value from 'p' into this property
    void copyValue(Core::Property* p) override;
    void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap) override;

    bool createSQL(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version, bool data) override;
    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    const Core::PropertyKind getPropertyKind(void) const override;
    bool isEqual(const Property*) const override;
    bool isLink() const override { return true; }
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    Core::Property* copy(void) const override;
    void paste(const Core::Property& from) override;

    // Tries to resolve the link from the object handle. Returns 'true' if successful, 'false' if it failed
    bool resolveLink();

    bool removeLink(DocObject*) override { return true; }
    bool addLink(DocObject*) override { return true; }

    std::vector<Core::DocObject*> getLinks() override;

protected:
    Core::Object_Hnd hObject;
};
}  // namespace Core
