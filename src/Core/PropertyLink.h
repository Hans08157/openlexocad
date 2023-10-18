#pragma once

#include <Base/AbstractXMLReader.h>
#include <Base/Log.h>
#include <Base/StringTool.h>
#include <Base/Writer.h>
#include <Core/CoreDocument.h>
#include <Core/PropertyLinkBase.h>
#include <Core/PropertyLinkListBase.h>
#include <Core/PropertyLinkSetBase.h>

namespace Core
{
template <typename T>
struct TypeName
{
    static const char* Get() { return typeid(T).name(); }
};

//----------------------------------------------------------------------------
// PropertyLink<T>
//----------------------------------------------------------------------------

template <typename T>
class PropertyLink : public PropertyLinkBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyLink, Core::PropertyLinkBase);
    typedef PropertyLinkBase inherited;

public:
    void setValue(T value) { inherited::setValue(value); }
    T getValue() const { return static_cast<T>(inherited::getValue()); }

    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& lversion) override
    {
        inherited::restore(reader, lversion);
        if (hObject.getStatus() == Object_Hnd::Valid && getValue() && !dynamic_cast<T>(inherited::getValue()))
        {
            setValue(nullptr);
            cDebug("ERROR: Trying to fill PropertyLink with object of wrong type!");
        }
    }

    bool removeLink(DocObject* /*o*/) override
    {
        setValue(nullptr);
        return true;
    }

    bool addLink(DocObject* o) override
    {
        setValue((T)o);
        return true;
    }
};

#ifndef SWIG
template <typename T>
Base::Type PropertyLink<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeName<PropertyLink<T>>::Get());
#endif


//----------------------------------------------------------------------------
// PropertyLinkSet<T>
//----------------------------------------------------------------------------

template <typename T>
class PropertyLinkSet : public PropertyLinkSetBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyLinkSet, Core::PropertyLinkSetBase);
    typedef PropertyLinkSetBase inherited;

public:
    void setValue(const std::unordered_set<T>& linkset) { inherited::setValue(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); }
    const std::unordered_set<T>& getValue() const { return *(const std::unordered_set<T>*)(&_linkSet); }

    bool addLink(T link) { return inherited::addLink(link); }
    bool removeLink(T link) { return inherited::removeLink(link); }

    void addLinks(const std::unordered_set<T>& linkset) { inherited::addLinks(*(const std::unordered_set<Core::DocObject*>*)(&linkset)); }
};

#ifndef SWIG
template <typename T>
Base::Type PropertyLinkSet<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeName<PropertyLinkSet<T>>::Get());
#endif


//----------------------------------------------------------------------------
// PropertyLinkList
//----------------------------------------------------------------------------

class LX_CORE_EXPORT PropertyLinkList : public PropertyLinkListBase
{
    TYPESYSTEM_HEADER();

public:
    PropertyLinkList() = default;
    virtual ~PropertyLinkList() = default;

    void setValue(const std::list<Core::DocObject*>& list) override;
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;

    bool addLink(Core::DocObject* o) override;
    bool removeLink(Core::DocObject* o) override;
    void setEmpty() override;

    Core::Variant getVariant() const override;

    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property* p) const override;
};


//----------------------------------------------------------------------------
// PropertyTypedLinkList
//----------------------------------------------------------------------------

template <typename T>
class PropertyTypedLinkList : public PropertyLinkListBase  //@todo mondzi: check if everything works
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyTypedLinkList, Core::PropertyLinkListBase);

public:
    void setValue(const std::list<T>& aList);
    bool setValueFromVariant(const Core::Variant& value) override;
    void copyValue(Core::Property* p) override;
    const std::list<T>& getValue() const { return *(const std::list<T>*)(&_linkList); };

    bool addLink(T link);
    bool removeLink(T link);
    bool hasLink(T link) const;

    void setEmpty();
    inline bool isEmpty() const { return _linkList.empty(); }

    size_t getSize() const { return _linkList.size(); }

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;
    bool isEqual(const Property*) const override;
};

#ifndef SWIG
template <typename T>
Base::Type PropertyTypedLinkList<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeName<PropertyTypedLinkList<T>>::Get());
#endif

// implementation

template <typename T>
bool PropertyTypedLinkList<T>::hasLink(T link) const
{
    return std::find(_linkList.begin(), _linkList.end(), link) != _linkList.end();
}

template <typename T>
bool PropertyTypedLinkList<T>::isEqual(const Property* p) const
{
    if (const PropertyTypedLinkList<T>* other = dynamic_cast<const PropertyTypedLinkList<T>*>(p))
        return _linkList == other->_linkList;

    return false;
}

