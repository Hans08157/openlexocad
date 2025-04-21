#pragma once

#include <Base/String.h>
#include <OpenLxApp/Application.h>
#include <OpenLxApp/Element.h>
#include <OpenLxApp/Globals.h>
#include <OpenLxApp/Property.h>

#include <vector>

class BODY;

namespace OpenLxApp
{
/////////////////////////////////////////
/// General
/////////////////////////////////////////

LX_OPENLXAPP_EXPORT Version getOpenLxVersion();
LX_OPENLXAPP_EXPORT Version getLexocadVersion();
LX_OPENLXAPP_EXPORT Base::String getCurrentScriptFilePath();
LX_OPENLXAPP_EXPORT int addScriptJob(Event* aEvent, const std::string& aFunctionName);
LX_OPENLXAPP_EXPORT void setCadworkUser(bool on);
LX_OPENLXAPP_EXPORT std::string installPythonPackage(const std::string& aPackageName);

/////////////////////////////////////////
/// COMMANDS
/////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////
/// ORTHOPHOTO, PROJECTION
//////////////////////////////////////////////////////////////////////////////////

LX_OPENLXAPP_EXPORT ErrorCode projectOrthoPhoto(const std::vector<std::shared_ptr<Element>>& elems,
                                             const Base::String& imgPath,
                                             const Base::String& jpgdFilePath,
                                             const Base::String& lokFilePath);
LX_OPENLXAPP_EXPORT ErrorCode projectOrthoPhoto(const std::vector<std::shared_ptr<Element>>& elems,
                                             const Base::String& imgPath,
                                             double minX,
                                             double minY,
                                             double maxX,
                                             double maxY);
LX_OPENLXAPP_EXPORT ErrorCode projectImage(const std::vector<std::shared_ptr<Element>>& elems, const Base::String& imgPath);

// Casting for Python bindings
template <typename T>
std::shared_ptr<T> castTo(std::shared_ptr<DocObject> aObj)
{
    if (aObj)
    {
        return std::dynamic_pointer_cast<T>(aObj);
    }
    else
        return nullptr;
}

template <typename T>
std::shared_ptr<T> castTo(std::shared_ptr<Property> aProp)
{
    if (aProp)
    {
        return std::dynamic_pointer_cast<T>(aProp);
    }
    else
        return nullptr;
}



/////////////////////////////////////////
/// FILES
/////////////////////////////////////////

/*
/// Import files
LX_OPENLXAPP_EXPORT std::vector<App::Element*> importFile(std::shared_ptr<Document> aDoc, const Base::String& path, const Base::String& format,
Geom::Vec& where = Geom::Vec(0, 0, 0), Geom::Vec& normal = Geom::Vec(0, 0, 1), bool createlayer = false, bool groupelements = true, const
Base::String& realpath = "", bool asExternalFile = false, bool ignoreZeropoint = false, bool dontSnapToGrid = false); LX_OPENLXAPP_EXPORT
std::vector<App::Element*> importFile(std::shared_ptr<Document> aDoc, const Base::String& path, const Base::String& format, Geom::Vec& where =
Geom::Vec(0, 0, 0), Geom::Vec& normal = Geom::Vec(0, 0, 1), bool createlayer = false, bool groupelements = true, const Base::String& realpath =
Base::String(), bool asExternalFile = false, bool ignoreZeropoint = false, bool dontSnapToGrid = false);

/////////////////////////////////////////
/// Tasks
/////////////////////////////////////////


/////////////////////////////////////////
/// Bitmaps and Icons
/////////////////////////////////////////
*/

/////////////////////////////////////////
/// Helper
/////////////////////////////////////////
LX_OPENLXAPP_EXPORT BODY* getAcisBodyCopy(pConstShape shape);

/////////////////////////////////////////
/// Bim Helper
/////////////////////////////////////////
LX_OPENLXAPP_EXPORT int getBimColor(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimCut(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimLane(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimName(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimNumber(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimPreset(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT Base::String getBimZone(std::shared_ptr<Element> element);

LX_OPENLXAPP_EXPORT double getStoreyElevation(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT int getStoreyNumber(std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT int getBuildingNumber(std::shared_ptr<Element> element);

LX_OPENLXAPP_EXPORT void setBimLane(const Base::String& value, std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT bool setComponentByColor(int cadworkColor, std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT void setImportIFCColor(int cadworkColor, std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT bool setNewComponentByColorAndName(int cadworkColor, const Base::String& name, std::shared_ptr<Element> element);
LX_OPENLXAPP_EXPORT bool setStoreyNumber(const double& z, std::shared_ptr<Element> element);

/*
 * PropertySets Helper
 */
LX_OPENLXAPP_EXPORT bool addLxUserPropertyText(const std::string& name, Core::CoreDocument* document = nullptr);
LX_OPENLXAPP_EXPORT bool addIfcPropertyText(const std::string& name, Core::CoreDocument* document = nullptr);

LX_OPENLXAPP_EXPORT bool addLxUserPropertyList(const std::string& name, const std::vector<std::string>& entries, Core::CoreDocument* document = nullptr);
LX_OPENLXAPP_EXPORT bool addIfcPropertyList(const std::string& name, const std::vector<std::string>& entries, Core::CoreDocument* document = nullptr);

LX_OPENLXAPP_EXPORT bool addLxPropertySet(const std::string& name,
                                       const std::vector<std::string>& propertyNames,
                                       Core::CoreDocument* document = nullptr);
LX_OPENLXAPP_EXPORT bool addIfcPropertySet(const std::string& name,
                                        const std::vector<std::string>& propertyNames,
                                        Core::CoreDocument* document = nullptr);

LX_OPENLXAPP_EXPORT bool assignLxPropertySetsToComponent(std::shared_ptr<Element> elementForComponent, const std::vector<std::string>& propertySetNames);
LX_OPENLXAPP_EXPORT bool assignIfcPropertySetsToComponent(std::shared_ptr<Element> elementForComponent,
                                                       const std::vector<std::string>& propertySetNames);

LX_OPENLXAPP_EXPORT bool assignValuesToLxProperties(std::shared_ptr<Element> element,
                                                 const std::string& propertySetName,
                                                 const std::vector<std::string>& propertyNames,
                                                 const std::vector<std::string>& propertyValues);
LX_OPENLXAPP_EXPORT bool assignValuesToIfcProperties(std::shared_ptr<Element> element,
                                                  const std::string& propertySetName,
                                                  const std::vector<std::string>& propertyNames,
                                                  const std::vector<std::string>& propertyValues);

/**
 * \brief Return the value in form of a Variant of the PropertySet->Property associated with the given Element
 * \param element 
 * \param propertySetName 
 * \param propertyName 
 * \return Core::Variant
 */
LX_OPENLXAPP_EXPORT Core::Variant getValueOfPropertyDescriptor(std::shared_ptr<Element> element,
                                                               const std::string& propertySetName,
                                                               const std::string& propertyName);
}  // namespace OpenLxApp