#===============================================================================
#
# CREATE AN HORIZONTAL MEASUREMENT
#  
#===============================================================================
import Annotation, App, Base, Geom

#-------------------------------------------------------------------------------
# Helper function to create HorizontalDimension elements
#-------------------------------------------------------------------------------
def createFromPoints(points, passageP):
 doc = App.castToDocument(App.GetApplication().getActiveDocument())
 while len(points) > 1:
  P1 = points[0]
  P2 = points[1]
  points.pop(0)
  
  hDim = App.castToGeometry(doc.createObjectFromTypeName("Annotation::HorizontalDimension"))
  r = hDim.setProperty("startPoint", P1)
  r = hDim.setProperty("endPoint", P2)
  r = hDim.setProperty("dimensionCurvePassingPoint", passageP)
  r = hDim.setProperty("dimensionCurveDirection", Geom.Dir(Geom.Vec(P1,P2)))
  
  ds = doc.getActiveDimensionStyle()
  ds.numberOfDecimals.setValue(0)
  
  elem = Annotation.castToDimensionElement(doc.createObjectFromTypeName("Annotation::DimensionElement"))
  elem.setGeometry(hDim)
  elem.dimensionStyle.setValue(ds)
  doc.recompute()

#-------------------------------------------------------------------------------
# Horizontal Measurement 
#-------------------------------------------------------------------------------
points = []
points.append(Geom.Pnt( 0.,0.,0.))
points.append(Geom.Pnt(10.,0.,0.))
points.append(Geom.Pnt(25.,0.,0.))
points.append(Geom.Pnt(45.,0.,0.))

Y = 0.;Z = 0.
for point in points:
 Y = max(Y, point.y()); Z = max(Z, point.z())
passageP = Geom.Pnt(0. ,Y-5., Z)

createFromPoints(points, passageP)

#-------------------------------------------------------------------------------
# Vertical Measurement 
#-------------------------------------------------------------------------------
points = []
points.append(Geom.Pnt(0., 0.,0.))
points.append(Geom.Pnt(0.,10.,0.))
points.append(Geom.Pnt(0.,25.,0.))
points.append(Geom.Pnt(0.,45.,0.))

X = 0.;Z = 0.
for point in points:
 X = max(X, point.x()); Z = max(Z, point.z())
passageP = Geom.Pnt(X-5., 0. ,Z)

createFromPoints(points, passageP)