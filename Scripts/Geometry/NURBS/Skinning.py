# ===============================================================================
#
# SKINNING
#
# Skinning is a modeling technique that fits a surface through a series of
# curves and builds the required topology for the resulting Shape.
# Skinning can be used to create closed, solid shapes as well as open,
# solid shapes.
#
# ===============================================================================

import OpenLxApp as lx
import OpenLxCmd as cmd
import Base
import Geom
import Topo

if __name__ == "__main__":
    # ----------------------------
    # 1. Get the active document.
    # ----------------------------
    app = lx.Application.getInstance()
    doc = app.getActiveDocument()

    # ----------------------------------------------------------------------------------------
    # 2. Create three Shapes to be connected
    # ----------------------------------------------------------------------------------------
    ellipse1 = lx.Ellipse.createIn(doc)
    ellipse1.setSemiAxis1(4)
    ellipse1.setSemiAxis2(2)
    
    ellipse2 = lx.Ellipse.createIn(doc)
    ellipse2.setSemiAxis1(3)
    ellipse2.setSemiAxis2(2)
    
    t = Geom.Trsf()
    shape1 = ellipse1.computeShape()
    
    t.setTranslationPart(Geom.Vec(0.,0.,5.))
    shape2 = Topo.ShapeTool.transformed(shape1, t)
    
    t.setTranslationPart(Geom.Vec(0.,0.,7.5))
    shape3 = Topo.ShapeTool.transformed(ellipse2.computeShape(), t)
    
    # ----------------------------------------------------------------------------------------
    # 3. Remove the temporary Geometries
    # ----------------------------------------------------------------------------------------
    doc.removeObject(ellipse1)
    doc.removeObject(ellipse2)

    # ----------------------------------------------------------------------------------------
    # 4. Add the Shapes to a vector in the order they need to be connected
    # ----------------------------------------------------------------------------------------
    shapes = Topo.vector_ConstShape()
    shapes.append(shape1)
    shapes.append(shape2)
    shapes.append(shape3)

    # ----------------------------------------------------------------------------------------
    # 5. Create the NURBS
    # ----------------------------------------------------------------------------------------
    c = cmd.CmdAddSkinLinearNURBS(shapes)
    if c.redo():
        # Get the Element and do something with it
        e = c.getElement()
        e.setDiffuseColor(Base.Color_fromCdwkColor(70))

    # ----------------------------------------------------------------------------------------
    # 6. Recompute the document
    # ----------------------------------------------------------------------------------------
    doc.recompute()
