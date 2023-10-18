import unittest
import io

# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI	 as ui
import Base, Core, Geom, Topo, Draw

class SelectionTest(unittest.TestCase):
	def setUp(self):
		self.app   = lx.Application.getInstance()
		self.doc   = self.app.getActiveDocument()	
		self.uiapp = ui.UIApplication.getInstance()
		self.uidoc = self.uiapp.getUIDocument(doc)
		self.sel   = self.uidoc.getSelection()

	def tearDown(self):
		pass
		
	def test_getDocument(self):		
		self.assertTrue(1 == 1)
		


if __name__ == '__main__':	
	unittest.main()