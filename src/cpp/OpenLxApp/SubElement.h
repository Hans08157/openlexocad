#pragma once


#include <Core/DocObjectObserver.h>
#include <Core/StandardManipulatorPolicy.h>
#include <Draw/DrawStyle.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>
#include <Geom/Ax2.h>
#include <Geom/Bnd_Box.h>
#include <Geom/Trsf.h>
#include <Geom/Vec.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/Material.h>
#include <OpenLxApp/Root.h>

#include <memory>

namespace App
{
class SubElement;
}

namespace OpenLxApp
{
class Element;

/**
 * @brief A SubElement extends an Element. Together with the (parent) Element
 * it describes an entity with multiple geometries.
 * The spatial structure of SubElements is defined by their parent Elements.
 *
 * @ingroup OPENLX_FRAMEWORK
 */
class LX_OPENLXAPP_EXPORT SubElement : public Root
#ifndef SWIG
    ,
                                    public Core::DocObjectObserver,
                                    public std::enable_shared_from_this<SubElement>
#endif
{
    PROXY_HEADER(SubElement, App::SubElement, IFCCDWKELEMENT)

public:
    virtual ~SubElement(void);

    /** @name Misc */
    //@{
    std::shared_ptr<Element> getElement() const;
    std::shared_ptr<SubElement> copy() const;
    //@}

    /** @name Representation */
    //@{
    bool setGeometry(std::shared_ptr<Geometry> geo);
    std::shared_ptr<Geometry> getGeometry() const;
    Geom::Trsf getGeometryToWorldTransform() const;
    Geom::Bnd_Box getBoundingBox() const;
    //@}

    /** @name Placement */
    //@{
    Geom::Ax2 getLocalPlacement() const;
    void setLocalPlacement(const Geom::Ax2& pos);
    Geom::Trsf getTransform() const;
    Geom::Trsf getLocalToWorldTransform() const;
    void setTransform(const Geom::Trsf& t);
    void translate(const Geom::Vec& aVec, Geom::CoordSpace aCoordSpace = Geom::CoordSpace::WCS);
    void rotate(const Geom::Ax1& axis, double angle, Geom::CoordSpace aCoordSpace = Geom::CoordSpace::WCS);
    bool getLocalAxes(Geom::Ax2& localAxes);
    void setLocalAxes(const Geom::Dir& zHeight, const Geom::Dir& xLength);
    //@}

    /** @name Topology */
    //@{
    pConstShape getShape() const;
    pConstShape getLocalShape() const;
    //@}

    /** @name Rendering */
    //@{
    void setOglMaterial(const Draw::OglMaterial& mat, int faceIndex = -1);
    Draw::OglMaterial getOglMaterial() const;

    void setAmbientColor(const Base::Color& aCol);
    void setDiffuseColor(const Base::Color& aCol);
    void setSpecularColor(const Base::Color& aCol);
    void setEmissiveColor(const Base::Color& aCol);
    void setReflectiveColor(const Base::Color& aCol);
    void setShininess(int aVal);
    void setTransparency(int aVal);

    void setDrawStyle(const Draw::DrawStyle& ds);
    Draw::DrawStyle getDrawStyle() const;
    void setLineWidth(float width);
    void setTexture(const Draw::Texture2& tex, int faceIndex = -1);
    void setLengthAndCrossTexture(const Draw::Texture2& lengthTexture,
                                  const Draw::Texture2& crossTexture,
                                  const Draw::Texture2Transform& lengthTextureTrsf = Draw::Texture2Transform(),
                                  const Draw::Texture2Transform& crossTextureTrsf = Draw::Texture2Transform());
    //@}

    /** @name Attributes */
    //@{
    void setPositionNb(long value);
    long getPositionNb() const;

    bool isVisible() const;
    void setVisible(bool onoff);
    //@}

    /** @name Attributes */
    //@{
    void setAssociatedMaterial(std::shared_ptr<Material> aMaterial);
    std::shared_ptr<Material> getAssociatedMaterial() const;
    void removeAssociatedMaterial();
    //@}

    /** @name Python */
    //@{
    bool registerPythonClass(const std::string& aClassName, const std::string& aParentClassName);
    virtual Base::GlobalId getGlobalClassId() const;
    //@}

    /** @name Properties */
    //@{
    std::shared_ptr<PropertyInteger> registerPropertyInteger(const std::string& aName,
                                                             int aDefaultValue,
                                                             Property::Visible aVisible = Property::VISIBLE,
                                                             Property::Editable aEditable = Property::EDITABLE,
                                                             int aTranslationId = -1);
    std::shared_ptr<PropertyEnum> registerPropertyEnum(const std::string& aName,
                                                       int aDefaultValue,
                                                       Property::Visible aVisible = Property::VISIBLE,
                                                       Property::Editable aEditable = Property::EDITABLE,
                                                       int aTranslationId = -1);

    std::shared_ptr<PropertyDouble> registerPropertyDouble(const std::string& aName,
                                                           double aDefaultValue,
                                                           Property::Visible aVisible = Property::VISIBLE,
                                                           Property::Editable aEditable = Property::EDITABLE,
                                                           int aTranslationId = -1);

    std::shared_ptr<PropertyButton> registerPropertyButton(const std::string& aName,
                                                           Property::Visible aVisible = Property::VISIBLE,
                                                           Property::Editable aEditable = Property::EDITABLE,
                                                           int aTranslationId = -1);

    std::shared_ptr<PropertyBool> registerPropertyBool(const std::string& aName,
                                                       bool aDefaultValue,
                                                       Property::Visible aVisible = Property::VISIBLE,
                                                       Property::Editable aEditable = Property::EDITABLE,
                                                       int aTranslationId = -1);

    std::shared_ptr<PropertyString> registerPropertyString(const std::string& aName,
                                                           Base::String aDefaultValue,
                                                           Property::Visible aVisible = Property::VISIBLE,
                                                           Property::Editable aEditable = Property::EDITABLE,
                                                           int aTranslationId = -1);

    std::shared_ptr<PropertyColor> registerPropertyColor(const std::string& aName,
                                                         Base::Color aDefaultValue,
                                                         Property::Visible aVisible = Property::VISIBLE,
                                                         Property::Editable aEditable = Property::EDITABLE,
                                                         int aTranslationId = -1);

    std::shared_ptr<OpenLxApp::Property> getProperty(const std::string& aName) const;
    std::map<std::string, std::shared_ptr<Property>> getPropertyMap() const;
    std::shared_ptr<PropertyInteger> getPropertyInteger(const std::string& aName) const;
    std::shared_ptr<PropertyEnum> getPropertyEnum(const std::string& aName) const;
    std::shared_ptr<PropertyDouble> getPropertyDouble(const std::string& aName) const;
    std::shared_ptr<PropertyButton> getPropertyButton(const std::string& aName) const;
    std::shared_ptr<PropertyBool> getPropertyBool(const std::string& aName) const;
    std::shared_ptr<PropertyString> getPropertyString(const std::string& aName) const;
    std::shared_ptr<PropertyColor> getPropertyColor(const std::string& aName) const;
    bool isRegisteredProperty(const std::string& aName) const;
    void updatePythonProductVersion();

    virtual int getScriptVersion();
    virtual void convertFromOldVersion(int pythonProductVersion);
    virtual void onPropertyChanged(const std::string& aPropertyName);
    virtual void onScaling(const Geom::Vec& aVec, const Geom::Pnt& aScaleBasePnt);
    virtual void translateAfterScaled(const Geom::Vec& aVec, const Geom::Pnt& aScaleBasePnt);

    void setStandardManipulatorPolicy(const Core::StandardManipulatorPolicy& aPolicy);
    void setPropertyHeader(const Base::String& aDefaultName, int aTranslationId);
    void setPropertyGroupName(const Base::String& aDefaultName, int aTranslationId);
    Base::String getPropertyHeader() const;
    Base::String getPropertyGroupName() const;
    //@}
protected:
#ifndef SWIG
    void onChange(Core::DocObject* aCaller, const Core::DocObjectObserverMsg& aReason) override;
#endif

    SubElement() {}
};

}  // namespace OpenLxApp
