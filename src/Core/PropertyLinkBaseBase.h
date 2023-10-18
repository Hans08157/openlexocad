#pragma once

#include <Core/Property.h>

namespace Core
{
class LX_CORE_EXPORT PropertyLinkBaseBase : public Property
{
    TYPESYSTEM_HEADER();

public:
    virtual bool addLink(DocObject*) = 0;
    virtual bool removeLink(DocObject*) = 0;
    virtual std::vector<Core::DocObject*> getLinks() = 0;

    void onAddLink(Core::DocObject* o);
    void onRemoveLink(Core::DocObject* o);
    void onAddLinks(const std::list<Core::DocObject*>& linkList);
    void onRemoveLinks(const std::list<Core::DocObject*>& linkList);
    void onAddLinks(const std::unordered_set<Core::DocObject*>& linkSet);
    void onRemoveLinks(const std::unordered_set<Core::DocObject*>& linkSet);

    void onAddBackLink(Core::DocObject* o);
    void onRemoveBackLink(Core::DocObject* o);
    void onAddBackLinks(const std::list<Core::DocObject*>& linkList);
    void onRemoveBackLinks(const std::list<Core::DocObject*>& linkList);
    void onAddBackLinks(const std::unordered_set<Core::DocObject*>& linkSet);
    void onRemoveBackLinks(const std::unordered_set<Core::DocObject*>& linkSet);
};
}  // namespace Core
