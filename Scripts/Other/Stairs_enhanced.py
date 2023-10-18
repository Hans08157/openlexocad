# Script GUID : {A921A948-076F-4EAA-8203-DF69585D9491}

# LexoCad libraries
import os
import App, Base, Core, Geom, Gui, Part   ###### HPK Added ###### -> Core added

# UI libraries
from PySide2 import QtCore, QtGui, QtWidgets

##### HPK Added ######
# Tool classes
class ParamElemTool:
    def __init__(self, pyService):
        self._pyService = pyService     
          
    def getDouble(self, propName):
        p = Core.castToPropertyScriptParam(self._pyService.getPropertyByName(propName))
        value = p.getValue().toDouble()
        return value
      
    def getInteger(self, propName):
        p = Core.castToPropertyScriptParam(self._pyService.getPropertyByName(propName))
        value = p.getValue().toInteger()
        return value

    def isSameScript(self):
        s = Base.StringTool.toString('{A921A948-076F-4EAA-8203-DF69585D9491}')
        return (self._pyService.scriptGUID.getValue().isEqual(s))
        
    def saveSingleValue(self, aMember, aPropertyName, isVisibleInUI):
        # Maybe create property or use existing.        
        prop = Core.castToPropertyScriptParam(self._pyService.getPropertyByName(aPropertyName))
        value = Core.Variant(aMember)
        #print variant.getTypeAsString()        
        if prop:
            prop.setValue(value)
            prop.setVisibleInUI = isVisibleInUI
        else:
            prop = self._pyService.addPropertyScriptParam(aPropertyName,value)
            prop.setVisibleInUI = isVisibleInUI

class ActiveElementWrapper:
    def __init__(self, activeElem):
        self._activeElem = activeElem
        
    def isSameScript(self):
        if  self._activeElem:
            pyService =  self._activeElem.getParamElementPythonService()
            tool = ParamElemTool(pyService)
            if pyService and tool.isSameScript():
                return True
            else:
                return False
        else:
            return False
            
    def getActiveElement(self):
        return self._activeElem
        
    


