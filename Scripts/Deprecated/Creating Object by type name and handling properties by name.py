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

#-------------------------------------------------------------------------------
# Helper function to return the value of the property
#-------------------------------------------------------------------------------
def getPropertyValue(abstract):
    property = Core.castToPropertyPositiveLength(abstract)
    if property: return property.getValue()

    property = Core.castToPropertyAxis2(abstract)
    if property: return property.getValue()

    return None

doc = App.castToDocument(App.GetApplication().getActiveDocument())

box = doc.createObjectFromTypeName("Part::Box")     # Creation of an object
box = App.castToGeometry(box)                       # We have to cast the object to a geometry

#-------------------------------------------------------------------------------
# Setting some properties by name.
#-------------------------------------------------------------------------------
box.setProperty("height", 1)
box.setProperty("width", 2)
box.setProperty("length", 3)

elem = doc.createObjectFromTypeName("App::Element") # Creation of an object
elem = App.castToElement(elem)                      # We have to cast the object to an element
elem.setGeometry(box)

doc.recompute()

#-------------------------------------------------------------------------------
# Reading back the properties by name.
#-------------------------------------------------------------------------------
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
