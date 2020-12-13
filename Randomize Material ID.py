# randomize metrial ID on all materials
    
#################################################################
# Libs
from PySide2 import QtCore, QtGui, QtWidgets

importError = False
try:
    import vrMaterialPtr
    import vrMaterialEditor
    import vrFieldAccess
    import random
except ImportError:
    importError = True
    pass

import uiTools

#################################################################
# Build Menu
vrRandomizeMaterialID_form, vrRandomizeMaterialID_base = uiTools.loadUiType('Randomize Material ID.ui')

class vrRandomizeMaterialID(vrRandomizeMaterialID_form, vrRandomizeMaterialID_base):
    def __init__(self, parent=None):
        super(vrRandomizeMaterialID, self).__init__(parent)
        parent.layout().addWidget(self)
        self.parent = parent
        self.setupUi(self)

        # add resize grip in bottom right corner.
        self.sizeGrip = QtWidgets.QSizeGrip(parent);
        self.sizeGrip.setFixedSize(16, 16)
        self.sizeGrip.move(parent.rect().bottomRight() - self.sizeGrip.rect().bottomRight())
        self.sizeGrip.raise_()
        self.sizeGrip.show()
        
        self._Randomize_Material_ID.clicked.connect(self.randomizeMaterialID)
        
    def resizeEvent(self, event):
        # move resize grip to bottom right corner.
        self.sizeGrip.move(self.parent.rect().bottomRight() - self.sizeGrip.rect().bottomRight())
        self.sizeGrip.raise_()

    def randomizeMaterialID(self):
        newIDList = []
        counter = 0
        allMaterials = vrMaterialPtr.getAllMaterials()
        print("Material managed :")
        for material in allMaterials:
            if material.fields().hasField("colorComponentData"):
                colorComponentData = vrFieldAccess.vrFieldAccess(material.fields().getFieldContainer("colorComponentData"))
                if colorComponentData:
                    materialID = colorComponentData.getUInt32("materialID")
                    newMaterialID = random.randrange(1, 32)
                    if newMaterialID in newIDList:
                        newMaterialID = random.randrange(1, 32)
                        if newMaterialID in newIDList:
                            newMaterialID = random.randrange(1, 32)
                    if counter == 2:
                        newIDList.clear()
                        counter = 0
                    newIDList.append(newMaterialID)
                    counter = counter + 1
                    colorComponentData.setUInt32("materialID", newMaterialID)
                    # print(materialID, newMaterialID, newIDList, counter)
                    print(material.getName() + " -Old ID: " + str(materialID) + " -New ID: " + str(newMaterialID))
                    vrMaterialEditor.updateMaterials()
    
if not importError:
    randomizeMatID = vrRandomizeMaterialID(VREDPluginWidget)
