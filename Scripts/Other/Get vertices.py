#===============================================================================
#
# GETTING THE VERTICES OF AN ELEMENT CURVE/MESH/SOLID...
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
import App, Base, Core, Geom, Gui

#----------------------------
# 2. Get the active document.
#----------------------------
doc = App.castToDocument(App.GetApplication().getActiveDocument())

#----------------------------------------------------------------------------
# 3. Loop on all selected elements and print the coordinates of all vertices.
#----------------------------------------------------------------------------
elements =  Gui.getSelectedElements(doc)
for element in elements:
	if element is not None:
		points = Geom.vector_Pnt()
		App.ShapeTool.getVerticesAsPoints(element.getShape(), points)
		for point in points:
			print(point.x(), " ", point.y(), " ", point.z(), "\n")
