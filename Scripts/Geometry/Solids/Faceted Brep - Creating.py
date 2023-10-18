#===============================================================================
#
# CREATING A FACETED BREP
#
#===============================================================================

#-----------------------------
# 1. Import OpenLexocad libraries.
#-----------------------------
import OpenLxApp as lx
import OpenLxUI  as ui
import Geom

def vertices(w, h, b):

    w = float(w)
    h = float(h)
    b = float(b)

    #--------------------------------------
    # Creating a vector of points.
    #--------------------------------------
    list = Geom.vector_Pnt()

    list.append(Geom.Pnt(0, 0, 0)) # Lower vertices
    list.append(Geom.Pnt(w, 0, 0)) #
    list.append(Geom.Pnt(w, b, 0)) #
    list.append(Geom.Pnt(0, b, 0)) #

    list.append(Geom.Pnt(0, 0, h)) # Upper vertices
    list.append(Geom.Pnt(w, 0, h)) #
    list.append(Geom.Pnt(w, b, h)) #
    list.append(Geom.Pnt(0, b, h)) #

    return list

def faces():

    def createFace(a, b, c, d):
        list.append(a)
        list.append(b)
        list.append(c)
        list.append(d)
        list.append(-2) # Closing the Loop
        list.append(-1) # Closing the Face

    #---------------------------------------------------------------------------
    # Creating an list o faces (the order is not important).
    # Every face is defined connecting a min. 3 vertices in ANTICLOCKWISE order.
    #---------------------------------------------------------------------------
    list = []

    # Bottom face
    createFace(3, 2, 1, 0)

    # Top face
    createFace(4, 5, 6, 7)

    # Side faces
    createFace(0, 1, 5, 4)
    createFace(1, 2, 6, 5)
    createFace(2, 3, 7, 6)
    createFace(3, 0, 4, 7)

    return list

#---------------------------------------------------------------
# Getting the document, creating the geometry and the element...
#---------------------------------------------------------------
app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
facetedBrep = lx.FacetedBrep.createIn(doc)
elem = lx.Element.createIn(doc)
elem.setGeometry(facetedBrep)

facetedBrep.setPoints(vertices(2, 2, 2)) # This is parametric
facetedBrep.setModel(faces())

doc.recompute()