# Stairs generator class
class StairCreator:
    _epsilon = 0.0001
    
    def __init__(self, length, width, height, stepNum, stepHeight):
        self._length = length
        self._width = width
        self._height = height
        
        self._stepNum = stepNum
        self._stepHeight = stepHeight
        self._lastStepHeight = self.calcLastStepHeight()
        
    @staticmethod
    def createStepNum(length, width, height, stepNum):
        if (height > StairCreator._epsilon) and (stepNum > 0):
            stepHeight = height / stepNum
            return StairCreator(length, width, height, stepNum, stepHeight)
        else:
            return StairCreator(length, width, height, 1, height)
        
    def setIdentityStepNumAndHeights(self):
        self._stepNum = 1
        self._stepHeight = self._height
        self._lastStepHeight = self._height
        
    def calcLastStepHeight(self):
        if self._stepNum > 0:
            stepNumM1 = self._stepNum - 1
            return self._height - (self._stepHeight * float(stepNumM1))
        else:
            return self._height
        
    def calcStepNumAndLastStepHeight(self):
        if self._height <= self._epsilon or self._stepHeight <= self._epsilon:
            self.setIdentityStepNumAndHeights()
        else:
            self._lastStepHeight = self._height % self._stepHeight
            clearStepNum = int(self._height // self._stepHeight)
            if clearStepNum > 0:
                if self._lastStepHeight > self._epsilon:
                    self._stepNum = clearStepNum + 1
                else:
                    self._stepNum = clearStepNum
                    self._lastStepHeight = self.calcLastStepHeight()
            else:
                self.setIdentityStepNumAndHeights()
        
    def setLength(self, length):
        self._length = length
        
    def length(self):
        return self._length
    
    def setWidth(self, width):
        self._width = width
        
    def width(self):
        return self._width
    
    def setHeight(self, height):
        self._height = height
        self.calcStepNumAndLastStepHeight() 
                
    def height(self):
        return self._height
    
    def setStepNum(self, stepNum):
        if stepNum > 1:
            self._stepNum = stepNum
            self._stepHeight = self._height / float(stepNum)
            self._lastStepHeight = self.calcLastStepHeight()
        else:
            self.setIdentityStepNumAndHeights()
            
    def stepNum(self):
        return self._stepNum
    
    def setStepHeight(self, stepHeight):
        if(stepHeight > self._epsilon):
            self._stepHeight = stepHeight
            if self._stepNum > 1:
                lowHeight = self._stepHeight * float(self._stepNum - 1)
                if lowHeight < (self._height - self._epsilon):
                    self._lastStepHeight = self._height - lowHeight
                else:
                    self._stepNum -= 1
                    self._stepHeight = self._height / float(self._stepNum)
                    self._lastStepHeight = self._stepHeight
            else:
                if stepHeight < (self._height - self._epsilon):
                    self._stepNum = 2
                    self._stepHeight = stepHeight
                    self._lastStepHeight = self._height - self._stepHeight
                else:
                    self.setIdentityStepNumAndHeights()
        else:
            self.setIdentityStepNumAndHeights()
    
    def stepHeight(self):
        return self._stepHeight
    
    def setLastStepHeight(self, lastStepHeight):
        if lastStepHeight > self._epsilon:
            remainingHeight = self._height - lastStepHeight
            if (remainingHeight > self._epsilon) and (self._stepNum > 1):
                self._stepHeight = remainingHeight / float(self._stepNum - 1)
                self._lastStepHeight = lastStepHeight
            else:
                self.setIdentityStepNumAndHeights()
        else:
            if (self._height > self._epsilon) and (self._stepNum > 0):
                self._stepHeight = self._height / float(self._stepNum)
            else:
                self.setIdentityStepNumAndHeights()
    
    def lastStepHeight(self):
        return self._lastStepHeight
    
    def _genRightProfilePoints(self, vtxList):
        stepLength = self._length / float(self._stepNum)
        backBorder = max(self._stepHeight, self._lastStepHeight)
        
        stepTopVec = Geom.Vec(stepLength, 0.0, 0.0)
        stepSideVec = Geom.Vec(0.0, 0.0, -self._stepHeight)
        
        startPt = Geom.Pnt(0.0, 0.0, self._height)
        penPt = Geom.Pnt(startPt)
        vtxList.append(Geom.Pnt(penPt))
        penPt.translate(stepTopVec)
        vtxList.append(Geom.Pnt(penPt))
        penPt.translate(Geom.Vec(0.0, 0.0, -self._lastStepHeight))
        vtxList.append(Geom.Pnt(penPt))
        if self._stepNum > 1:
            for step in range(1, self._stepNum):
                penPt.translate(stepTopVec)
                vtxList.append(Geom.Pnt(penPt))
                penPt.translate(stepSideVec)
                vtxList.append(Geom.Pnt(penPt))
                
            penPt.translate(Geom.Vec(-(stepLength * 1.5), 0.0, 0.0))
            vtxList.append(Geom.Pnt(penPt))
            
            lastPt = Geom.Pnt(startPt)
            lastPt.translate(Geom.Vec(0.0, 0.0, -(self._lastStepHeight + (self._stepHeight * 0.5))))
            vtxList.append(Geom.Pnt(lastPt))
        else:
            vtxList.append(Geom.Pnt(0.0, 0.0, 0.0))
    
    def _transProfilePoints(self, srcVtxList, vtxList, dPos):
        transPtList = Geom.vector_Pnt()
        for srcPt in srcVtxList:
            dstPt = Geom.Pnt(srcPt)
            dstPt.translate(dPos)
            
            vtxList.append(dstPt)
    
    def _genSideProfileFace(self, startIndex, vtxCount, revOrder, indexList):
        indexList += range(startIndex, startIndex + vtxCount, 1)
        if revOrder:
            indexList.reverse()
            
        indexList.append(-2) # Closing the Loop
        indexList.append(-1) # Closing the Face
        
    def _genBridgeFaces(self, profVtxCount, indexList):
        for vtxId in range(profVtxCount):
            nextVtxId = (vtxId + 1) % profVtxCount
            
            indexList.append(vtxId)
            indexList.append(nextVtxId)
            indexList.append(nextVtxId + profVtxCount)
            indexList.append(vtxId + profVtxCount)
            
            indexList.append(-2) # Closing the Loop
            indexList.append(-1) # Closing the Face


    ###### HPK Added ######         
    def _saveValues(self, stair):   
        # If the App.ParamElementPythonService does not exist we create a new one
        pyService = stair.getParamElementPythonService()
        if not pyService:
            pyService = App.createParamElementPythonService(doc)
            # Save location of script
            fileName = Core.getCurrentScriptFilePath()
            print(Base.StringTool.toStlString(fileName))
            pyService.fileName.setValue(fileName)
            # Save GUID of script. @See top of document
            pyService.scriptGUID.setValue(Base.StringTool.toString('{A921A948-076F-4EAA-8203-DF69585D9491}'))
            stair.setParamElementPythonService(pyService)
        
        # Save the properties of the StepCreator to the stair's App.ParamElementPythonService       
        tool = ParamElemTool(pyService)            
        tool.saveSingleValue(self._length, '_length', True)
        tool.saveSingleValue(self._width, '_width', True)
        tool.saveSingleValue(self._height, '_height', True)
        tool.saveSingleValue(self._stepNum, '_stepNum', True)
        tool.saveSingleValue(self._stepHeight, '_stepHeight', True)       
     
    # Creates a new element
    def _createElement(self, doc, vtxList, indexList, pickedPoint):
        geom = Part.createFacetedBrep(doc)
        geom.points.setValue(vtxList)
        geom.model.setValue(indexList)
        
        #stair = App.createElement(doc)
        ##### HPK Added ######      
        stair = App.createStair(doc)
        stair.placement.setLocalPlacement(Geom.Ax2(pickedPoint, Geom.Dir(0.,0.,1.)))
        stair.setGeometry(geom)     
        self._saveValues(stair)
            
    # Modifies an existing element
    ##### HPK Added ######  
    def _modifyElement(self, doc, vtxList, indexList, activeElem):
        geom = Part.createFacetedBrep(doc)
        geom.points.setValue(vtxList)
        geom.model.setValue(indexList)
        
        ##### HPK Added ######      
        if activeElem:
            activeElem.setGeometry(geom)
            self._saveValues(activeElem)
            
    def createStairs(self, doc, pickedPoint):
        if (self._length < self._epsilon) or \
                (self._width < self._epsilon) or \
                (self._height < self._epsilon):
            return   

        vtxList = Geom.vector_Pnt()
        self._genRightProfilePoints(vtxList)
        profileVtxCount = len(vtxList)
        self._transProfilePoints(vtxList[:], vtxList, Geom.Vec(0.0, self._width, 0.0))       
        
        indexList = []
        self._genSideProfileFace(0, profileVtxCount, True, indexList)                   #Right profile
        self._genBridgeFaces(profileVtxCount, indexList)
        self._genSideProfileFace(profileVtxCount, profileVtxCount, False, indexList)    #Left profile
        
        self._createElement(doc, vtxList, indexList, pickedPoint)
     
    ##### HPK Added ######   
    def modifyStairs(self, doc, activeElem):
        if (self._length < self._epsilon) or \
                (self._width < self._epsilon) or \
                (self._height < self._epsilon):
            return 

        vtxList = []
        self._genRightProfilePoints(vtxList)
        profileVtxCount = len(vtxList)
        self._transProfilePoints(vtxList[:], vtxList, Geom.Vec(0.0, self._width, 0.0))       
        
        indexList = []
        self._genSideProfileFace(0, profileVtxCount, True, indexList)                   #Right profile
        self._genBridgeFaces(profileVtxCount, indexList)
        self._genSideProfileFace(profileVtxCount, profileVtxCount, False, indexList)    #Left profile   
        
        self._modifyElement(doc, vtxList, indexList, activeElem)

# Options dialog class
class Ui_StairDlg(object):
    def setupUi(self, StairDlg):
        StairDlg.setObjectName("StairDlg")
        StairDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        StairDlg.resize(400, 300)
        StairDlg.setModal(True)
        self.mainBox = QtWidgets.QVBoxLayout(StairDlg)
        self.mainBox.setObjectName("mainBox")
        self.ctrlBox = QtWidgets.QFormLayout()
        self.ctrlBox.setHorizontalSpacing(36)
        self.ctrlBox.setVerticalSpacing(6)
        self.ctrlBox.setObjectName("ctrlBox")
        self.lengthLbl = QtWidgets.QLabel(StairDlg)
        self.lengthLbl.setObjectName("lengthLbl")
        self.ctrlBox.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lengthLbl)
        self.lengthSpBox = QtWidgets.QDoubleSpinBox(StairDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lengthSpBox.sizePolicy().hasHeightForWidth())
        self.lengthSpBox.setSizePolicy(sizePolicy)
        self.lengthSpBox.setMaximum(10000.0)
        self.lengthSpBox.setObjectName("lengthSpBox")
        self.ctrlBox.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lengthSpBox)
        self.widthLbl = QtWidgets.QLabel(StairDlg)
        self.widthLbl.setObjectName("widthLbl")
        self.ctrlBox.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.widthLbl)
        self.widthSpBox = QtWidgets.QDoubleSpinBox(StairDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widthSpBox.sizePolicy().hasHeightForWidth())
        self.widthSpBox.setSizePolicy(sizePolicy)
        self.widthSpBox.setMaximum(10000.0)
        self.widthSpBox.setObjectName("widthSpBox")
        self.ctrlBox.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.widthSpBox)
        self.heightLbl = QtWidgets.QLabel(StairDlg)
        self.heightLbl.setObjectName("heightLbl")
        self.ctrlBox.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.heightLbl)
        self.heightSpBox = QtWidgets.QDoubleSpinBox(StairDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.heightSpBox.sizePolicy().hasHeightForWidth())
        self.heightSpBox.setSizePolicy(sizePolicy)
        self.heightSpBox.setMaximum(10000.0)
        self.heightSpBox.setObjectName("heightSpBox")
        self.ctrlBox.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.heightSpBox)
        self.stepsLbl = QtWidgets.QLabel(StairDlg)
        self.stepsLbl.setObjectName("stepsLbl")
        self.ctrlBox.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.stepsLbl)
        self.numberSpBox = QtWidgets.QSpinBox(StairDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberSpBox.sizePolicy().hasHeightForWidth())
        self.numberSpBox.setSizePolicy(sizePolicy)
        self.numberSpBox.setMaximum(99999999)
        self.numberSpBox.setObjectName("numberSpBox")
        self.ctrlBox.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.numberSpBox)
        self.fstStepHLbl = QtWidgets.QLabel(StairDlg)
        self.fstStepHLbl.setObjectName("fstStepHLbl")
        self.ctrlBox.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.fstStepHLbl)
        self.fstStepHSpBox = QtWidgets.QDoubleSpinBox(StairDlg)
        self.fstStepHSpBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fstStepHSpBox.sizePolicy().hasHeightForWidth())
        self.fstStepHSpBox.setSizePolicy(sizePolicy)
        self.fstStepHSpBox.setMinimum(0.01)
        self.fstStepHSpBox.setMaximum(10000.0)
        self.fstStepHSpBox.setSingleStep(0.01)
        self.fstStepHSpBox.setObjectName("fstStepHSpBox")
        self.ctrlBox.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.fstStepHSpBox)
        self.lastStepHLbl = QtWidgets.QLabel(StairDlg)
        self.lastStepHLbl.setObjectName("lastStepHLbl")
        self.ctrlBox.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.lastStepHLbl)
        self.lastStepHSpBox = QtWidgets.QDoubleSpinBox(StairDlg)
        self.lastStepHSpBox.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lastStepHSpBox.sizePolicy().hasHeightForWidth())
        self.lastStepHSpBox.setSizePolicy(sizePolicy)
        self.lastStepHSpBox.setMinimum(0.01)
        self.lastStepHSpBox.setMaximum(10000.0)
        self.lastStepHSpBox.setSingleStep(0.01)
        self.lastStepHSpBox.setObjectName("lastStepHSpBox")
        self.ctrlBox.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.lastStepHSpBox)
        self.topLbl = QtWidgets.QLabel(StairDlg)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setUnderline(True)
        self.topLbl.setFont(font)
        self.topLbl.setObjectName("topLbl")
        self.ctrlBox.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.topLbl)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.ctrlBox.setItem(4, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.mainBox.addLayout(self.ctrlBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(StairDlg)
        font = QtGui.QFont()
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.mainBox.addWidget(self.buttonBox)

        self.retranslateUi(StairDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), StairDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), StairDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(StairDlg)

    def retranslateUi(self, StairDlg):
        StairDlg.setWindowTitle(QtWidgets.QApplication.translate("StairDlg", "Create", None, -1))
        self.lengthLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Length", None, -1))
        self.widthLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Width", None, -1))
        self.heightLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Height", None, -1))
        self.stepsLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Number of steps", None, -1))
        self.fstStepHLbl.setText(QtWidgets.QApplication.translate("StairDlg", "1. Step height", None, -1))
        self.lastStepHLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Last step height", None, -1))
        self.topLbl.setText(QtWidgets.QApplication.translate("StairDlg", "Stair", None, -1))

class StairDlg(QtWidgets.QDialog, Ui_StairDlg):
    def __init__(self, parent=None):
        super(StairDlg, self).__init__(parent)
        
        ##### HPK Added ######
        doc = App.Application.instance().getActiveDocument()
        activeElem = Gui.getActiveElement(doc)

        length = 4.0
        width = 3.0
        height = 2.0        
        stepNum = 10
        
        # Check if active element was created with this script
        # If 'true' we fetch the properties from the App.ParamElementPythonService
        if activeElem:
            pyService = activeElem.getParamElementPythonService()
            tool = ParamElemTool(pyService)
            if pyService and tool.isSameScript():
                length  = tool.getDouble('_length')
                width   = tool.getDouble('_width')
                height  = tool.getDouble('_height')
                stepNum = tool.getInteger('_stepNum')
            else:
                print('The Element was not created with this script!')

                ##### END - HPK Added ######
        
        self.stairCreator = StairCreator.createStepNum(length, width, height, stepNum)
        self._insideUIUpdate = False        
        
        self.setupUi(self)
        self.initEvents()
        self.updateValues()
        
    def initEvents(self):
        self.lengthSpBox.valueChanged.connect(self.onLengthChanged)
        self.widthSpBox.valueChanged.connect(self.onWidthChanged)
        self.heightSpBox.valueChanged.connect(self.onHeightChanged)
        
        self.numberSpBox.valueChanged.connect(self.onNumberChanged)
        
        self.fstStepHSpBox.valueChanged.connect(self.onFirstHeightChanged)
        self.lastStepHSpBox.valueChanged.connect(self.onLastHeightChanged)
        
    def updateValues(self):
        self._insideUIUpdate = True

        self.lengthSpBox.setValue(self.stairCreator.length())
        self.widthSpBox.setValue(self.stairCreator.width())
        self.heightSpBox.setValue(self.stairCreator.height())
        
        self.numberSpBox.setValue(self.stairCreator.stepNum())
        
        self.fstStepHSpBox.setValue(self.stairCreator.stepHeight())
        self.lastStepHSpBox.setValue(self.stairCreator.lastStepHeight())
        
        self._insideUIUpdate = False
        
    def onLengthChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setLength(val)
            self.updateValues()
            
    def onWidthChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setWidth(val)
            self.updateValues()
            
    def onHeightChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setHeight(val)
            self.updateValues()
            
    def onNumberChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setStepNum(val)
            self.updateValues()
            
    def onFirstHeightChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setStepHeight(val)
            self.updateValues()
            
    def onLastHeightChanged(self, val):
        if not self._insideUIUpdate:
            self.stairCreator.setLastStepHeight(val)
            self.updateValues()

if __name__ == '__main__':

    ##### HPK Added ######
    doc = App.Application.instance().getActiveDocument()
    actElemWrapper = ActiveElementWrapper(Gui.getActiveElement(doc))
    
    if actElemWrapper.isSameScript():
        # Modify stairs
        stairDlg = StairDlg();
        result = stairDlg.exec_()
        if result == QtWidgets.QDialog.Accepted:
            stairDlg.stairCreator.modifyStairs(doc, Gui.getActiveElement(doc)) 
    
    else:
        # Make new stairs        
        stairDlg = StairDlg();
        result = stairDlg.exec_()
        if result == QtWidgets.QDialog.Accepted:
            Gui.pickPoint(doc)
            pickedPoint = Gui.getPickedPoint(doc)
            stairDlg.stairCreator.createStairs(doc, pickedPoint) 
    
           
    
    doc.recompute()