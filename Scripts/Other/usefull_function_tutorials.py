
###########################################################################################################
#               Import Libraries
###########################################################################################################

import  Base, Core, Geom, Draw, Topo
import  OpenLxApp as lx
import  OpenLxUI  as ui
import  OpenLxCmd as cmd

import App
import time



###########################################################################################################
#               Defining namespaces
###########################################################################################################
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
uiapp = ui.UIApplication.getInstance()
uidoc = uiapp.getUIDocument(doc)
sel   = uidoc.getSelection()




###########################################################################################################
#               get the path of the file with no .lxz extension
###########################################################################################################
def getFilenamepath_noext():
        old_doc = App.castToDocument(App.GetApplication().getActiveDocument())

        filename_prop = old_doc.fileName

        path_tot = filename_prop.c_str()

        split = path_tot.split("/")
        name = split[len(split)-1]
        name = name.strip(".lxz")
        path = ""
        for i in range(0,len(split)-1):
                path += split[i]+"/"
        path += name
        
        print(path)
        return path


###########################################################################################################
#               create a cylinder
###########################################################################################################
def createCylinder(r, h, color = Base.Color(1,230,153)):
    cylinder2 = lx.RightCircularCylinder.createIn(doc)
    element = lx.Element.createIn(doc)
    cylinder2.setHeight(h)
    cylinder2.setRadius(r)
    element.setGeometry(cylinder2)
    axis2 = Geom.Ax2(origin1, zDir1, xDir1)
    element.setLocalPlacement(axis2)
    element.setDiffuseColor(color)

    return element


###########################################################################################################
#               create a plate
###########################################################################################################
def createPlate(platelength, platedepth, color = Base.Color(3,255,255)):
    plategeo = lx.Block.createIn(doc)
    plate = lx.Element.createIn(doc)

    plategeo.setXLength(platelength)
    plategeo.setYLength(platedepth)
    plategeo.setZLength(platelength)

    plate.setGeometry(plategeo)
    plate.setDiffuseColor(color)

    return plate


###########################################################################################################
#               set the Coordinates of a elem with 2 direcionvecs
###########################################################################################################
def setKoord(element,v1, v2, xkoord, ykoord, zkoord):

    element.setLocalPlacement(Geom.Ax2(origin1, Geom.Dir(v1.x(), v1.y(), v1.z()), Geom.Dir(v2.x(), v2.y(), v2.z())))
    element.translate(Geom.Vec(xkoord, ykoord, zkoord),Geom.CoordSpace_WCS)  
    
    return element

###########################################################################################################
#               Prints the directionplacements of Element
###########################################################################################################
def printplacement(element):
        place = element.getLocalPlacement()
        x = place.xDirection()
        y = place.yDirection()
        print("xDir: ", x.x(), x.y(), x.z())
        print("yDir: ", y.x(), y.y(), y.z())


###########################################################################################################
#               creates surface with height h, over Point 1 to Point 2
###########################################################################################################
def createwall(x1, y1, z1, x2, y2, z2, h):

    wall = Geom.vector_Pnt()
    wall.append(Geom.Pnt(x1,y1,z1))
    wall.append(Geom.Pnt(x1,y1,z1+h))
    wall.append(Geom.Pnt(x2,y2,z2+h))
    wall.append(Geom.Pnt(x2,y2,z2))
    wallsurface = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(wall))
    wallgeo = lx.createCurveBoundedPlaneFromFace(doc, wallsurface)

    wallelem = lx.Element.createIn(doc)
    wallelem.setGeometry(wallgeo)

    return wallelem


###########################################################################################################
#               creates a circle with middlepoint x,y,z
###########################################################################################################
def createCircle(radius, x = 0, y = 0, z = 0, color = Base.Color(0,0,0)):
    circle = lx.Circle.createIn(doc)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(circle)
    circle.setRadius(radius)
    elem.setDiffuseColor(color)

    return elem

###########################################################################################################
#               creates a face
###########################################################################################################
def createFace(p1, p2, p3):
    facepoints = Geom.vector_Pnt()
    facepoints.append(p1)
    facepoints.append(p2)
    facepoints.append(p3)
    face = Topo.FaceTool.makeFace(Topo.WireTool.makePolygon(facepoints))
    geo = lx.createCurveBoundedPlaneFromFace(doc, face)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(geo)

    return elem


###########################################################################################################
#               creates a face
###########################################################################################################
def createCartesianPoint(point):
    pnt = lx.CartesianPoint.createIn(doc)
    pnt.setPoint(point)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(pnt)
    ds = elem.getDrawStyle()
    ds.setPointSize(10)
    elem.setDrawStyle(ds)

    return elem


###########################################################################################################
#               creates a line
###########################################################################################################
def createLine(startpoint, endpoint, color = Base.Color(204,204,204)):
    pl = lx.Polyline.createIn(doc)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(pl)

    points = Geom.vector_Pnt()
    points.append(startpoint)
    points.append(endpoint)

    pl.setPoints(points)

    elem.setDiffuseColor(color)

    return elem     


#--------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

    print("start Program")
    t1 = time.clock()
    

    
            

    t2 = time.clock()
    print("end program Runtime: ", t2-t1)

