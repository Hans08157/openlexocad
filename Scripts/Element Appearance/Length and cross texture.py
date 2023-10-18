# OpenLexocad libraries
import OpenLxApp as lx
import OpenLxUI  as ui
import Base, Core, Geom, Draw

lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

doc   = lx.Application.getInstance().getActiveDocument()
uidoc = ui.UIApplication.getInstance().getUIDocument(doc)
sel   = uidoc.getSelection()

    
if __name__ == "__main__": 

    lenghttexname = lxstr("C:/Users/knoll/Desktop/sapin.png")
    crosstexname  = lxstr("C:/Users/knoll/Desktop/sapin_section.png")

    block = lx.Block.createIn(doc)
    elem = lx.Element.createIn(doc)
    elem.setGeometry(block)
    block.setXLength(5)
    block.setYLength(.12)
    block.setZLength(.24)
    lengthTexture = Draw.Texture2()
    lengthTexture.setTextureFileName(lenghttexname)
    lengthTexture.setTextureOriginalFileName(lenghttexname)
    lengthTexture.setMappingModel(Draw.Texture2.MODULATE)

    crossTexture = Draw.Texture2()
    crossTexture.setTextureFileName(crosstexname) 
    crossTexture.setTextureOriginalFileName(crosstexname)
    crossTexture.setMappingModel(Draw.Texture2.MODULATE)

    elem.setLengthAndCrossTexture(lengthTexture, crossTexture)
    doc.recompute()