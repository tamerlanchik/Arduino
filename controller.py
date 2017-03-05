# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QSignalMapper, QPoint
from PyQt5.QtWidgets import (QMainWindow, QWidget,  QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout, QComboBox, QAction, QInputDialog, QMessageBox, QPushButton, QDesktopWidget, QLineEdit, QFormLayout, QGroupBox, QSpinBox)
from PyQt5.QtGui import QIcon, QColor, QPainter, QBrush, QPen, QPalette
import os
from core import Core
from display_img import DisplayImg
from dictionary import T
import time
import math

styleFile=open('style.css', 'r')
styleSheet=styleFile.read()
styleFile.close()
class Window(QMainWindow):
    sliderMaxValue=300
    sliderPosition=0 
    def __init__(self):
        super().__init__()
        try:            
            self.controller=Controller(self)
            self.statusBar().showMessage('Opened')
            self.setCentralWidget(self.controller)

    
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
            self.setWindowTitle('Manip arduino')
            self.setWindowIcon(QIcon('icon.png'))
            self.show()
        except:
            print('Init error')
    
    def showInfo(self, info_str):
        try:
            text = ''
            for i in info_str:
                text = text + str(i) + '   '
            self.statusBar().showMessage(text)
        except:
            print('Couldn\'t update the statusBar')
