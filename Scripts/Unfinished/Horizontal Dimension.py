#===============================================================================
#
# DISCLAIMER
#
# Some methods used in this script are not part of the official API and may be
# not available in the future (i.e. creating objects by type name and accessing
# properties by name).
#  
#===============================================================================

import App, Base, Geom

anchorP1 = Geom.Pnt(0,0,0)
anchorP2 = Geom.Pnt(10,10,0)
passageP = Geom.Pnt(0,-5,0)

doc = App.castToDocument(App.GetApplication().getActiveDocument())

hDim = App.castToGeometry(doc.createObjectFromTypeName("Annotation::HorizontalDimension"))
r = hDim.setProperty("startPoint", anchorP1)
r = hDim.setProperty("endPoint", anchorP2)
r = hDim.setProperty("dimensionCurvePassingPoint", passageP)
r = hDim.setProperty("dimensionCurveDirection", Geom.Dir(Geom.Vec(anchorP1,anchorP2)))

elem = App.castToElement(doc.createObjectFromTypeName("Annotation::DimensionElement"))
elem.setGeometry(hDim)
doc.recompute()