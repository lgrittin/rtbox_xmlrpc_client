# ===============================================================================
# PYTHON INTERACTIVE GUI XMLPRC CLIENT FOR RT-BOX
# 
# Luca Grittini
# 20/03/2023
# ===============================================================================

import traceback
import sys
import socket
import time
import base64
import xmlrpc.client
import pathlib
import os
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog, QLabel, QVBoxLayout
from pyqtgraph import PlotWidget, plot
from PyQt5.QtCore import QTimer, Qt
from PyQt5.uic import loadUi
from socket import gaierror
from enum import Enum
from pathlib import Path
from main_window_ui import Ui_MainWindow
from settings_ui import Ui_Dialog

import pyqtgraph as pg
import numpy as np

# ===============================================================================
# GLOBALS
# ===============================================================================

## CONNECTIVITY
RTBOX_MACADDRESS = "20b0f7047680"
HOST_NAME = "rtbox-" + RTBOX_MACADDRESS + ".local"
HOST_IPV4 = "000.000.000.000"
HOST_ADDRESS = "http://" + HOST_IPV4 + ":9998/RPC2"
INPUTBLOCKS = [0]
OUTPUTBLOCKS = [0]
DESIGN_NAME = "sim_correnti_tensioni"
DESIGN_PATH = str(pathlib.Path().resolve().parent.joinpath('plecs_design'))
RTBOX_SERVER_XMLPRC = 0
ConnectionStatus = Enum('ConnectionStatus', ["NOT_CONNECTED", "CONNECTED"])
RTBOX_CONNECTED = ConnectionStatus.NOT_CONNECTED
RTBOX_IPFOUND = ConnectionStatus.NOT_CONNECTED
DeviceStatus = Enum('DeviceStatus', ['STOPPED', 'RUNNING', 'LOADING_DESIGN', 'DESIGN_LOADED', 'ERROR'])
RTBOX_STATUS = DeviceStatus.STOPPED
RTBOX_STATUS_INT = 0

## STATUS DISPLAY
dispListColor = ["background-color: red", "background-color: lightgreen"]
dispList_ConnectionStatus = ["Not Connected", "Connected"]
dispListColor2 = ["background-color: orange", "background-color: lightgreen", "background-color: orange"]
dispList_DeviceStatus = ["Stopped", "Running", "Error"]
dispList_Ipv4 = ["No IP", HOST_IPV4]
TOUT_settingsDialog_RefreshLabels_ms = 2000
TOUT_mainWindow_RefreshStatusBar_ms = 1500
TOUT_mainWindow_RefreshWrite_ms = 900
TOUT_mainWindow_RefreshRead_ms = 1100
TOUT_mainWindow_PlotData_ms = 700

## Specific Implementation
V_AC_Ampl = 0.0
V_AC_Freq = 50
V_AC_Ena = 0
WhiteNoise_AC_Ampl = 0.0
WhiteNoise_AC_Ena = 0
SwitchingNoise_AC_Ampl = 0.0
SwitchingNoise_AC_Freq = 680.0
SwitchingNoise_AC_Ena = 0
UnbalVoltage_AC_Ampl = 0.0
UnbalVoltage_AC_Phase = 0
UnbalVoltage_AC_Ena = 0
V_DC_Ampl1 = 0.0
V_DC_Ampl2 = 0.0
V_DC_Ampl3 = 0.0
V_DC_Ena = 0
V_DC_Link = 0
WhiteNoise_DC_Ampl = 0.0
WhiteNoise_DC_Ena = 0
SwitchingNoise_DC_Ampl = 0.0
SwitchingNoise_DC_Freq = 680.0
SwitchingNoise_DC_Ena = 0
UnbalVoltage_DC_Ampl = 0.0
UnbalVoltage_DC_Phase = 0
UnbalVoltage_DC_Ena = 0
DATA_DIM = 2000
Voltage_AC_R = np.zeros(DATA_DIM, dtype=float)
Voltage_AC_S = np.zeros(DATA_DIM, dtype=float)
Voltage_AC_T = np.zeros(DATA_DIM, dtype=float)
Voltage_DC_R = np.zeros(DATA_DIM, dtype=float)
Voltage_DC_S = np.zeros(DATA_DIM, dtype=float)
Voltage_DC_T = np.zeros(DATA_DIM, dtype=float)

