import  Base, Core, Geom, Draw, Topo
import  OpenLxApp as lx
import  OpenLxUI  as ui
import  OpenLxCmd as cmd
##########################################################################
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
##########################################################################
doc   = lx.Application.getInstance().getActiveDocument()

# Create a test Element
e = lx.Element.createIn(doc)
block = lx.Block.createIn(doc)
e.setGeometry(block)
doc.recompute()


ex = lx.IFC_Exporter.createIn(doc)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_ifc.ifc"))
print("IFC_Exporter returned: ", res)

ex = lx.IV_Exporter.createIn(doc)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_iv.iv"))
print("IV_Exporter returned: ", res)

ex = lx.OBJ_Exporter.createIn(doc)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_obj.obj"))
print("OBJ_Exporter returned: ", res)

ex = lx.SAT_Exporter.createIn(doc)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_sat.sat"))
print("SAT_Exporter returned: ", res)

ex = lx.WebGL_Exporter.createIn(doc)
ex.setSingleHtmlFile(True)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_webgl.html"))
print("WebGL_Exporter returned: ", res)

ex = lx.C3DZ_Exporter.createIn(doc)
res = ex.exportFile(lxstr("C:\\Users\\Hans\\Desktop\\test_3dz.3dz"))
print("C3DZ_Exporter returned: ", res)



