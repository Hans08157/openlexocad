#===============================================================================
#
# GET THE FOLDERS THAT ARE SHOWN IN THE INFO DIALOG OF LEXOCAD
#
#===============================================================================

#-----------------------------
# 1. Import Lexocad libraries.
#-----------------------------
import App, Base, Core

#-----------------------------------------------
# 2. Get all the folders like the "Info" dialog.
#-----------------------------------------------
curDir = Base.StringTool.toStlString(Base.StringTool.toString(Core.Settings.getInstance().getOpenFileDir()))
exeDir = Base.StringTool.toStlString(App.GetApplication().getApplicationPath())
tmpDir = Base.StringTool.toStlString(App.GetApplication().getActiveDocument().getTmpDirectory()) 
usrDir = Base.StringTool.toStlString(Base.StringTool.toString(Core.Settings.getInstance().getCadworkUserprofile()))
catDir = Base.StringTool.toStlString(Base.StringTool.toString(Core.Settings.getInstance().getUserCatalogDir()))

# Some of the functions above may return '/' or '\\' as separator for folders. In Python they are both valid.