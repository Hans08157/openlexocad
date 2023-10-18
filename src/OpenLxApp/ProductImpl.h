#pragma once

#include <App/Application.h>
#include <App/Product.h>
#include <Base/Exception.h>
#include <Core/Core_Interface.h>
#include <Core/DocObjectObserver.h>
#include <Core/PropertyDescriptor.h>
#include <Core/PropertyScriptParam.h>
#include <Core/StandardManipulatorPolicy.h>
#include <Core/PythonScriptObject.h>
#include <Draw/DrawStyle.h>
#include <Draw/Texture2.h>
#include <Draw/Texture2Transform.h>
#include <Geom/Ax1.h>
#include <Geom/Ax2.h>
#include <Geom/Bnd_Box.h>
#include <Geom/Dir.h>
#include <Geom/Trsf.h>
#include <Geom/Vec.h>
#include <OpenLxApp/Geometry.h>
#include <OpenLxApp/Object.h>
#include <OpenLxApp/Property.h>
#include <OpenLxApp/PropertySet.h>
#include <OpenLxApp/Value.h>
#include <iostream>
#include <QFileInfo>
#include <memory>


namespace OpenLxApp
{
class Geometry;

/**
 * @brief ProductImpl implements the Product behavior of an object.
 * This is used in Product and SubElement.
 */

class ProductImpl
{
public:
    ProductImpl(App::Product* aProduct);
    ~ProductImpl(void);

    std::shared_ptr<Document> getDocument() const;

    virtual bool setGeometry(std::shared_ptr<Geometry> geo);
    std::shared_ptr<Geometry> getGeometry() const;
    Geom::Trsf getGeometryToWorldTransform() const;
    Geom::Bnd_Box getBoundingBox() const;

    Geom::Ax2 getLocalPlacement() const;
    void setLocalPlacement(const Geom::Ax2& pos);
    Geom::Trsf getTransform() const;
    Geom::Trsf getLocalToWorldTransform() const;
    void setTransform(const Geom::Trsf& t);
    void translate(const Geom::Vec& aVec, Geom::CoordSpace aCoordSpace = Geom::CoordSpace::WCS);
    void rotate(const Geom::Ax1& axis, double angle, Geom::CoordSpace aCoordSpace = Geom::CoordSpace::WCS);
    bool getLocalAxes(Geom::Ax2& localAxes);
    void setLocalAxes(const Geom::Dir& zHeight, const Geom::Dir& xLength);

    pConstShape getShape() const;
    pConstShape getLocalShape() const;

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

    void setPositionNb(long value);
    long getPositionNb() const;

    bool isVisible() const;
    void setVisible(bool onoff);

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
                                                           const Base::String& aDefaultValue,
                                                           Property::Visible aVisible = Property::VISIBLE,
                                                           Property::Editable aEditable = Property::EDITABLE,
                                                           int aTranslationId = -1);

