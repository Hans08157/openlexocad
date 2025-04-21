#pragma once

#include <Base/AbstractXMLReader.h>
#include <Base/StringTool.h>
#include <Base/Writer.h>
#include <Core/CoreDocument.h>
#include <Core/DbgInfo.h>
#include <Core/PropertyLinkBaseBase.h>


namespace Core
{
/**
 * PropertyType2Link is a map property. As key is Base::Type as values is object link
 *
 * @since         28.0
 * @author        Tonda Buèek
 * @date          2021-06-22
 */
class LX_CORE_EXPORT PropertyType2Link : public PropertyLinkBaseBase
{
    TYPESYSTEM_HEADER();

public:
    void setValue(const std::map<Base::Type, DocObject*>& list);
    bool setValueFromVariant(const Variant& v) override;
    [[nodiscard]] Variant getVariant(void) const override { return Variant(_linkMap); }
    [[nodiscard]] const std::map<Base::Type, DocObject*>& getValue() const { return _linkMap; }
    [[nodiscard]] std::vector<DocObject*> getLinks() override;

    void copyValue(Property* p) override;
    void deepCopy(Property* p, CoreDocument* dest_doc, DocObjectMap& copyMap) override;

    bool hasKey(Base::Type type) const;
    bool hasLink(DocObject* link) const;
    bool addLink(DocObject* link) override;
    bool removeLink(DocObject* link) override;
    [[nodiscard]] DocObject* getLink(Base::Type type) const;

    [[nodiscard]] bool isEmpty() const;
    void setEmpty();
    [[nodiscard]] size_t getSize() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    inline void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property* o) const override;
    const PropertyKind getPropertyKind() const override;

    std::shared_ptr<DbgInfo> getDbgInfo() const override;
    Property* copy() const override;
    void paste(const Property& from) override;

protected:
    std::map<Base::Type, DocObject*> _linkMap;
};



/// THIS MUST BE ADDED TO - INIT_PROPERTY_TEMPLATES - TOO???!!!!!

/**
 * PropertyLinkMap is a map property. As key is template parameter as values is object link
 *
 * @since         28.0
 * @author        Tonda Buèek
 * @date          2021-06-27
 */
template <typename T>
class PropertyLinkMap : public PropertyLinkBaseBase
{
    TYPESYSTEM_PROPERTY_HEADER(PropertyLinkMap, PropertyLinkBaseBase);

public:
    void setValue(const std::map<T, DocObject*>& list);
    bool setValueFromVariant(const Variant&) override;
    [[nodiscard]] Variant getVariant(void) const override;
    [[nodiscard]] const std::map<T, DocObject*>& getValue() const { return _linkMap; }
    [[nodiscard]] std::vector<DocObject*> getLinks() override;

    void copyValue(Property* p) override;
    void deepCopy(Property* p, CoreDocument* dest_doc, DocObjectMap& copyMap) override;

    bool hasKey(T key) const;
    bool hasLink(DocObject* link, T& key) const;
    bool addLink(DocObject* link) override { return false; }
    bool addLink(T key, DocObject* link);
    bool removeLink(DocObject* link) override;
    DocObject* getLink(T key) const;

    [[nodiscard]] bool isEmpty() const;
    void setEmpty();
    [[nodiscard]] size_t getSize() const;

    void save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version) override;
    void restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version) override;

    bool isEqual(const Property* o) const override;
    const PropertyKind getPropertyKind(void) const override;

    std::shared_ptr<DbgInfo> getDbgInfo() const override;
    Property* copy(void) const override;
    void paste(const Property& from) override;

protected:
    std::map<T, DocObject*> _linkMap;
};


#ifndef SWIG

template <typename T>
struct TypeName2
{
    static const char* Get() { return typeid(T).name(); }
};

template <typename T>
Base::Type PropertyLinkMap<T>::classTypeId = Base::Type().createType(Base::Type::badType(), TypeName2<PropertyLinkMap<T>>::Get());
#endif

/////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////
/// template implementation PropertyLinkMap

template <typename T>
void PropertyLinkMap<T>::setValue(const std::map<T, DocObject*>& map)
{
    aboutToSetValue();
    for (auto pairIt : _linkMap)
    {
        if (pairIt.second)
            pairIt.second->unref();
        onRemoveLink(pairIt.second);
    }

    _linkMap = *(const std::map<T, DocObject*>*)(&map);

    for (auto pairIt : _linkMap)
    {
        onAddLink(pairIt.second);
        if (pairIt.second)
            pairIt.second->ref();
    }
    hasSetValue();
}

