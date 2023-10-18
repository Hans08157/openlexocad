///////////////////////////////////////////////////////////////////////
//																	 //
// LEXOCAD API														 //
//																	 //
// ©2005-2016   Cadwork Informatik. All rights reserved.             //
//																	 //
// ONLY INCLUDE OTHER INTERFACES!									 //
// Lexocad provides API Classes for public use and					 //
// Implementation Classes for private use.						     //
//																	 //
// - Do ONLY include and use the LEXOCAD API in this header.		 //
// - Do not change existing interfaces.			                     //
// - Document your code!											 //
//																	 //
// - All types from Base, Core, Geom, Topo are allowed here.         //
// - In the Gui modules the use of Qt types is allowed.              //
//                                                                   //
///////////////////////////////////////////////////////////////////////

#pragma once

#include <Base/String.h>
#include <Core/Command.h>
#include <Draw/CurveStyle.h>
#include <Draw/DimensionStyle.h>
#include <Draw/ExtrusionStyle.h>
#include <Draw/PointStyle.h>
#include <Draw/SolidStyle.h>
#include <Draw/SurfaceStyle.h>
#include <Draw/TextStyle.h>
#include <OpenLxApp/Building.h>
#include <OpenLxApp/BuildingStorey.h>
#include <OpenLxApp/DocObjectFactory.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/LayerIfc.h>
#include <OpenLxApp/Site.h>
#include <OpenLxApp/Space.h>
#include <OpenLxApp/SpatialElement.h>
#include <OpenLxApp/Task.h>

#include <memory>
#include <string>
#include <vector>


namespace App
{
class Document;
}

namespace OpenLxApp
{
class Application;
class DocumentObserver;

/**
 * @brief Document holding all persistent DocObjects.
 *
 * @ingroup OPENLX_FRAMEWORK
 */

class LX_OPENLXAPP_EXPORT Document
{
public:
    friend class Application;
    friend class ApplicationP;

    /** @name Attributes*/
    //@{
    Base::String getName() const;
    void setCompany(const Base::String& company);
    void setComment(const Base::String& comment);
    void setCreatedBy(const Base::String& createdBy);
    //@}



    /** @name Editing*/
    //@{
    void beginEditing();
    void endEditing();
    bool isEditing() const;
    void addObject(std::shared_ptr<DocObject> aObject);
    void removeObject(std::shared_ptr<DocObject> aObject);
    void deleteObject(std::shared_ptr<DocObject> aObject);
    void deleteObjects(const std::vector<std::shared_ptr<DocObject>>& aObjects);
    void copyObjectsFrom(std::shared_ptr<Document> other);
    void recompute();
    //@}

    /** @name Observer*/
    //@{
    void attachDocumentObserver(std::shared_ptr<DocumentObserver> aObserver);
    void detachDocumentObserver(std::shared_ptr<DocumentObserver> aObserver);
    //@}

    bool saveAs(const Base::String& filename);
    bool saveAs(const Base::String& format, const Base::String& filename);
    bool saveAs2dl(const Base::String& filename,
                   const std::vector<std::shared_ptr<Element>>& elements,
                   const Geom::Ax2& axis,
                   bool exportFacesAsLines,
                   bool forLexo2d);
    bool saveForWeb(const Base::String& fileOrDirName, bool aSingleHtmlFile = false);
    bool createAutomaticWedgeMesh(const Base::String& xlsFileName = Base::String(), const Base::String& fileName2dl = Base::String());


    /** @name Zeropoint - Origin*/
    //@{
    Geom::XYZ getZeropointXYZ();
    void setZeropointXYZ(const Geom::XYZ& xyz);
    Geom::Pnt getZeropointLok();
    void setZeropointLok(const Geom::Pnt& pnt);
    double getZeropointAngle();
    void setZeropointAngle(double value);
    //@}

    Base::String getTmpDirectory() const;
    std::shared_ptr<Element> addVariant(const Base::String& aFileValName, const Geom::Ax2& position);
    std::shared_ptr<Element> import2dvFile(const Base::String& aFile2dvName, const Geom::Ax2& position);

    /** @name Commands */
    //@{
    bool runCommand(const std::string& cmdName);
    bool runCommand(Core::Command* cmd);
    static std::vector<std::string> getCommandNames();
    //@}

    /** @name Layer */
    //@{
    std::vector<int> getLayerNumbers() const;
    int addLayer(const Base::String& layerName, bool isVisible = true, bool isFrozen = false);
    bool getLayerName(int layerNumber, Base::String& layerName) const;
    bool setLayerName(int layerNumber, const Base::String& layerName);
    bool setLayerVisible(int layerNumber, bool isVisible);
    bool getLayerVisible(int layerNumber, bool& isVisible) const;
    bool setLayerFrozen(int layerNumber, bool isFrozen);
    bool getLayerFrozen(int layerNumber, bool& isFrozen) const;
    //@}

    /** @name Finding DocObjects */
    //@{
    std::shared_ptr<Element> getElementByGlobalId(const Base::GlobalId& aGlobalId);
    std::vector<std::shared_ptr<Element>> getElements();
    std::vector<std::shared_ptr<Element>> getElements(std::function<bool(std::shared_ptr<Element> aElement)> aFilter);
    std::shared_ptr<Root> getRootByGlobalId(const Base::GlobalId& aGlobalId);
    std::vector<std::shared_ptr<Root>> getRoots();
    std::vector<std::shared_ptr<Root>> getRoots(std::function<bool(std::shared_ptr<Root> aRoot)> aFilter);
    std::vector<std::shared_ptr<DocObject>> getObjects();
    std::vector<std::shared_ptr<DocObject>> getObjects(std::function<bool(std::shared_ptr<DocObject> aObject)> aFilter);