    std::shared_ptr<PropertyColor> registerPropertyColor(const std::string& aName,
                                                         const Base::Color& aDefaultValue,
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

    int getPythonProductVersion() const;
    void setPythonProductVersion(int pythonProductVersion) const;

    void translateAfterScaled(const Geom::Vec& aVec, const Geom::Pnt& aScaleBasePnt);
    void setStandardManipulatorPolicy(const Core::StandardManipulatorPolicy& aPolicy);
    void setPropertyHeader(const Base::String& aDefaultName, int aTranslationId);
    void setPropertyGroupName(const Base::String& aDefaultName, int aTranslationId);
    Base::String getPropertyHeader() const;
    Base::String getPropertyGroupName() const;

    // User defined properties
    std::shared_ptr<PropertyUser> getPropertyUser(const std::string& aName) const;
    std::vector<std::shared_ptr<PropertyUser>> getPropertyUser() const;
    std::vector<Base::String> getPropertySetNames() const;
    std::shared_ptr<PropertySet> getPropertySetByName(const Base::String& aName) const;

    /**
     * Implementation of registerPythonClass
     *
     * @param[in]     T aCaller: The calling instance
     * @param[in]     const std::string & aClassName : The name of the Python class.
     * @param[in]     const std::string & aParentClassName : The full name of the parent class (or super class)
     *                                                       e.g. OpenLxApp.Element
     * @result        bool : Returns true if successfully registered.
     *
     * @since         26.0
     * @author        HPK
     * @date          2019-04-14
     */
    template <typename T>
    bool registerPythonClass(std::shared_ptr<T> aObject, const std::string& aClassName, const std::string& aParentClassName)
    {
        if (aClassName == "" || aParentClassName == "")
            return false;

        auto pco = mProduct->getPythonClassObject();
        if (pco)
        {
            std::cout << "Already registered!" << std::endl;

            int pythonProductVersion = getPythonProductVersion();
            if (pythonProductVersion < aObject->getScriptVersion())
            {
                aObject->convertFromOldVersion(pythonProductVersion);
            }

            return true;  // Class is already registered.
        }
        else
        {
            auto fileName = Core::getCurrentScriptFilePath();

            // Get Script
            Base::GlobalId scriptId = Core::getCurrentScriptId();
            if (scriptId.isNull())
            {
                Base::Message().showMessageBoxError(App::GetApplication().getQApplicationName(),
                                                    QString("Cannot register Python Script. \nGlobalId = %1\nDid you forget to "
                                                            "add\n\ndoc.registerPythonScript(Base.GlobalId(\"{<aGloballyUniqueId>}\") \n\nto your "
                                                            "Lexocad Python Script?\nSee https://www.guidgenerator.com to generate a GlobalId.")
                                                        .arg(QString::fromStdWString(scriptId.toString().c_str())));
                return false;
            }

            Core::PythonScriptObject* pythonScriptObject = Core::PythonScriptObject::getRegisteredScript(scriptId);
            if (!pythonScriptObject)
            {
                Base::Message().showMessageBoxError(
                    App::GetApplication().getQApplicationName(),
                    QString("Cannot get the registered Script.\nGlobalId = %1").arg(QString::fromStdWString(scriptId.toString().c_str())));
                return false;
            }

            // Check if class is already registered...
            auto classId = aObject->getGlobalClassId();
            if (classId.isNull())
            {
                Base::Message().showMessageBoxError(App::GetApplication().getQApplicationName(),
                                                    QString("Cannot register Python class. \nGlobalId = %1\nDid you forget to add\n\ndef "
                                                            "getGlobalClassId(self):\n      return Base.GlobalId(\"{<aGloballyUniqueId>}\") \n\nto "
                                                            "your Lexocad Python class?\nSee https://www.guidgenerator.com to generate a GlobalId.")
                                                        .arg(QString::fromStdWString(classId.toString().c_str())));
                return false;
            }

            // Check if the file base name contains whitespaces.
            // This is not allowed because it will later cause
            // problems when trying to import the module.
            // eg: 'import My module name' will cause an error.
            QFileInfo fi(QString::fromStdWString(fileName.c_str()));
            QString baseName = fi.completeBaseName();
            if (baseName.contains(' '))
            {
                Base::Message().showMessageBoxError(QString::fromStdWString(Core::CoreApplication::instance()->getApplicationName().c_str()),
                                                    QString("Cannot import '%1'.\nWhitespaces in names are not allowed.").arg(baseName));
                return false;
            }

            Base::String thisClassName = Base::StringTool::toString(aClassName);
            Base::String superClassName = Base::StringTool::toString(aParentClassName);

            if (auto regClass = Core::PythonClassObject::getRegisteredClass(classId))
            {
                if (regClass->className.getValue() != thisClassName)
                {
                    Base::Message().showMessageBoxError(
                        App::GetApplication().getQApplicationName(),
                        QString("Cannot register Python class. \nThe GlobalId is already registered with a different class (%1)")
                            .arg(QString::fromStdWString(regClass->className.getValue().c_str())));
                    return false;
                }
                mProduct->setPythonClassObject(regClass);

                // Save the version of the script that first created *this* Product
                const int pythonProductVersion = aObject->getScriptVersion();
                setPythonProductVersion(pythonProductVersion);

                return true;  // Class is already registered.
            }
            else
            {
                std::cout << "First register" << std::endl;
                Core::CoreDocument* doc = mProduct->getDocument();
                auto pythonClassObject = doc->createObject<Core::PythonClassObject>();
                mProduct->setPythonClassObject(pythonClassObject);
                pythonClassObject->className.setValue(thisClassName);
                pythonClassObject->classId.setValue(classId);
                pythonClassObject->superClassName.setValue(superClassName);
                Core::PythonClassObject::registerClass(pythonClassObject);

                pythonClassObject->pythonScriptObject.setValue(pythonScriptObject);
                pythonClassObject->standardManipulatorPolicy.setValue(
                    Core::StandardManipulatorPolicy::SHOWBBOX |
                    Core::StandardManipulatorPolicy::TRANSLATEXENABLED | Core::StandardManipulatorPolicy::TRANSLATEYENABLED |
                    Core::StandardManipulatorPolicy::TRANSLATEZENABLEDL | Core::StandardManipulatorPolicy::TRANSLATEZENABLEDW |
                    Core::StandardManipulatorPolicy::TRANSLATEZENABLEDH | Core::StandardManipulatorPolicy::HIGHLIGHT);

                // Save the version of the script that first created *this* Product
                const int pythonProductVersion = aObject->getScriptVersion();
                setPythonProductVersion(pythonProductVersion);

                return true;  // Class is registered successfully.
            }
        }
    }

    template <typename T>
    void onChange(std::shared_ptr<T> aObject, Core::DocObject* aCaller, const Core::DocObjectObserverMsg& aReason)
    {
        if (getDocument()->isEditing())
            return;

        switch (aReason.msgId)
        {
            case Core::DocObjectObserverMsg::MessageId::PropertyChanged:
                aObject->onPropertyChanged(Base::StringTool::toStlString(aReason.value1.toString()));
                break;
            case Core::DocObjectObserverMsg::MessageId::Scaling:
            {
                const auto& vec = aReason.value1.toVector();
                const auto& pnt = aReason.value2.toPoint();

                if (vec.magnitude() > Geom::Precision::linear_Resolution())
                {
                    aObject->onScaling(vec, pnt);
                }
                break;
            }
            default:
                break;
        }
    }

private:
    App::Product* mProduct = nullptr;
};

}  // namespace OpenLxApp
