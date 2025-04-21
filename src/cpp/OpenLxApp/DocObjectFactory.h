#pragma once
#include <LxIfc4/IFC4_impl/LxIfc4EntityEnums.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/Group.h>
#include <OpenLxApp/LayerIfc.h>
#include <OpenLxApp/MaterialSelect.h>
#include <OpenLxApp/ObjectDefinition.h>
#include <OpenLxApp/Process.h>
#include <OpenLxApp/ProfileDef.h>
#include <OpenLxApp/SubElement.h>
#include <OpenLxApp/Task.h>


namespace App
{
class Document;
class Geometry;
class Element;
class ObjectDefinition;
class MaterialSelect;
}  // namespace App

namespace boost
{
    template <class T, class H, class P, class A> class unordered_set;
}

namespace Part
{
class ProfileDef;
}

namespace OpenLxApp
{
class Document;

/**
 * @brief DocObjectFactory to create DocObjects
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT DocObjectFactory
{
public:
    friend class Document;

    DocObjectFactory(std::shared_ptr<Document> aDoc);
    DocObjectFactory(App::Document* aDoc);
    ~DocObjectFactory();

    static std::vector<std::shared_ptr<Product>> aProducts(const std::vector<App::Product*> aProduct);
    static std::shared_ptr<Product> aProduct(App::Product* aProduct);

    static std::vector<std::shared_ptr<Element>> aElements(const std::vector<App::Element*> aElem);
    static std::vector<std::shared_ptr<Element>> aElements(std::unordered_set<App::Element*> aElems);
    static std::shared_ptr<Element> aElement(App::Element* aElem);

    std::shared_ptr<Element> aTmpElement();
    static std::shared_ptr<Geometry> aGeometry(App::Geometry* aGeom);
    static std::shared_ptr<ProfileDef> aProfile(Part::ProfileDef* aProfileDef);
    static std::shared_ptr<DocObject> aDocObject(Core::DocObject* aObj);
    static std::shared_ptr<LayerIfc> aLayerIfc(App::LayerIFC* aLayerIfc);
    static std::shared_ptr<ObjectDefinition> aObjectDefinition(App::ObjectDefinition* aObj);
    static std::shared_ptr<Object> aObject(App::Object* aObj);
    static std::shared_ptr<Process> aProcess(App::Process* aProcess);
    static std::shared_ptr<Root> aRoot(App::Root* aObj);
    static std::shared_ptr<Task> aTask(App::Task* aTask);
    static std::shared_ptr<MaterialSelect> aMaterialSelect(App::MaterialSelect* aMatSel);

    template <typename OpenLxClass>
    std::shared_ptr<OpenLxClass> aObject()
    {
        return OpenLxClass::createIn(_doc);
    }

    template <typename OpenLxClass>
    static std::shared_ptr<OpenLxClass> aObject(std::shared_ptr<Document> aDoc)
    {
        return OpenLxClass::createIn(aDoc);
    }

    static LxIfc4::LxIfc4EntityEnum getEntityTypeFromTypeName(const std::string& aType);


private:
    DocObjectFactory() {}
    static std::shared_ptr<Product> _createProduct(LxIfc4::LxIfc4EntityEnum aType, App::Product* aProduct, std::shared_ptr<Document> aDoc);

    std::shared_ptr<Document> _doc;
    Core::CoreDocument* _coredoc = nullptr;
};



}  // namespace OpenLxApp