template <typename T>
bool PropertyLinkMap<T>::setValueFromVariant(const Variant&)
{
    cWarn("PropertyLinkMap::setValueFromVariant, Variant not implemented.");
    return false;
}

template <typename T>
Variant PropertyLinkMap<T>::getVariant() const
{
    cWarn("PropertyLinkMap::setValueFromVariant, Variant not implemented.");
    return Variant();
}

template <typename T>
DocObject* PropertyLinkMap<T>::getLink(T key) const
{
    const auto it = _linkMap.find(key);
    if (it != _linkMap.end())
        return it->second;

    return nullptr;
}

template <typename T>
void PropertyLinkMap<T>::copyValue(Property* p)
{
    assert(p->getTypeId() == getTypeId() && "Wrong property type!");
    if (p->getTypeId() == getTypeId())
    {
        PropertyLinkMap<T>* other = (PropertyLinkMap<T>*)p;
        setValue(other->getValue());
    }
}

template <typename T>
void PropertyLinkMap<T>::deepCopy(Property* p, CoreDocument* dest_doc, DocObjectMap& copyMap)
{
    assert(p->getTypeId() == getTypeId() && "Wrong property type!");
    if (p->getTypeId() == getTypeId())
    {
        PropertyLinkMap<T>* source = (PropertyLinkMap<T>*)p;

        setEmpty();
        for (auto pairIt : source->getValue())
        {
            auto it = copyMap.find(pairIt.second);
            if (it != copyMap.end())
            {
                addLink(it->second);
            }
            else
            {
                DocObject* dest_obj = dest_doc->copyObject(pairIt.second, copyMap);
                copyMap[pairIt.second] = dest_obj;
                addLink(dest_obj);
            }
        }
    }
}

template <typename T>
void PropertyLinkMap<T>::setEmpty()
{
    aboutToSetValue();
    for (auto pairIt : _linkMap)
    {
        if (pairIt.second)
            pairIt.second->unref();
        onRemoveLink(pairIt.second);
    }

    _linkMap.clear();
    hasSetValue();
}

template <typename T>
bool PropertyLinkMap<T>::hasKey(T key) const
{
    const auto it = _linkMap.find(key);
    return it != _linkMap.end();
}

template <typename T>
bool PropertyLinkMap<T>::hasLink(DocObject* link, T& key) const
{
    // Traverse the map
    for (const auto& [lKey, value] : _linkMap)
        if (value == link)
        {
            key = lKey;
            return true;
        }

    return false;
}

template <typename T>
bool PropertyLinkMap<T>::addLink(T key, DocObject* link)
{
    if (!link)
        return false;

    aboutToSetValue();
    link->ref();
    onAddLink(link);
    _linkMap.emplace(key, link);
    hasSetValue();

    return true;
}

template <typename T>
bool PropertyLinkMap<T>::removeLink(DocObject* link)
{
    if (!link)
        return false;

    // Traverse the map
    for (const auto& [key, value] : _linkMap)
    {
        if (value == link)
        {
            aboutToSetValue();
            link->unref();
            onRemoveLink(link);

            _linkMap.erase(key);
            hasSetValue();

            return true;
        }
    }

    return false;
}

template <typename T>
std::vector<DocObject*> PropertyLinkMap<T>::getLinks()
{
    std::vector<DocObject*> links;

    for (auto pairIt : _linkMap)
    {
        links.push_back(pairIt.second);
    }

    return links;
}

template <typename T>
bool PropertyLinkMap<T>::isEmpty() const
{
    return _linkMap.empty();
}

template <typename T>
size_t PropertyLinkMap<T>::getSize() const
{
    return _linkMap.size();
}

template <typename T>
void PropertyLinkMap<T>::save(Base::AbstractWriter& writer, Base::PersistenceVersion& save_version)
{
    writer << "<LinkMap size=\"" << _linkMap.size() << "\"/>";

    for (const auto& [key, value] : _linkMap)
    {
        if (value)
        {
            writer << "<Item key=\"" << key << "\" value = \"" << value->getId() << "\"/>";
        }
    }
}