template <typename T>
bool PropertyTypedLinkList<T>::addLink(T link)
{
    if (!link)
        return false;

    aboutToSetValue();
    if (link)
        link->ref();
    onAddLink(link);
    _linkList.push_back(link);
    hasSetValue();
    return true;
}

template <typename T>
bool PropertyTypedLinkList<T>::removeLink(T link)
{
    if (!link)
        return false;
    if (!hasLink(link))
        return false;

    link->unref();
    aboutToSetValue();
    onRemoveLink(link);
    _linkList.remove(link);
    hasSetValue();
    return true;
}



template <typename T>
void PropertyTypedLinkList<T>::setValue(const std::list<T>& list)
{
    aboutToSetValue();
    for (Core::DocObject* link : _linkList)
    {
        if (link)
            link->unref();
    }

    onRemoveLinks(_linkList);
    _linkList = *(const std::list<Core::DocObject*>*)(&list);
    onAddLinks(_linkList);

    for (Core::DocObject* link : _linkList)
    {
        if (link)
            link->ref();
    }
    hasSetValue();
}

template <typename T>
bool PropertyTypedLinkList<T>::setValueFromVariant(const Core::Variant& value)
{
    if (value.canConvert(Core::Variant::LinkList))
    {
        std::list<Core::DocObject*> linkList = value.toLinkList();
        for (Core::DocObject* o : linkList)
        {
            if (o && !dynamic_cast<T>(o))
            {
                cDebug("ERROR: Cannot set Core::PropertyTypedLinkList value");
                return false;
            }
        }
        setValue(*(const std::list<T>*)(&linkList));
        return true;
    }

    cDebug("ERROR: Cannot set Core::PropertyTypedLinkList value");
    return false;
}

template <typename T>
void PropertyTypedLinkList<T>::copyValue(Core::Property* p)
{
    assert(p->getTypeId() == getTypeId() && "Wrong property type!");
    if (p->getTypeId() == getTypeId())
    {
        Core::PropertyTypedLinkList<T>* other = (Core::PropertyTypedLinkList<T>*)p;
        setValue(other->getValue());
    }
}

template <typename T>
void PropertyTypedLinkList<T>::setEmpty()
{
    aboutToSetValue();
    for (Core::DocObject* link : _linkList)
    {
        if (link)
            link->unref();
    }

    onRemoveLinks(_linkList);
    _linkList.clear();
    hasSetValue();
}

template <typename T>
void PropertyTypedLinkList<T>::save(Base::AbstractWriter& writer, Base::PersistenceVersion&)
{
    std::vector<Core::DocObject*> toSave;
    for (Core::DocObject* obj : _linkList)
    {
        if (!obj)
        {
            // can nullptr be valid? -mh-
            toSave.push_back(obj);
        }
        else if (obj && (!obj->isTemporary() || obj->mustBeSaved()))
        {
            toSave.push_back(obj);
        }
    }

    writer << "<Link size=\"" << toSave.size() << "\"/>";

    for (Core::DocObject* link : toSave)
    {
        writer << "<Link value=\"" << (link ? link->getId() : std::string()) << "\"/>";
    }
}

template <typename T>
void PropertyTypedLinkList<T>::restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion&)
{
    _linkList.clear();
    reader.readElement("Link");
    int size = (reader.getAttributeAsInteger(L"size"));

    for (int i = 0; i < size; i++)
    {
        reader.readElement("Link");

        Base::String value = reader.getAttribute(L"value");
        std::string id = Base::StringTool::toQString(value).toUtf8().constData();
        if (!id.empty())
        {
            Core::CoreDocument* cd = ((Core::DocObject*)getContainer())->getDocument();
            T link = dynamic_cast<T>(cd->getObjectById(id));
            if (link)
            {
                link->ref();
                onAddLink((Core::DocObject*)link);
                _linkList.push_back(link);
            }
            else
            {
                cDebug("Error: Core::PropertyLinkList::restore ExecObject: %s not found!", id.c_str());
            }
        }
    }
}

DECLARE_PROPERTY_FACTORY(PropertyLinkBase_Factory, Core::PropertyLinkBase);
DECLARE_PROPERTY_FACTORY(PropertyLinkSetBase_Factory, Core::PropertyLinkSetBase);
DECLARE_PROPERTY_FACTORY(PropertyLinkList_Factory, Core::PropertyLinkList);

}  // namespace Core
