#===============================================================================
#
# DISCLAIMER
#
# Some methods used in this script are not part of the official API and may be
# not available in the future (i.e. creating objects by type name and accessing
# properties by name).
#  
#===============================================================================

import App, Base, Core, Geom, Part

#-------------------------------------------------------
# Helper function to cast a property to the correct one.
#-------------------------------------------------------
def getPropertyValue(abstract):
    property = Core.castToPropertyAxis1(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyAxis2(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyAxis22D(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyAxis2D(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyAxis2List(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyBrepData(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyBrepDataSet(abstract)
    if property: return property.getValue()

    property =Core.castToPropertyColor(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyDirection(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyDrawStyle(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyDynamicViscosity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyEmbeddedFile(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyEnum(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyFile(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyFont(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyGTransform(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyHeatingValue(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyIndex(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyIndexList(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyInteger(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyIonConcentration(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyIsothermalMoistureCapacity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyLength(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyLengthOpt(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyLinkBase(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyLinkList(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyLogical(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyMassDensity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyMD5(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyModulusOfElasticity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyMoistureDiffusivity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyMolecularWeight(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyMultiLineText(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyNormalisedRatio(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyNumberOfDecimals(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPercent(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPHMeasure(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPlaneAngle(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPoint(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPoint2d(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPoint2dList(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPointList(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPositiveLength(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPositiveRatio(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyPressure(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyRatio(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyReal(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyRelation(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyRelationSet(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyRelaxation(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyRelaxationSet(abstract)
    if property: return property.getValue()

    property = Core.castToPropertySpecificHeatCapacity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyText(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTextList(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTexture2(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTexture2List(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTexture2Transform(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTextureCoordinateFunction(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTextureCoordinateMapping(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyThermalConductivity(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyThermalExpansionCoefficient(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyThermodynamicTemperature(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyTransform(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyUser(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyVaporPermeability(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyVector(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyVectorList(abstract)
    if property: return property.getValue()

    return None

doc = App.castToDocument(App.GetApplication().getActiveDocument())

box = doc.createObjectFromTypeName("Part::Box")     # Here we get an object
box = App.castToGeometry(box)                       # We have to cast the object to a geometry

#-------------------------------------------------------------------------------
# Setting some properties by name (properties depend on the type of the object).
#-------------------------------------------------------------------------------
box.setProperty("height", 1)
box.setProperty("width", 2)
box.setProperty("length", 3)

elem = doc.createObjectFromTypeName("App::Element") # Here we get an object
elem = App.castToElement(elem)                      # We have to cast the object to an element
elem.setGeometry(box)

doc.recompute()

#-------------------------------------
# Reading back the properties by name.
#-------------------------------------
a_length = box.getPropertyByName("length")
a_width = box.getPropertyByName("width")
a_height = box.getPropertyByName("height")
a_position = box.getPropertyByName("position")

value = getPropertyValue(a_length)
print("The length is " + str(value))

value = getPropertyValue(a_height)
print("The height is " + str(value))

value = getPropertyValue(a_width)
print("The width is " + str(value))

value = getPropertyValue(a_position)
print("The location is x:" + str(value.location().x()) + " y:" + str(value.location().y()) + " z:" + str(
    value.location().z()) + " ")
