#pragma once 

#include <Base/Writer.h>
#include <Core/PropertyLinkBaseBase.h>

namespace Core
{
template <typename T>
struct TypeNameBack
{
    static const char* Get() { return typeid(T).name(); }
};

//----------------------------------------------------------------------------
// PropertyBackLinkBase
//----------------------------------------------------------------------------

class LX_CORE_EXPORT PropertyBackLinkBase : public Core::PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();


public:
    PropertyBackLinkBase(void);

    void setValue(Core::DocObject* o);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    Core::DocObject* getValue() const;
    Core::Variant getVariant(void) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual const Core::PropertyKind getPropertyKind(void) const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    virtual bool removeLink(DocObject* o) override;
    virtual bool addLink(DocObject* o) override;
    virtual void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap) override;
    virtual std::vector<Core::DocObject*> getLinks() override;

protected:
    Core::DocObject* _link;
private:
    bool mRunningCopy = false;
};

//----------------------------------------------------------------------------
// PropertyBackLink<T>
//----------------------------------------------------------------------------

template <typename T>
class PropertyBackLink : public PropertyBackLinkBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyBackLink, Core::PropertyBackLinkBase);
    typedef PropertyBackLinkBase inherited;

public:
    void setValue(T o) { inherited::setValue(o); }
    T getValue() const { return static_cast<T>(inherited::getValue()); }
};

#ifndef SWIG
template <typename T>
Base::Type PropertyBackLink<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeNameBack<PropertyBackLink<T>>::Get());
#endif

//----------------------------------------------------------------------------
// PropertyBackLinkSetBase
//----------------------------------------------------------------------------

class LX_CORE_EXPORT PropertyBackLinkSetBase : public Core::PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();

public:
    PropertyBackLinkSetBase();
    ~PropertyBackLinkSetBase();

    void setValue(const std::unordered_set<Core::DocObject*>& linkset);
    bool setValueFromVariant(const Core::Variant& value);
    void copyValue(Core::Property* p);
    const std::unordered_set<Core::DocObject*>& getValue() const;

    bool addLink(Core::DocObject* o) override;
    void addLinks(const std::unordered_set<Core::DocObject*>& linkset);
    bool removeLink(Core::DocObject* o) override;
    void setEmpty();
    bool hasLink(Core::DocObject* o) const;
    bool isEmpty() const;
    size_t getSize() const;

    Core::Variant getVariant(void) const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
    std::shared_ptr<Core::DbgInfo> getDbgInfo() const override;
    virtual const Core::PropertyKind getPropertyKind(void) const override;
    virtual Core::Property* copy(void) const override;
    virtual void paste(const Core::Property& from) override;
    void deepCopy(Core::Property* p, Core::CoreDocument* dest_doc, DocObjectMap& copyMap) override;
    virtual std::vector<Core::DocObject*> getLinks() override;

protected:
    std::unordered_set<Core::DocObject*> _linkSet;
};

//----------------------------------------------------------------------------
// PropertyBackLinkSet<T>
//----------------------------------------------------------------------------

template <typename T>
class PropertyBackLinkSet : public PropertyBackLinkSetBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyBackLinkSet, Core::PropertyBackLinkSetBase);
    typedef PropertyBackLinkSetBase inherited;

public:
    void setValue(const std::unordered_set<T>& linkset) { inherited::setValue(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); };
    const std::unordered_set<T>& getValue() const { return *(const std::unordered_set<T>*)(&_linkSet); }

    bool addLink(T link) { return inherited::addLink(link); }
    bool removeLink(T link) { return inherited::removeLink(link); };

    void addLinks(const std::unordered_set<T>& linkset) { inherited::addLinks(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); }
};

//----------------------------------------------------------------------------
// PropertyBackLinkSet_SaveV27AsBackLink<T>
//----------------------------------------------------------------------------

template <typename T>
class PropertyBackLinkSet_SaveV27AsBackLink : public PropertyBackLinkSetBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyBackLinkSet_SaveV27AsBackLink, Core::PropertyBackLinkSetBase);
    typedef PropertyBackLinkSetBase inherited;

public:
    void setValue(const std::unordered_set<T>& linkset) { inherited::setValue(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); };
    const std::unordered_set<T>& getValue() const { return *(const std::unordered_set<T>*)(&_linkSet); }

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override
    {
        if (save_version.documentVersionMajor == 27 && save_version.documentVersionMinor == 0)
        {
            // HPK: Check for OpeningElement -> Only these should be inserted here...
            if (!_linkSet.empty())
                writer << "<Link value=\"" << (*_linkSet.begin())->getId() << "\"/>";
            else
                writer << "<Link value=\""
                       << ""
                       << "\"/>";
        }
        else
        {
            PropertyBackLinkSetBase::save(writer, save_version);
        }
    }

    bool addLink(T link) { return inherited::addLink(link); }
    bool removeLink(T link) { return inherited::removeLink(link); };

    void addLinks(const std::unordered_set<T>& linkset) { inherited::addLinks(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); }
};

#ifndef SWIG
template <typename T>
Base::Type PropertyBackLinkSet<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeNameBack<PropertyBackLinkSet<T>>::Get());
template <typename U>
Base::Type PropertyBackLinkSet_SaveV27AsBackLink<U>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeNameBack<PropertyBackLinkSet_SaveV27AsBackLink<U>>::Get());
#endif

DECLARE_PROPERTY_FACTORY(PropertyBackLinkBase_Factory, Core::PropertyBackLinkBase);
DECLARE_PROPERTY_FACTORY(PropertyBackLinkSetBase_Factory, Core::PropertyBackLinkSetBase);
DECLARE_PROPERTY_FACTORY(PropertyBackLinkSet_SaveV27AsBackLink_Factory, Core::PropertyBackLinkSetBase);

}  // namespace Core
