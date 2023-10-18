#pragma once 

#include <Core/Property.h>


namespace Core
{
class LX_CORE_EXPORT PropertySolverSolverLinkList : public Core::Property
{
    TYPESYSTEM_HEADER();

public:
    PropertySolverSolverLinkList();
    virtual ~PropertySolverSolverLinkList();

    virtual void setValue(const std::list<Core::DocObject*>& list);
    virtual bool setValueFromVariant(const Core::Variant&);
    virtual void copyValue(Core::Property* p);

    virtual void addLink(Core::DocObject* o);
    virtual void removeLink(Core::DocObject* o);
    virtual bool hasLink(Core::DocObject* o) const;
    virtual void setEmpty();
    bool isEmpty() const;
    size_t getSize() const;

    const std::list<Core::DocObject*>& getValue() const;

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
    std::list<Core::DocObject*> _linkList;
};

DECLARE_PROPERTY_FACTORY(PropertySolverSolverLinkList_Factory, Core::PropertySolverSolverLinkList);
}  // namespace Core