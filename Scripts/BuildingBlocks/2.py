#!/usr/bin/python
# -*- coding: utf-8 -*-

import OpenLxApp
if __name__ == "__main__":
    thisScript = OpenLxApp.Application.getInstance().getActiveScript()
    if thisScript.isDragAndDropped():
        OpenLxCmd.CmdAddStructuralCurveConnection(thisScript.getInsertionPoint()).redo()
    else:
        OpenLxCmd.CmdAddStructuralCurveConnection().redo()
