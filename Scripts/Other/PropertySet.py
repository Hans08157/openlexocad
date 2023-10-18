# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base
import Core
import Geom

app = lx.Application.getInstance()
doc = app.getActiveDocument() 

# Create an Element
element = lx.Element.createIn(doc)
block = lx.Block.createIn(doc)
block.setYLength(2)
block.setZLength(2)
block.setXLength(2) 
element.setGeometry(block)
doc.recompute()

# Create a UserProperty "lx_Property1" of type Text
lx.addLxUserPropertyText("Property1")

# Create a UserProperty "lx_Property2" of type List with two entries
lx.addLxUserPropertyList("Property2", ["Entry1", "Entry2"])

# Create a PropertySet "lx_PropertySet1" and assign the above Properties to it
lx.addLxPropertySet("PropertySet1", ["Property1", "Property2"])

# Get the Component from the given Element and assign it the above PropertySet
lx.assignLxPropertySetsToComponent(element, ["PropertySet1"])

# Assign some values to the Properties of the given Element
lx.assignValuesToLxProperties(element, "PropertySet1", ["Property1", "Property2"], ["Value1", "Entry2"])