    std::vector<std::shared_ptr<Element>> getElementsByBimNumber(const Base::String& componentName, bool useRegularExpression = false);
    std::vector<std::shared_ptr<Element>> getElementsByBimColor(const int& cadworkColor);

    std::vector<std::shared_ptr<SpatialElement>> getSpatialElements();
    std::vector<std::shared_ptr<Site>> getSites();
    std::vector<std::shared_ptr<Building>> getBuildings();
    std::vector<std::shared_ptr<BuildingStorey>> getBuildingStoreys();
    std::vector<std::shared_ptr<Space>> getSpaces();

    std::shared_ptr<Element> getActiveElement();
    std::shared_ptr<Site> getActiveSite();
    std::shared_ptr<Building> getActiveBuilding();
    std::shared_ptr<BuildingStorey> getActiveBuildingStorey();
    //@}

    /** @name Styles */
    //@{
    Draw::PointStyle getActivePointStyle() const;
    Draw::CurveStyle getActiveCurveStyle() const;
    Draw::SurfaceStyle getActiveSurfaceStyle() const;
    Draw::TextStyle getActiveTextStyle() const;
    Draw::DimensionStyle getActiveDimensionStyle() const;
    Draw::CurveStyle getActiveAuxiliaryCurveStyle() const;
    Draw::SolidStyle getActiveSpineStyle() const;
    Draw::ExtrusionStyle getActiveExtrusionStyle() const;

    void setActivePointStyle(const Draw::PointStyle& ps);
    void setActiveCurveStyle(const Draw::CurveStyle& cs);
    void setActiveSurfaceStyle(const Draw::SurfaceStyle& ss);
    void setActiveTextStyle(const Draw::TextStyle& ts);
    void setActiveDimensionStyle(const Draw::DimensionStyle& ds);
    void setActiveAuxiliaryCurveStyle(const Draw::CurveStyle& cs);
    void setActiveSpineStyle(const Draw::SolidStyle& ss);
    void setActiveExtrusionStyle(const Draw::ExtrusionStyle& ss);
    //@}

    /** @name Tasks */
    //@{
    std::set<std::shared_ptr<Task>> getTasks(std::shared_ptr<Element> aElement);
    void setTasks(std::shared_ptr<Element> aElement, std::set<std::shared_ptr<Task>> aTasks) const;
    //@}

    std::shared_ptr<LayerIfc> getIfcLayer(const std::shared_ptr<Element>& aElement);

    /** @name WCS - WorldCoordinateSystem */
    //@{
    void set_WCS(const Geom::Ax2& axis);
    void reset_WCS();
    double getRotationZ_WCS() const;
    Geom::Pnt getLocation_WCS() const;
    Geom::Dir getGlobalX_WCS() const;
    Geom::Dir getGlobalY_WCS() const;
    Geom::Dir getGlobalZ_WCS() const;
    //@}

    /** @name Python */
    //@{
    bool registerPythonScript(const Base::GlobalId& aScriptId, const Base::String& aScriptFilePath = L"");
    //@}

    Document(const Base::String& name, const Base::String& typeName = L"");
    Document(App::Document* appDoc, const Base::String& name);

    // semi-regular
    explicit Document(const Document& other) { _appDoc = other._appDoc; }

    Document& operator=(const Document& other)
    {
        _appDoc = other._appDoc;
        return *this;
    }

    bool isEqual(std::shared_ptr<Document> other) const { return (*this == *other); }


    // regular
    friend bool operator==(const Document& x, const Document& y) { return x._appDoc == y._appDoc; }
    friend bool operator!=(const Document& x, const Document& y) { return !(x == y); }

    // totally ordered
    friend bool operator<(const Document& x, const Document& y) { return x._appDoc < y._appDoc; }
    friend bool operator>(const Document& x, const Document& y) { return y < x; }
    friend bool operator<=(const Document& x, const Document& y) { return !(x > y); }
    friend bool operator>=(const Document& x, const Document& y) { return !(x < y); }

    Document(App::Document* aDoc);
    ~Document(void);

    std::shared_ptr<DocObjectFactory> create();

    // Internal
    static std::set<std::string> commandSet;

    Document() = default;

    /// @cond INTERNAL
    // For internal use only
    static void startTimer();
    static int stopTimer();
    static int elapsedTime();
    static int elapsedTimeForTextures();
    static int elapsedTimeForLocalAxes();
    static int getRecomputeCount();

    Core::CoreDocument* __getInternalDoc__() const;
    static void __addTextureTimeInMS__(int ms);
    static void __addSetLocalAxesTimeInMS__(int ms);
    static void __addRecomputeCount__();
    static bool is_ok_for_sdk(Core::DocObject* aObj);
    /// @endcond
private:
    App::Document* _appDoc = nullptr;
    static int timeInMS;
    static int textureTimeInMS;
    static int setLocalAxesTimeInMS;
    static int recomputeCnt;
};

}  // namespace OpenLxApp
