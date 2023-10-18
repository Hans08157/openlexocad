#==================================================
#
# LAYER - Assign specific layer to an object
#
#==================================================
import App, Base, Geom, Part
doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Create additional layers
App.createLayer(doc, Base.StringTool.toString("Layer 2"))
App.createLayer(doc, Base.StringTool.toString("Layer 3"))

# Create an element: it will be assigned to the active layer (whatever it is).
box = Part.createBox(doc)
elem = App.createElement(doc)
elem.setGeometry(box)
box.length.setValue(5)
box.width.setValue(5)
box.height.setValue(5)
doc.recompute()

# Get the required layer
layer2 = App.getLayerByName(doc, Base.StringTool.toString("Layer 2"))
# If the layer number is know -> layer2 = App.getLayerByLayerNumber(doc, 2)

# Assign the element to the layer
App.setLayer(elem, layer2)