template <typename T>
void PropertyLinkMap<T>::restore(Base::AbstractXMLReader& reader, Base::PersistenceVersion& version)
{
    _linkMap.clear();

    reader.readElement("LinkMap");
    const int size = reader.getAttributeAsInteger(L"size");

    for (int i = 0; i < size; i++)
    {
        reader.readElement("Item");

        Base::String value = reader.getAttribute(L"value");
        std::string id = Base::StringTool::toQString(value).toUtf8().constData();
        if (!id.empty())
        {
            DocObject* o = nullptr;
            if (DocObject* container = Base::cast2<DocObject>(getContainer()))
                o = (DocObject*)container->getDocument()->getObjectById(id);
            else if (CoreDocument* doc = Base::cast2<CoreDocument>(getContainer()))
                o = (DocObject*)doc->getObjectById(id);

            if (o)
            {
                o->ref();
                onAddLink(o);
                if (std::is_same<T, int>::value)
                    _linkMap.emplace(reader.getAttributeAsInteger(L"key"), o);
                else if (std::is_same<T, double>::value)
                    _linkMap.emplace(reader.getAttributeAsDouble(L"key"), o);
                else if (std::is_same<T, std::string>::value)
                    // this seems not correct, but changing it to string makes the thing not compilable? -mh-
                    _linkMap.emplace(reader.getAttributeAsDouble(L"key"), o);
            }
            else
            {
                if (DocObject* container = dynamic_cast<DocObject*>(getContainer()))
                    cWarn("Core::PropertyLinkMap::restore (%s) Container (%s) (%s), Object %s not exists!", getName().c_str(),
                          container->getTypeId().getName().c_str(), container->getId().c_str(), id.c_str());
                else
                    cWarn("Core::PropertyLinkMap::restore (%s), Object %s not exists!", getName().c_str(), id.c_str());
            }
        }
        else
        {
            // DG ????
            // onAddLink(0);
            //_linkList.push_back(0);
        }
    }
}

template <typename T>
const PropertyKind PropertyLinkMap<T>::getPropertyKind() const
{
    return P_MODIFY_LINK;
}

template <typename T>
bool PropertyLinkMap<T>::isEqual(const Property* o) const
{
    if (const PropertyLinkMap<T>* other = dynamic_cast<const PropertyLinkMap<T>*>(o))
        return _linkMap == other->_linkMap;

    return false;
}

template <typename T>
std::shared_ptr<DbgInfo> PropertyLinkMap<T>::getDbgInfo() const
{
    QString s = QString("size: %1").arg(_linkMap.size());

    Base::String name = Base::StringTool::toString(getName());
    Base::String type = Base::StringTool::toString(getTypeId().getName());
    Base::String value = s.toStdWString();
    auto info = DbgInfo::createDbgInfo<DbgInfo>(name, value, type, nullptr);
    for (const auto& [key, link] : _linkMap)
    {
        s = QString("key: %1, val: %2").arg(key).arg(link ? link->getId().c_str() : "nullptr");
        value = s.toStdWString();
        name = Base::StringTool::toString(link ? link->getTypeId().getName() : "");
        type = Base::StringTool::toString(link ? link->getTypeId().getName() : "");
        auto m0 = DbgInfo::createDbgInfo<DbgInfoLink>(name, value, type, info);
        m0->object = link;
    }

    return info;
}

/**
 * Returns a new copy of the property (mainly for Undo/Redo and transactions).
 * The copy has no container.
 *
 * @param[in]     void
 * @result        Property*
 *
 * @since         28.0
 * @author        Tonda Bucek
 * @date          2021-07-01
 */
template <typename T>
Property* PropertyLinkMap<T>::copy() const
{
    PropertyLinkMap<T>* p = new PropertyLinkMap<T>();
    p->setValue(_linkMap);
    return p;
}

/**
 * Paste the value from the property (mainly for Undo/Redo and transactions)
 *
 * @param[in]     const Property & from
 * @result        void
 *
 * @since         28.0
 * @author        Tonda Bucek
 * @date          2021-07-01
 */
template <typename T>
void PropertyLinkMap<T>::paste(const Property& from)
{
    const PropertyLinkMap<T>& FromList = dynamic_cast<const PropertyLinkMap<T>&>(from);
    setValue(FromList._linkMap);
}

}  // namespace Core
