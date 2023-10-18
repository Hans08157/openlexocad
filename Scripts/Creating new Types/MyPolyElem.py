# OpenLexocad libraries
import OpenLxApp
import Base
import Core
import Geom

lxstr = Base.StringTool.toString
cstr = Base.StringTool.toStlString

class MyPolyLineElem(OpenLxApp.Element):
	def getGlobalClassId(self):
		return Base.GlobalId("{deadc0de-06c4-4653-b4fa-1784f9f07746}")
		
	def __init__(self, aArg): 
		OpenLxApp.Element.__init__(self, aArg)
		self.registerPythonClass("MyPolyLineElem", "OpenLxApp.Element")
		# Register properties
		self.setPropertyHeader(lxstr("My Profile"), -1)
		self.setPropertyGroupName(lxstr("My Profile Parameters"), -1)
		self.width = self.registerPropertyDouble("Width", 10.0, OpenLxApp.Property.VISIBLE, OpenLxApp.Property.EDITABLE, -1)
		self.height = self.registerPropertyDouble("Height", 10.0, OpenLxApp.Property.VISIBLE, OpenLxApp.Property.EDITABLE, -1)
		self.arc = self.registerPropertyDouble("Arc", 2.0, OpenLxApp.Property.VISIBLE, OpenLxApp.Property.EDITABLE, -1)
		
	def createGeometry(self):
		res = Geom.Precision.linear_Resolution()
		if self.width.getValue() <= res:
			return None
		if self.height.getValue() <= res:
			return None
		if self.arc.getValue() <= res:
			return None

		# Build the geometry
		half = self.width.getValue() / 2.
		height = self.height.getValue()
		arc = self.arc.getValue()
		
		p1 = Geom.Pnt(-half, 0, 0)
		p2 = Geom.Pnt(-half, height, 0)
		p3 = Geom.Pnt(0, height + arc, 0)
		p4 = Geom.Pnt(half, height, 0)
		p5 = Geom.Pnt(half, 0, 0)
		
		compcurve = OpenLxApp.CompositeCurve.createIn(doc)
		compcurve.addSegment(OpenLxApp.createLineSegment(doc, p1, p2))
		compcurve.addSegment(OpenLxApp.createArc3PointsSegment(doc, p2, p3, p4))
		compcurve.addSegment(OpenLxApp.createLineSegment(doc, p4, p5))
		compcurve.addSegment(OpenLxApp.createLineSegment(doc, p5, p1))
		return compcurve
		
	def modifyGeometry(self):
		pl = self.createGeometry()
		if pl:
			self.setGeometry(pl)

	def onPropertyChanged(self, aPropertyName):
		self.getDocument().beginEditing()        
		self.modifyGeometry()        
		self.getDocument().endEditing()
		self.getDocument().recompute()
		
if __name__ == "__main__":   
	# Register this Python Script
	doc = OpenLxApp.Application.getInstance().getActiveDocument()
	doc.registerPythonScript(Base.GlobalId("{deadc0de-897d-4163-a168-a62038c92e91}"))
	polyLineElem = MyPolyLineElem(doc)
	
	# Begin editing of the Element
	doc.beginEditing()
	b = polyLineElem.createGeometry()
	polyLineElem.setGeometry(b)
	# End editing of the Element
	doc.endEditing()
	doc.recompute()   
	