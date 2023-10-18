import sys
import Base, Geom
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString
doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

# Put the name of the group(s) in a list
groupNames = ["Group 1", "Group 2"]

# Do something with the scene (e.g. create some objects or import them from a file)

sphere = lx.Sphere.createIn(doc)
sphere.setRadius(5)
element1 = lx.Element.createIn(doc)
element1.setGeometry(sphere)

# ---------------------------------------------------------------------------------

# Hide the unwanted element(s)
#element2.setVisible(False) #print "Id:" + element.getId() + " - Name:" + name

# Export the visible elements

path = sys.path[0]  #Path of the this py file
print(sys.path[0])
filename = "C:/Users/waltherp/Desktop/atest.ivz"  #Here you change it to any directory you want
filename2 = str(path)+"/atest.ivz"

doc.saveAs(lxstr("ivz"), lxstr(filename2))

print("end")