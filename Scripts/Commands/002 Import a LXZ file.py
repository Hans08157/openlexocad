#==============================================================================
#
# IMPORT FILE - Import an external lxz file. Importing a file will get all the
# elements out of it and merge them into the current document (as opposed to
# OPENING a file, where the whole scene will be replaced).
#
#==============================================================================

import os
import Base, Geom
import OpenLxApp as lx
import OpenLxUI  as ui
import OpenLxCmd as cmd

app   = lx.Application.getInstance()
doc   = app.getActiveDocument()
lxstr = Base.StringTool.toString
cstr  = Base.StringTool.toStlString

lxz_file = "C:/Users/Hans/Desktop/test.lxz"

# Test if the file really exists. If you omit this and the file does not exists, Lexocad will still show a warning.
if os.path.isfile(lxz_file):
    # Use "cmd = Gui.CmdImportFile()" to have Lexocad asking for a file
    cmd = cmd.CmdImportFile(lxstr(lxz_file), "lxz")
    if cmd.redo():
        # Use "elements = doc.getElements()" to get ALL elements in the document instead
        elements = lx.vector_Element(cmd.getImportedElements())

        for e in elements:
            if cstr(e.getUserName()) == "Cube":
                e.setDiffuseColor(Base.Color(255, 0, 0))
        
        doc.recompute()
    