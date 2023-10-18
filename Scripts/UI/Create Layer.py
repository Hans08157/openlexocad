#==================================================
#
# LAYER - Create and set it as active
#
#==================================================

import App, Base, Geom
doc = App.castToDocument(App.GetApplication().getActiveDocument())
name = Base.StringTool.toString("<LAYER NAME GOES HERE>")	# Define the layer name here.
layer = App.createLayer(doc, name)				# Create the layer.
doc.setActiveLayer(layer)					# Optionally set the new layer as the active one.
doc.recompute()