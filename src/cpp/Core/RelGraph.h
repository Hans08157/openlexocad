#pragma once 

#include <Core/CoreDocument.h>
#include <boost/graph/adjacency_list.hpp>
#ifndef Q_MOC_RUN
#include <mutex>
#endif



namespace Core
{


class LX_CORE_EXPORT RelGraph
{
public:
    RelGraph( Core::CoreDocument* doc );
    ~RelGraph();
    Core::PropertyLinkBaseBase* getProperty(Core::DocObject* docObj, size_t pos);
    
    bool hasRelationShip(PropertyLinkBaseBase* p, Core::DocObject* from, Core::DocObject* to);
    
    void removeObject( Core::DocObject* obj );
    void addRelationShip(PropertyLinkBaseBase* p, Core::DocObject* from,Core::DocObject* to);
    void addRelationShips(PropertyLinkBaseBase* p, Core::DocObject* from,const std::list<Core::DocObject*>& linkList);
    void addRelationShips(PropertyLinkBaseBase* p, Core::DocObject* from,const std::unordered_set<Core::DocObject*>& linkSet);
    void removeRelationShip(PropertyLinkBaseBase* p, Core::DocObject* from,Core::DocObject* to);
    void removeRelationShips(PropertyLinkBaseBase* p, Core::DocObject* from,const std::list<Core::DocObject*>& linkList);
    void removeRelationShips(PropertyLinkBaseBase* p, Core::DocObject* from,const std::unordered_set<Core::DocObject*>& linkSet);
    
    Core::Link getOutEdges(Core::DocObject* docObj);
    Core::Link getInEdges(Core::DocObject* docObj);
    void breakLinks( Core::DocObject* from );

    
    bool check();
    
    //std::string dump();
    //void test_graph();

    std::vector<Link> mProblems;

private:
    RelGraph() = default;
    Core::CoreDocument* _cDoc = nullptr;
    class RelGraphP;
    RelGraphP* _pimpl = nullptr;
};


}  // namespace Core
