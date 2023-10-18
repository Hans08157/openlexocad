#==========================================
#
# TOP VIEW - Switch to top view mode
#
#==========================================

import Base, Gui
a = Gui.Lexocad().getActionByName(Base.StringTool.toQString(Base.StringTool.toString("viewZAction2")))
if a is not None:
 a.toggle()
 # a.toggled(True) <= Force Top View