# ===============================================================================
# MAIN CLASS
# ===============================================================================
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        global DATA_DIM
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("RT-Box GUI")
        ## Status Bar # ---------------------------------------------------------
        self.label_RtBoxDeviceStatusVal = QLabel(dispList_DeviceStatus[RTBOX_STATUS.value-1])
        self.label_RtBoxConnectionVal = QLabel(dispList_ConnectionStatus[RTBOX_CONNECTED.value-1])
        self.label_Ipv4Val = QLabel(dispList_Ipv4[RTBOX_IPFOUND.value-1])
        self.statusBar().addPermanentWidget(self.label_RtBoxDeviceStatusVal)
        self.statusBar().addPermanentWidget(self.label_RtBoxConnectionVal)
        self.statusBar().addPermanentWidget(self.label_Ipv4Val)
        self.timer_RefreshStatusBar = QTimer()
        self.timer_RefreshWrite = QTimer()
        self.timer_RefreshRead = QTimer()
        self.timer_PlotData = QTimer()
        ## Graph # --------------------------------------------------------------
        layout = self.groupBox_Plot.layout()#QVBoxLayout()
        if layout is None:
            layout = QVBoxLayout(self.groupBox_Plot)
        self.graphWidget = PlotWidget()
        layout.addWidget(self.graphWidget)
        self.init_PlotData()
        ## Connect Slots # ------------------------------------------------------
        self.connectSignalsSlots()
        ## Start Timer # --------------------------------------------------------
        self.timer_RefreshStatusBar.start(TOUT_mainWindow_RefreshStatusBar_ms)
        self.timer_RefreshWrite.start(TOUT_mainWindow_RefreshWrite_ms)
        self.timer_RefreshRead.start(TOUT_mainWindow_RefreshRead_ms)
        self.timer_PlotData.start(TOUT_mainWindow_PlotData_ms)

    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_Settings.triggered.connect(self.settingsRtBox)
        self.action_About.triggered.connect(self.about)
        self.timer_RefreshStatusBar.timeout.connect(self.refreshStatusBar)
        self.timer_RefreshWrite.timeout.connect(self.refreshWrite)
        self.timer_RefreshRead.timeout.connect(self.refreshRead)
        self.timer_PlotData.timeout.connect(self.update_PlotData)
        ## Specific Implementation
        self.pushButton_voltageEna.clicked.connect(self.pushButton_voltageEna_clicked)
        self.pushButton_wnEna.clicked.connect(self.pushButton_wnEna_clicked)
        self.pushButton_snEna.clicked.connect(self.pushButton_snEna_clicked)
        self.pushButton_unbalEna.clicked.connect(self.pushButton_unbalEna_clicked)
        self.pushButton_vDCEna.clicked.connect(self.pushButton_vDCEna_clicked)
        self.pushButton_wnDCEna.clicked.connect(self.pushButton_wnDCEna_clicked)
        self.pushButton_snDCEna.clicked.connect(self.pushButton_snDCEna_clicked)
        self.pushButton_unbalDCEna.clicked.connect(self.pushButton_unbalDCEna_clicked)
        self.pushButton_vDCLink.clicked.connect(self.pushButton_vDCLink_clicked)

    def settingsRtBox(self):
        dialog = settingsDialog(self)
        dialog.exec()

    def about(self):
        QMessageBox.about(
            self,
            "About",
            """ This project represents a simple xml-prc client for PLECS RTBox1."""
            """It consists in a PyQt5-based GUI which lets to connect to RTBox1"""
            """and send parameters and read data. The PLECS design implemented"""
            """in RTBox1 actually consists in a configurable function generator."""
            """<p>Copyright (c) 2023 lgrittin - MIT License</p>
            <p>luca.grittini@nidec-asi.com</p>"""
        )

    def refreshStatusBar(self):
        try:
            self.label_RtBoxDeviceStatusVal.setStyleSheet(dispListColor2[RTBOX_STATUS.value-1])
            self.label_RtBoxDeviceStatusVal.setText(dispList_DeviceStatus[RTBOX_STATUS.value-1])
            self.label_RtBoxConnectionVal.setStyleSheet(dispListColor[RTBOX_CONNECTED.value-1])
            self.label_RtBoxConnectionVal.setText(dispList_ConnectionStatus[RTBOX_CONNECTED.value-1])
            self.label_Ipv4Val.setStyleSheet(dispListColor[RTBOX_IPFOUND.value-1])
            self.label_Ipv4Val.setText(dispList_Ipv4[RTBOX_IPFOUND.value-1])
        except Exception:
            pass

    ## Specific Implementation

    def refreshWrite(self):
        global RTBOX_SERVER_XMLPRC
        global V_AC_Ena
        global V_AC_Ampl
        global V_AC_Freq
        global WhiteNoise_AC_Ampl
        global WhiteNoise_AC_Ena
        global SwitchingNoise_AC_Ampl
        global SwitchingNoise_AC_Freq
        global SwitchingNoise_AC_Ena
        global UnbalVoltage_AC_Ampl
        global UnbalVoltage_AC_Phase
        global UnbalVoltage_AC_Ena
        global V_DC_Ampl1
        global V_DC_Ampl2
        global V_DC_Ampl3
        global V_DC_Ena
        global V_DC_Link
        global WhiteNoise_DC_Ampl
        global WhiteNoise_DC_Ena
        global SwitchingNoise_DC_Ampl
        global SwitchingNoise_DC_Freq
        global SwitchingNoise_DC_Ena
        global UnbalVoltage_DC_Ampl
        global UnbalVoltage_DC_Phase
        global UnbalVoltage_DC_Ena

        V_AC_Ampl = self.doubleSpinBox_vAmp.value()
        V_AC_Freq = self.doubleSpinBox_vFreq.value()
        WhiteNoise_AC_Ampl = self.doubleSpinBox_wnAmp.value()
        SwitchingNoise_AC_Ampl = self.doubleSpinBox_snAmp.value()
        SwitchingNoise_AC_Freq = self.doubleSpinBox_snFreq.value()
        UnbalVoltage_AC_Ampl = self.doubleSpinBox_unbalAmp.value()
        UnbalVoltage_AC_Phase = self.spinBox_unbalPhase.value()
        V_DC_Ampl1 = self.doubleSpinBox_vDCAmp1.value()
        V_DC_Ampl2 = self.doubleSpinBox_vDCAmp2.value()
        V_DC_Ampl3 = self.doubleSpinBox_vDCAmp3.value()
        WhiteNoise_DC_Ampl = self.doubleSpinBox_wnDCAmp.value()
        SwitchingNoise_DC_Ampl = self.doubleSpinBox_snDCAmp.value()
        SwitchingNoise_DC_Freq = self.doubleSpinBox_snDCFreq.value()
        UnbalVoltage_DC_Ampl = self.doubleSpinBox_unbalDCAmp.value()
        UnbalVoltage_DC_Phase = self.spinBox_unbalDCPhase.value()

        if (V_DC_Link == 1):
            V_DC_Ampl2 = V_DC_Ampl1
            V_DC_Ampl3 = V_DC_Ampl1

        try:
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('Input', [V_AC_Ampl, V_AC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('Input1', [WhiteNoise_AC_Ampl, WhiteNoise_AC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('Input2', [SwitchingNoise_AC_Ampl, SwitchingNoise_AC_Freq, SwitchingNoise_AC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('Input3', [UnbalVoltage_AC_Ampl, UnbalVoltage_AC_Phase, UnbalVoltage_AC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('InputDC', [V_DC_Ampl1, V_DC_Ampl2, V_DC_Ampl3, V_DC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('InputDC1', [WhiteNoise_DC_Ampl, WhiteNoise_DC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('InputDC2', [SwitchingNoise_DC_Ampl, SwitchingNoise_DC_Freq, SwitchingNoise_DC_Ena])
            RTBOX_SERVER_XMLPRC.rtbox.setProgrammableValue('InputDC3', [UnbalVoltage_DC_Ampl, UnbalVoltage_DC_Phase, UnbalVoltage_DC_Ena])
        except Exception:
            pass

    def refreshRead(self):
        # Capture1 -> 500 dati
        # Capture2 -> 500 dati
        global RTBOX_SERVER_XMLPRC
        global RTBOX_CONNECTED
        global RTBOX_STATUS
        global data_Capture1
        global data_Capture2
        global Voltage_AC_R
        global Voltage_AC_S
        global Voltage_AC_T
        global Voltage_DC_R
        global Voltage_DC_S
        global Voltage_DC_T
        if ((RTBOX_STATUS == DeviceStatus.RUNNING) & (RTBOX_CONNECTED == ConnectionStatus.CONNECTED)):
            try:
                if (RTBOX_SERVER_XMLPRC.rtbox.getCaptureTriggerCount('Capture1') != 0):
                    try:
                        data_Capture1 = list(RTBOX_SERVER_XMLPRC.rtbox.getCaptureData('Capture1').values())
                        Voltage_DC_R = [idx[0] for idx in data_Capture1[0]]
                        Voltage_DC_S = [idx[1] for idx in data_Capture1[0]]
                        Voltage_DC_T = [idx[2] for idx in data_Capture1[0]]
                    except Exception:
                        pass
                if (RTBOX_SERVER_XMLPRC.rtbox.getCaptureTriggerCount('Capture2') != 0):
                    try:
                        data_Capture2 = list(RTBOX_SERVER_XMLPRC.rtbox.getCaptureData('Capture2').values())
                        Voltage_AC_R = [idx[0] for idx in data_Capture2[0]]
                        Voltage_AC_S = [idx[1] for idx in data_Capture2[0]]
                        Voltage_AC_T = [idx[2] for idx in data_Capture2[0]]
                    except Exception:
                        pass
            except Exception:
                pass
        pass

    def pushButton_voltageEna_clicked(self):
        global V_AC_Ena
        if self.pushButton_voltageEna.isChecked():
            self.pushButton_voltageEna.setText("On")
            V_AC_Ena = 1
        else:
            self.pushButton_voltageEna.setText("Off")
            V_AC_Ena = 0

    def pushButton_wnEna_clicked(self):
        global WhiteNoise_AC_Ena
        if self.pushButton_wnEna.isChecked():
            self.pushButton_wnEna.setText("On")
            WhiteNoise_AC_Ena = 1
        else:
            self.pushButton_wnEna.setText("Off")
            WhiteNoise_AC_Ena = 0

    def pushButton_snEna_clicked(self):
        global SwitchingNoise_AC_Ena
        if self.pushButton_snEna.isChecked():
            self.pushButton_snEna.setText("On")
            SwitchingNoise_AC_Ena = 1
        else:
            self.pushButton_snEna.setText("Off")
            SwitchingNoise_AC_Ena = 0

    def pushButton_unbalEna_clicked(self):
        global UnbalVoltage_AC_Ena
        if self.pushButton_unbalEna.isChecked():
            self.pushButton_unbalEna.setText("On")
            UnbalVoltage_AC_Ena = 1
        else:
            self.pushButton_unbalEna.setText("Off")
            UnbalVoltage_AC_Ena = 0

    def pushButton_vDCEna_clicked(self):
        global V_DC_Ena
        if self.pushButton_vDCEna.isChecked():
            self.pushButton_vDCEna.setText("On")
            V_DC_Ena = 1
        else:
            self.pushButton_vDCEna.setText("Off")
            V_DC_Ena = 0

    def pushButton_wnDCEna_clicked(self):
        global WhiteNoise_DC_Ena
        if self.pushButton_wnDCEna.isChecked():
            self.pushButton_wnDCEna.setText("On")
            WhiteNoise_DC_Ena = 1
        else:
            self.pushButton_wnDCEna.setText("Off")
            WhiteNoise_DC_Ena = 0

    def pushButton_snDCEna_clicked(self):
        global SwitchingNoise_DC_Ena
        if self.pushButton_snDCEna.isChecked():
            self.pushButton_snDCEna.setText("On")
            SwitchingNoise_DC_Ena = 1
        else:
            self.pushButton_snDCEna.setText("Off")
            SwitchingNoise_DC_Ena = 0

    def pushButton_unbalDCEna_clicked(self):
        global UnbalVoltage_DC_Ena
        if self.pushButton_unbalDCEna.isChecked():
            self.pushButton_unbalDCEna.setText("On")
            UnbalVoltage_DC_Ena = 1
        else:
            self.pushButton_unbalDCEna.setText("Off")
            UnbalVoltage_DC_Ena = 0

    def pushButton_vDCLink_clicked(self):
        global V_DC_Link
        if self.pushButton_vDCLink.isChecked():
            self.pushButton_vDCLink.setText("Link On")
            self.doubleSpinBox_vDCAmp2.setEnabled(0)
            self.doubleSpinBox_vDCAmp3.setEnabled(0)
            V_DC_Link = 1
        else:
            self.pushButton_vDCLink.setText("Link Off")
            self.doubleSpinBox_vDCAmp2.setEnabled(1)
            self.doubleSpinBox_vDCAmp3.setEnabled(1)
            V_DC_Link = 0
        
    def init_PlotData(self):
        # Data
        self.x = list(range(DATA_DIM))
        self.yAC1 = np.zeros(DATA_DIM, dtype=float)
        self.yAC2 = np.zeros(DATA_DIM, dtype=float)
        self.yAC3 = np.zeros(DATA_DIM, dtype=float)
        self.yDC1 = np.zeros(DATA_DIM, dtype=float)
        self.yDC2 = np.zeros(DATA_DIM, dtype=float)
        self.yDC3 = np.zeros(DATA_DIM, dtype=float)
        # Background Color
        color = self.palette().color(QtGui.QPalette.Window)  # Get the default window background
        self.graphWidget.setBackground(color)
        # Axis Style/Labels
        styles = {'color':'k', 'font-size':'10px'}
        self.graphWidget.setLabel('left', 'Voltage [V]', **styles)
        self.graphWidget.setLabel('bottom', 'Samples', **styles)
        # Legends
        self.graphWidget.addLegend()
        # Grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        self.graphWidget.setXRange(0, DATA_DIM, padding=0)
        self.graphWidget.setYRange(-6.5, 6.5, padding=0)
        # Pen Styles
        pen1 = pg.mkPen(color = 'g', width = 2, style = Qt.SolidLine)
        pen2 = pg.mkPen(color = 'r', width = 2, style = Qt.SolidLine)
        pen3 = pg.mkPen(color = 'b', width = 2, style = Qt.SolidLine)
        # Data Plot
        self.data_line_AC1 =  self.graphWidget.plot(self.x, self.yAC1, pen = pen1)
        self.data_line_AC2 =  self.graphWidget.plot(self.x, self.yAC2, pen = pen2)
        self.data_line_AC3 =  self.graphWidget.plot(self.x, self.yAC3, pen = pen3)
        self.data_line_DC1 =  self.graphWidget.plot(self.x, self.yDC1, pen = pen1)
        self.data_line_DC2 =  self.graphWidget.plot(self.x, self.yDC2, pen = pen2)
        self.data_line_DC3 =  self.graphWidget.plot(self.x, self.yDC3, pen = pen3)

    def update_PlotData(self):
        global Voltage_AC_R
        global Voltage_AC_S
        global Voltage_AC_T
        global Voltage_DC_R
        global Voltage_DC_S
        global Voltage_DC_T
        #self.x = self.x[1:]  # Remove the first y element.
        #self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        #self.y1 = self.y1[1:]  # Remove the first
        #self.y1.append(np.random.uniform(low=-10.0, high=10.0))  # Add a new random value.
        #self.y2 = self.y2[1:]  # Remove the first
        #self.y2.append(np.random.uniform(low=-10.0, high=10.0))  # Add a new random value.
        #self.y3 = self.y3[1:]  # Remove the first
        #self.y3.append(np.random.uniform(low=-10.0, high=10.0))  # Add a new random value.
        self.yAC1 = Voltage_AC_R
        self.yAC2 = Voltage_AC_S
        self.yAC3 = Voltage_AC_T
        self.yDC1 = Voltage_DC_R
        self.yDC2 = Voltage_DC_S
        self.yDC3 = Voltage_DC_T
        self.data_line_AC1.setData(self.x, self.yAC1)  # Update the data.
        self.data_line_AC2.setData(self.x, self.yAC2)  # Update the data.
        self.data_line_AC3.setData(self.x, self.yAC3)  # Update the data.
        self.data_line_DC1.setData(self.x, self.yDC1)  # Update the data.
        self.data_line_DC2.setData(self.x, self.yDC2)  # Update the data.
        self.data_line_DC3.setData(self.x, self.yDC3)  # Update the data.


# ===============================================================================
# RTBOX SETTINGS DIALOG CLASS
# ===============================================================================
class settingsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("RT-Box Settings")
        self.timer_RefreshLabels = QTimer()
        self.connectSignalsSlots()
        self.timer_RefreshLabels.start(TOUT_settingsDialog_RefreshLabels_ms)

    def connectSignalsSlots(self):
        self.pushButton_Find.clicked.connect(self.findRtBox)
        self.pushButton_Connect.clicked.connect(self.connectRtBox)
        self.pushButton_BrowseDesignFilePath.clicked.connect(self.browseDesignFile)
        self.pushButton_LoadDesign.clicked.connect(self.loadDesignFile)
        self.pushButton_Start.clicked.connect(self.startSimulation)
        self.pushButton_Stop.clicked.connect(self.stopSimulation)
        self.timer_RefreshLabels.timeout.connect(self.refreshLabels)

    def refreshLabels(self):
        global RTBOX_SERVER_XMLPRC
        global RTBOX_STATUS_INT
        global RTBOX_STATUS
        global RTBOX_CONNECTED
        global RTBOX_IPFOUND

        if (RTBOX_CONNECTED == ConnectionStatus.CONNECTED):
            try:
                RTBOX_STATUS_INT = list(RTBOX_SERVER_XMLPRC.rtbox.querySimulation().values())
                if (RTBOX_STATUS_INT[7] == 'running'):
                    RTBOX_STATUS = DeviceStatus.RUNNING
                    self.pushButton_Start.setEnabled(0)
                    self.pushButton_Stop.setEnabled(1)
                elif(RTBOX_STATUS_INT[7] == 'stopped'):
                    RTBOX_STATUS = DeviceStatus.STOPPED
                    self.pushButton_Start.setEnabled(1)
                    self.pushButton_Stop.setEnabled(0)
                elif(RTBOX_STATUS_INT[7] == 'error'):
                    RTBOX_STATUS = DeviceStatus.ERROR
                    self.pushButton_Start.setEnabled(0)
                    self.pushButton_Stop.setEnabled(0)
                else:
                    self.pushButton_Start.setEnabled(1)
                    self.pushButton_Stop.setEnabled(1)
            except Exception as error:
                QMessageBox.about(self, type(error).__name__, traceback.format_exc())
                RTBOX_STATUS = DeviceStatus.ERROR
                RTBOX_CONNECTED = ConnectionStatus.NOT_CONNECTED

        self.lineEdit_MacResult.setText(RTBOX_MACADDRESS)
        self.label_Ipv4Result.setStyleSheet(dispListColor[RTBOX_IPFOUND.value-1])
        self.label_Ipv4Result.setText(dispList_Ipv4[RTBOX_IPFOUND.value-1])
        self.label_StatusResult.setStyleSheet(dispListColor[RTBOX_CONNECTED.value-1])
        self.label_StatusResult.setText(dispList_ConnectionStatus[RTBOX_CONNECTED.value-1])
        self.label_DeviceStatusResult.setStyleSheet(dispListColor2[RTBOX_STATUS.value-1])
        self.label_DeviceStatusResult.setText(dispList_DeviceStatus[RTBOX_STATUS.value-1])
        self.label_DataCaptureBlocksResult.setText(str(len(OUTPUTBLOCKS)))
        self.label_NumProgrValueBlocksResult.setText(str(len(INPUTBLOCKS)))
        self.lineEdit_DesignFilePath.setText(DESIGN_PATH)

        if (RTBOX_IPFOUND == ConnectionStatus.NOT_CONNECTED):
            self.pushButton_Connect.setEnabled(0)
            self.pushButton_Start.setEnabled(0)
            self.pushButton_Stop.setEnabled(0)
        else:
            self.pushButton_Connect.setEnabled(1)

        if (RTBOX_CONNECTED == ConnectionStatus.NOT_CONNECTED):
            self.pushButton_LoadDesign.setEnabled(0)
            self.pushButton_Start.setEnabled(0)
            self.pushButton_Stop.setEnabled(0)
        else:
            self.pushButton_LoadDesign.setEnabled(1)

    def browseDesignFile(self):
        global DESIGN_PATH
        fname = QFileDialog.getOpenFileName(self, 'Open File', DESIGN_PATH, 'Plecs Autogenerated Code (*.elf)')
        DESIGN_PATH = fname[0]
        self.lineEdit_DesignFilePath.setText(DESIGN_PATH)

    def findRtBox(self):
        global HOST_IPV4
        global HOST_ADDRESS
        global RTBOX_IPFOUND
        global dispList_Ipv4
        try:
            HOST_IPV4 = socket.gethostbyname(HOST_NAME)
            RTBOX_IPFOUND = ConnectionStatus.CONNECTED
        except gaierror:
            HOST_IPV4 = "000.000.000.000"
            RTBOX_IPFOUND = ConnectionStatus.NOT_CONNECTED
        HOST_ADDRESS = "http://" + HOST_IPV4 + ":9998/RPC2"
        dispList_Ipv4[1] = HOST_IPV4

    def connectRtBox(self):
        global RTBOX_SERVER_XMLPRC
        global INPUTBLOCKS
        global OUTPUTBLOCKS
        global RTBOX_CONNECTED
        global RTBOX_STATUS_INT
        try:
            RTBOX_SERVER_XMLPRC = xmlrpc.client.Server(HOST_ADDRESS)
            RTBOX_CONNECTED = ConnectionStatus.CONNECTED
            self.requestInputOutputBlocks()
            self.querySimulation()
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())
            RTBOX_CONNECTED = ConnectionStatus.NOT_CONNECTED
            INPUTBLOCKS = [0]
            OUTPUTBLOCKS = [0]

    def requestInputOutputBlocks(self):
        global INPUTBLOCKS
        global OUTPUTBLOCKS
        global RTBOX_CONNECTED
        try:
            INPUTBLOCKS = RTBOX_SERVER_XMLPRC.rtbox.getProgrammableValueBlocks()
            RTBOX_CONNECTED = ConnectionStatus.CONNECTED
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())
            RTBOX_CONNECTED = ConnectionStatus.NOT_CONNECTED
            INPUTBLOCKS = [0]
        try:
            OUTPUTBLOCKS = RTBOX_SERVER_XMLPRC.rtbox.getDataCaptureBlocks()
            RTBOX_CONNECTED = ConnectionStatus.CONNECTED
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())
            RTBOX_CONNECTED = ConnectionStatus.NOT_CONNECTED
            OUTPUTBLOCKS = [0]

    def querySimulation(self):
        global RTBOX_STATUS_INT
        try:
            RTBOX_STATUS_INT = RTBOX_SERVER_XMLPRC.rtbox.querySimulation()
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())

    def loadDesignFile(self):
        global RTBOX_SERVER_XMLPRC
        global RTBOX_STATUS
        try:
            with open(DESIGN_PATH, "rb") as f:
                RTBOX_STATUS = DeviceStatus.LOADING_DESIGN
                try:
                    RTBOX_SERVER_XMLPRC.rtbox.load(xmlrpc.client.Binary(f.read()))
                    RTBOX_STATUS = DeviceStatus.DESIGN_LOADED
                except Exception as error:
                    QMessageBox.about(self, type(error).__name__, traceback.format_exc())
            f.closed
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())

    def startSimulation(self):
        global RTBOX_SERVER_XMLPRC
        try:
            RTBOX_SERVER_XMLPRC.rtbox.start()
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())
        self.requestInputOutputBlocks()

    def stopSimulation(self):
        global RTBOX_SERVER_XMLPRC
        try:
            RTBOX_SERVER_XMLPRC.rtbox.stop()
        except Exception as error:
            QMessageBox.about(self, type(error).__name__, traceback.format_exc())

# ===============================================================================
# MAIN FUNCTION
# ===============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())