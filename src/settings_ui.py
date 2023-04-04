# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(699, 230)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(13, 12, 681, 211))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_Ipv4Result = QtWidgets.QLabel(self.layoutWidget)
        self.label_Ipv4Result.setObjectName("label_Ipv4Result")
        self.gridLayout.addWidget(self.label_Ipv4Result, 1, 1, 1, 1)
        self.label_DataCaptureBlocks = QtWidgets.QLabel(self.layoutWidget)
        self.label_DataCaptureBlocks.setObjectName("label_DataCaptureBlocks")
        self.gridLayout.addWidget(self.label_DataCaptureBlocks, 5, 0, 1, 1)
        self.label_Status = QtWidgets.QLabel(self.layoutWidget)
        self.label_Status.setObjectName("label_Status")
        self.gridLayout.addWidget(self.label_Status, 2, 0, 1, 1)
        self.label_MacAddress = QtWidgets.QLabel(self.layoutWidget)
        self.label_MacAddress.setObjectName("label_MacAddress")
        self.gridLayout.addWidget(self.label_MacAddress, 0, 0, 1, 1)
        self.lineEdit_DesignFilePath = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_DesignFilePath.setObjectName("lineEdit_DesignFilePath")
        self.gridLayout.addWidget(self.lineEdit_DesignFilePath, 6, 1, 1, 1)
        self.label_DeviceStatus = QtWidgets.QLabel(self.layoutWidget)
        self.label_DeviceStatus.setObjectName("label_DeviceStatus")
        self.gridLayout.addWidget(self.label_DeviceStatus, 3, 0, 1, 1)
        self.lineEdit_MacResult = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_MacResult.setObjectName("lineEdit_MacResult")
        self.gridLayout.addWidget(self.lineEdit_MacResult, 0, 1, 1, 1)
        self.label_NumProgrValueBlocks = QtWidgets.QLabel(self.layoutWidget)
        self.label_NumProgrValueBlocks.setObjectName("label_NumProgrValueBlocks")
        self.gridLayout.addWidget(self.label_NumProgrValueBlocks, 4, 0, 1, 1)
        self.label_StatusResult = QtWidgets.QLabel(self.layoutWidget)
        self.label_StatusResult.setObjectName("label_StatusResult")
        self.gridLayout.addWidget(self.label_StatusResult, 2, 1, 1, 1)
        self.label_DeviceStatusResult = QtWidgets.QLabel(self.layoutWidget)
        self.label_DeviceStatusResult.setObjectName("label_DeviceStatusResult")
        self.gridLayout.addWidget(self.label_DeviceStatusResult, 3, 1, 1, 1)
        self.label_DesignFilePath = QtWidgets.QLabel(self.layoutWidget)
        self.label_DesignFilePath.setObjectName("label_DesignFilePath")
        self.gridLayout.addWidget(self.label_DesignFilePath, 6, 0, 1, 1)
        self.label_Ipv4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_Ipv4.setObjectName("label_Ipv4")
        self.gridLayout.addWidget(self.label_Ipv4, 1, 0, 1, 1)
        self.pushButton_BrowseDesignFilePath = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_BrowseDesignFilePath.setObjectName("pushButton_BrowseDesignFilePath")
        self.gridLayout.addWidget(self.pushButton_BrowseDesignFilePath, 6, 2, 1, 1)
        self.label_NumProgrValueBlocksResult = QtWidgets.QLabel(self.layoutWidget)
        self.label_NumProgrValueBlocksResult.setObjectName("label_NumProgrValueBlocksResult")
        self.gridLayout.addWidget(self.label_NumProgrValueBlocksResult, 4, 1, 1, 1)
        self.label_DataCaptureBlocksResult = QtWidgets.QLabel(self.layoutWidget)
        self.label_DataCaptureBlocksResult.setObjectName("label_DataCaptureBlocksResult")
        self.gridLayout.addWidget(self.label_DataCaptureBlocksResult, 5, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_Find = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Find.setCheckable(False)
        self.pushButton_Find.setObjectName("pushButton_Find")
        self.gridLayout_2.addWidget(self.pushButton_Find, 0, 0, 1, 1)
        self.pushButton_Connect = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Connect.setObjectName("pushButton_Connect")
        self.gridLayout_2.addWidget(self.pushButton_Connect, 1, 0, 1, 1)
        self.pushButton_LoadDesign = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_LoadDesign.setObjectName("pushButton_LoadDesign")
        self.gridLayout_2.addWidget(self.pushButton_LoadDesign, 2, 0, 1, 1)
        self.pushButton_Stop = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.gridLayout_2.addWidget(self.pushButton_Stop, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.pushButton_Cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.gridLayout_2.addWidget(self.pushButton_Cancel, 6, 0, 1, 1)
        self.pushButton_Start = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_Start.setObjectName("pushButton_Start")
        self.gridLayout_2.addWidget(self.pushButton_Start, 3, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButton_Cancel.clicked.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pushButton_Find, self.pushButton_Cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Find and Replace"))
        self.label_Ipv4Result.setText(_translate("Dialog", "000.000.000.000"))
        self.label_DataCaptureBlocks.setText(_translate("Dialog", "Number of DataCaptureBlocks:"))
        self.label_Status.setText(_translate("Dialog", "Connection Status:"))
        self.label_MacAddress.setText(_translate("Dialog", "MAC:"))
        self.label_DeviceStatus.setText(_translate("Dialog", "Device Status:"))
        self.label_NumProgrValueBlocks.setText(_translate("Dialog", "Number of ProgrammableValueBlocks:"))
        self.label_StatusResult.setText(_translate("Dialog", "Not Connected"))
        self.label_DeviceStatusResult.setText(_translate("Dialog", "Not Running"))
        self.label_DesignFilePath.setText(_translate("Dialog", "Design File Path:"))
        self.label_Ipv4.setText(_translate("Dialog", "IP v4:"))
        self.pushButton_BrowseDesignFilePath.setText(_translate("Dialog", "Browse"))
        self.label_NumProgrValueBlocksResult.setText(_translate("Dialog", "0"))
        self.label_DataCaptureBlocksResult.setText(_translate("Dialog", "0"))
        self.pushButton_Find.setText(_translate("Dialog", "&Find"))
        self.pushButton_Connect.setText(_translate("Dialog", "Connect"))
        self.pushButton_LoadDesign.setText(_translate("Dialog", "Load"))
        self.pushButton_Stop.setText(_translate("Dialog", "Stop"))
        self.pushButton_Cancel.setText(_translate("Dialog", "&Cancel"))
        self.pushButton_Start.setText(_translate("Dialog", "Start"))