class Controller(QWidget):
    changeAxisRangeSpinBoxSingleStep=5
    changeAxisRangeSpinBoxMinWidth=50
    controlGroupCurrentValueMaxWidth=30
    
    
    def __init__(self,  Window):
        self.Window=Window
        self.core =Core()
        super().__init__()
        
        self.portList, self.Coords, self.currentPort, self.portCount, self.serialSpeedCases, self.axisNumber, self.displaysNumber, self.legLenght, self.isConnectedFlag, self.axisRange=Core.getData(Core)
        self.setStyleSheet(styleSheet)
        
        self.mainBox=QVBoxLayout()
        
        self.createSettingsGroup() #создать верхнее меню настроек
        self.createControlGroup()
        
        self.createDisplayAreas(self.displaysNumber)
        
        self.displayAreasMainBox=QHBoxLayout()
        
        self.mainBox.addWidget(self.menuBoxFrame)
        self.mainBox.addStretch(1)
        self.mainBox.addWidget(self.controlGroupFrame)
        self.mainBox.addStretch(1)
        self.mainBox.addLayout(self.displayAreasBox)
        
        self.setLayout(self.mainBox)
        
        data= self.core.hello()
        self.displayAreas[0].hello(data)
    def createSettingsGroup(self):
        self.menuBox=QHBoxLayout(self)
                    
        self.menuBoxFrame=QGroupBox(T.SETTINGS_GROUP_HEADER, self)
        
        #------HorMenuBlock-1----------------------------------------------
        self.choosePortBox=QFormLayout(self)
        
        self.choosePortCombo=QComboBox(self)
        self.choosePortCombo.addItem(T.CONNECT_BUTTON_NOT_CONNECT)
        self.choosePortCombo.addItems(self.portList)
        self.choosePortCombo.activated[str].connect(self.changePort)
        
        self.choosePortLabelInfo=QLabel(T.CHOOSE_PORT_LABEL_INFO, self)
        
        self.choosePortBox.addRow(T.CHOOSE_PORT_LABEL, self.choosePortCombo)
        self.choosePortBox.addRow(T.CHOOSE_PORT_LABEL_STATE, self.choosePortLabelInfo)
        #-----End - HorMenuBlock-1-----------------------------------------
        
        
        #-----HorMenuBlock-2-----------------------------------------------
        self.chooseSpeedAxisBox=QFormLayout(self)
        
        self.chooseSpeedCombo=QComboBox(self)
        self.chooseSpeedCombo.addItems(list(map(str, self.serialSpeedCases)))
        self.chooseSpeedCombo.activated[str].connect(self.changeSpeed)
        
        self.chooseAxisNumberText=QPushButton(T.CONNECT_BUTTON_NOT_CONNECT)
        self.chooseAxisNumberText.setCheckable(1)
        self.chooseAxisNumberText.setChecked(0)
        self.chooseAxisNumberText.setObjectName('chooseAxisNumberText')
        self.chooseAxisNumberText.toggled.connect(self.disconnect)
        
        self.chooseSpeedAxisBox.addRow(T.CHOOSE_SERIAL_SPEED, self.chooseSpeedCombo)
        self.chooseSpeedAxisBox.addRow(T.CONNECTING_STATE, self.chooseAxisNumberText)
        #-----End - HorMenuBlock-2-----------------------------------------
        
        #-----HorMenuBlock-3-----------------------------------------------
        self.setCoordRangeBox=QVBoxLayout()
        
        self.setCoordRangeBoxLeft=QHBoxLayout()
        self.setCoordRangeBoxRight=QHBoxLayout()
        
        self.setCoordRangeLabel=QLabel(T.SET_COORD_RANGE)
        
        self.setCoordRangeLabels=[0]*self.axisNumber
        self.setCoordRangeSpinBox=[0]*self.axisNumber
        
        self.setCoordRangeBoxLeft.addWidget(self.setCoordRangeLabel)
        
        self.spinBoxSignalMapper=QSignalMapper(self)
        
        for i in range(self.axisNumber):
            self.setCoordRangeLabels[i]=QLabel(T.COORD_NAMES[i])
            
            self.setCoordRangeSpinBox[i]=QSpinBox()
            self.setCoordRangeSpinBox[i].setSingleStep(self.changeAxisRangeSpinBoxSingleStep)
            self.setCoordRangeSpinBox[i].setRange(0, self.axisRange[i]+100) #maxLegLenght + 100mm for experiments
            self.setCoordRangeSpinBox[i].setMinimumWidth(self.changeAxisRangeSpinBoxMinWidth)
            self.setCoordRangeSpinBox[i].setValue(self.axisRange[i])
            
            self.spinBoxSignalMapper.setMapping(self.setCoordRangeSpinBox[i], str(i))
            self.setCoordRangeSpinBox[i].valueChanged[int].connect(self.spinBoxSignalMapper.map)
            
            self.setCoordRangeBoxRight.addWidget(self.setCoordRangeLabels[i])
            self.setCoordRangeBoxRight.addWidget(self.setCoordRangeSpinBox[i])
            self.setCoordRangeBoxRight.addStretch(1)                
        self.spinBoxSignalMapper.mapped[str].connect(self.handleChangerRangeValue)
        self.setCoordRangeBox.addLayout(self.setCoordRangeBoxLeft)
        self.setCoordRangeBox.addLayout(self.setCoordRangeBoxRight)
        self.setCoordRangeBox.addStretch(1)
        #-----End - HorMenuBlock-3-----------------------------------------
        
        #-----Final building Window----------------------------------------
        self.menuBox.addLayout(self.choosePortBox)
        self.menuBox.addStretch(1)
        self.menuBox.addLayout(self.chooseSpeedAxisBox)
        self.menuBox.addStretch(1)
        self.menuBox.addLayout(self.setCoordRangeBox)
        
        self.menuBoxFrame.setLayout(self.menuBox)            
    
    def createControlGroup(self):
        self.controlGroupFrame=QGroupBox(T.CONTROL_GROUP_HEADER, self)
        
        self.slidersSignalMapper=QSignalMapper(self)
        
        self.controlGroupLayout=QHBoxLayout(self)
        
        self.controlGroupLayoutJoysticks=QFormLayout()
        self.controlGroupLayoutCurrentValue=QFormLayout()
        
        self.controlGroupJoysticks=[0]*3
        self.controlGroupCurrentValue=[0]*3
        for i in range(3):
            self.controlGroupJoysticks[i]=QSlider(Qt.Horizontal)
            self.controlGroupJoysticks[i].setMinimumWidth(self.size().width()+200)
            self.controlGroupJoysticks[i].setRange(self.axisRange[i]*(-1), self.axisRange[i])
            self.controlGroupJoysticks[i].setValue(self.Coords[i])
            
            self.controlGroupLayoutJoysticks.addRow(T.COORD_NAMES[i], self.controlGroupJoysticks[i])
            
            self.slidersSignalMapper.setMapping( self.controlGroupJoysticks[i], str(i) )
            
            self.controlGroupJoysticks[i].valueChanged[int].connect(self.slidersSignalMapper.map)
            
            self.controlGroupCurrentValue[i]=QLineEdit(str(self.controlGroupJoysticks[i].value()))
            self.controlGroupCurrentValue[i].setMaximumWidth(self.controlGroupCurrentValueMaxWidth)
            self.controlGroupLayoutCurrentValue.addRow(T.CURRENT_POSITION_LABEL, self.controlGroupCurrentValue[i])
        
        self.slidersSignalMapper.mapped[str].connect(self.handleSliderValue)
        self.controlGroupLayout.addLayout(self.controlGroupLayoutJoysticks)
        self.controlGroupLayout.addStretch(1)
        self.controlGroupLayout.addLayout(self.controlGroupLayoutCurrentValue)
        
        self.controlGroupFrame.setLayout(self.controlGroupLayout)
    
    def createDisplayAreas(self, numb):
        self.displayAreas=[0]*numb
        self.displayAreasBox=QHBoxLayout()
        for i in range(numb):
            displayAreaBox=QGroupBox(T.DISPLAY_AREA_HEADER[i])
            ttt=QHBoxLayout()
            
            self.displayAreas[i]=DisplayImg(300, i,  self.Coords,  self.legLenght)
            
            ttt.addWidget(self.displayAreas[i])
            ttt.addWidget(self.displayAreas[i].createControls())
            displayAreaBox.setLayout(ttt)
            self.displayAreasBox.addWidget(displayAreaBox)
    
    #------SLOTS---------------------
    def changePort(self, port):
        self.Window.showInfo("Port changed")
        if port==T.CONNECT_BUTTON_NOT_CONNECT:
            event=False
            self.updateLabel(flag=self.isConnectedFlag)
        else:
            event=True
            self.isConnectedFlag=Core.connect_(Core, self.portList.index(port))
            self.updateLabel(port, self.isConnectedFlag)
        
    def changeSpeed(self, newSpeed):
        if __name__!='__main__':
            self.Window.showInfo('Connectinh speed changed. Reconnecting...')
        Core.connect_(Core)
        
    def disconnect(self):
        state=[T.CONNECT_BUTTON_NOT_CONNECT, T.CONNECT_BUTTON_CONNECTED]
        currState=int(self.chooseAxisNumberText.isChecked())
        ans=Core.changePortState(Core, currState)
               
        self.chooseAxisNumberText.setText(state[int(ans)])
        
        self.chooseAxisNumberText.setChecked(ans)
            
        self.updateLabel(flag=self.isConnectedFlag)
        
        if __name__!='__main__':
            self.Window.showInfo(state[int(ans)])
        
    def handleChangerRangeValue(self, sender):
        sender=int(sender)
        value=self.setCoordRangeSpinBox[sender].value()
        self.axisRange[sender]=value
        self.controlGroupJoysticks[sender].setRange(value*(-1), value)
        if __name__!='__main__':
            self.Window.showInfo('Range on '+str(T.COORD_NAMES[sender])+' changed')
        
    def handleSliderValue(self, sender):
        sender=int(sender)
        value=self.controlGroupJoysticks[sender].value()
        self.controlGroupCurrentValue[sender].setText(str(value))
        
        data = self.core.calculatingAngles(sender, value)
        self.Window.showInfo(data)
        if type(data[0]) != str:
            Coords,  cA, cB, angles = data
            self.displayAreas[0].redrawArea(cA,  cB)
            self.displayAreas[1].redrawArea(cA,  cB)
        else:
            #self.Window.showInfo(("Error",  data[1],  'a'))
            self.displayAreas[0].redrawArea(cB = data[1],  err = True)
            self.displayAreas[1].redrawArea(cB = data[1],  err = True)
        
        
    def updateLabel(self, port=-1, flag=False):
        try:
            if port!=-1:
            
                if (flag==True):
                        
                    self.choosePortLabelInfo.setText('<font color="green">'+T.SUCCESFULLY_CONNECTED_TO_THE_PORT+' <b>'+port+'</b></font>')
                                   
                        
                else:
                    self.choosePortLabelInfo.setText('<FONT COLOR="red">'+T.CANT_CONNECT_TO_THIS_PORT+' <b>'+port+'</b></font>')
            else:
                self.choosePortLabelInfo.setText(T.CHOOSE_PORT_LABEL_INFO)
        except: pass
                       

            
    def closeEvent(self, event):
        try:
            Core.closeSerial()
        except:
            self.Window.showInfo("Cannot close the Serial")
    





if __name__=='__main__':
    app = QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())
