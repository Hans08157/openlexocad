#pragma once 

#include <Core/Property.h>


namespace Core
{
class LX_CORE_EXPORT PropertySolverElementLinkVector : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertySolverElementLinkVector();
    virtual ~PropertySolverElementLinkVector();

    virtual void setValue(const std::vector<Core::DocObject*>& list);
    virtual bool setValueFromVariant(const Core::Variant&);
    virtual void copyValue(Core::Property* p);

    virtual void addLink(Core::DocObject* o);
    virtual void removeLink(Core::DocObject* o);
    virtual bool hasLink(Core::DocObject* o) const;
    virtual void setEmpty();
    bool isEmpty() const;
    size_t getSize() const;

    const std::vector<Core::DocObject*>& getValue() const;

    Core::Variant getVariant(void) const;

    virtual void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version);
    inline virtual void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version);
    virtual const Core::PropertyKind getPropertyKind(void) const;
    virtual bool isEqual(const Property*) const;
    virtual bool isLink() const { return true; }
    virtual std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;

protected:
    std::vector<Core::DocObject*> _linkList;
};

DECLARE_PROPERTY_FACTORY(PropertySolverElementLinkList_Factory, Core::PropertySolverElementLinkVector);

}  // namespace Core