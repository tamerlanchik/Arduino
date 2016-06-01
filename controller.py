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

styleFile=open('style.css', 'r')
styleSheet=styleFile.read()
styleFile.close()

class Controller(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setStyleSheet(styleSheet)
        
        self.mainBox=QVBoxLayout()
        
        self.createSettingsGroup() #создать верхнее меню настроек
        self.createControlGroup()
        
        self.createDisplayAreas(Core.displaysNumber)
        
        self.displayAreasMainBox=QHBoxLayout()
        
        self.mainBox.addWidget(self.menuBoxFrame)
        self.mainBox.addStretch(1)
        self.mainBox.addWidget(self.controlGroupFrame)
        self.mainBox.addStretch(1)
        self.mainBox.addLayout(self.displayAreasBox)
        #self.mainBox.addStretch(1)
        
        self.main=QGroupBox(self)
        self.main.setLayout(self.mainBox)
        self.setLayout(self.mainBox)
        
        #self.statusBar().showMessage('opened')
        
        #self.setCentralWidget(self.main)
        '''self.setWindowTitle(T.WINDOW_TITLE)
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(400, 200, 500, 300)
        self.show()'''
    
    def createSettingsGroup(self):
        self.menuBox=QHBoxLayout(self)
                    
        self.menuBoxFrame=QGroupBox(T.SETTINGS_GROUP_HEADER, self)
        
        #------HorMenuBlock-1----------------------------------------------
        self.choosePortBox=QFormLayout(self)
        
        self.choosePortCombo=QComboBox(self)
        self.choosePortCombo.addItem(T.CONNECT_BUTTON_NOT_CONNECT)
        self.choosePortCombo.addItems(Core.portList)
        self.choosePortCombo.activated[str].connect(self.changePort)
        
        self.choosePortLabelInfo=QLabel(T.CHOOSE_PORT_LABEL_INFO, self)
        
        self.choosePortBox.addRow(T.CHOOSE_PORT_LABEL, self.choosePortCombo)
        self.choosePortBox.addRow(T.CHOOSE_PORT_LABEL_STATE, self.choosePortLabelInfo)
        #-----End - HorMenuBlock-1-----------------------------------------
        
        
        #-----HorMenuBlock-2-----------------------------------------------
        self.chooseSpeedAxisBox=QFormLayout(self)
        
        self.chooseSpeedCombo=QComboBox(self)
        self.chooseSpeedCombo.addItems(list(map(str, Core.serialSpeedCases)))
        self.chooseSpeedCombo.activated[str].connect(self.changeSpeed)
        
        self.chooseAxisNumberText=QPushButton(T.CONNECT_BUTTON_NOT_CONNECT)
        self.chooseAxisNumberText.setCheckable(1)
        self.chooseAxisNumberText.setChecked(0)
        self.chooseAxisNumberText.setObjectName('chooseAxisNumberText')
        #self.chooseAxisNumberText.setStyleSheet(self.styleSheet)
        self.chooseAxisNumberText.toggled.connect(self.disconnect)
        
        #self.chooseAxisNumberText.setFixedWidth(100)            
        
        self.chooseSpeedAxisBox.addRow(T.CHOOSE_SERIAL_SPEED, self.chooseSpeedCombo)
        self.chooseSpeedAxisBox.addRow(T.CONNECTING_STATE, self.chooseAxisNumberText)
        #-----End - HorMenuBlock-2-----------------------------------------
        
        #-----HorMenuBlock-3-----------------------------------------------
        self.setCoordRangeBox=QVBoxLayout()
        
        self.setCoordRangeBoxLeft=QHBoxLayout()
        self.setCoordRangeBoxRight=QHBoxLayout()
        
        self.setCoordRangeLabel=QLabel(T.SET_COORD_RANGE)
        
        self.setCoordRangeLabels=[0]*Core.axisNumber
        self.setCoordRangeTexts=[0]*Core.axisNumber
        
        self.setCoordRangeBoxLeft.addWidget(self.setCoordRangeLabel)
        self.W=0
        for i in range(Core.axisNumber):
            self.setCoordRangeLabels[i]=QLabel(T.COORD_NAMES[i])
            self.setCoordRangeTexts[i]=QSpinBox()
            self.setCoordRangeTexts[i].setSingleStep(5)
            self.setCoordRangeTexts[i].setRange(-300, 300)
            self.setCoordRangeTexts[i].setMaximumWidth(40)
            
            self.setCoordRangeBoxRight.addWidget(self.setCoordRangeLabels[i])
            self.setCoordRangeBoxRight.addWidget(self.setCoordRangeTexts[i])
            self.setCoordRangeBoxRight.addStretch(1)                
        
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
        #self.menuBox.addStretch(1)
        
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
            self.controlGroupLayoutJoysticks.addRow(T.COORD_NAMES[i], self.controlGroupJoysticks[i])
            
            self.slidersSignalMapper.setMapping( self.controlGroupJoysticks[i], str(i))
            
            self.controlGroupJoysticks[i].valueChanged[int].connect(self.slidersSignalMapper.map)
            
            self.controlGroupCurrentValue[i]=QLineEdit('0')
            self.controlGroupCurrentValue[i].setMaximumWidth(50)
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
            
            self.displayAreas[i]=DisplayImg(300, i)
            
            ttt.addWidget(self.displayAreas[i])
            ttt.addWidget(self.displayAreas[i].createControls())
            displayAreaBox.setLayout(ttt)
            self.displayAreasBox.addWidget(displayAreaBox)
    
    #------SLOTS---------------------
    def changePort(self, port):
        print('New port: '+port)
        
    def changeSpeed(self, newSpeed):
        print('New speed: '+newSpeed)
        
    def disconnect(self):
        state=[T.CONNECT_BUTTON_NOT_CONNECT, T.CONNECT_BUTTON_CONNECTED]
        z=int(self.chooseAxisNumberText.isChecked())
        self.chooseAxisNumberText.setText(state[z])
        
    def handleSliderValue(self, sender):
        value=self.controlGroupJoysticks[int(sender)].value()
        print(sender, str(value))
        self.controlGroupCurrentValue[int(sender)].setText(str(value))
        
    def handleValue(self, value, sender):
        try:
            sender=value//(self.sliderMaxValue)
            val=value-sender*self.sliderMaxValue-self.sliderMaxValue/2
            self.sliderPosition[sender]=val
            self.gui.sliderBoard[sender][3].setText(str(val))
            Core.updateCoords(sender, val)
            self.statusBar().showMessage(Core.sendPosition())
        except: self.statusBar().showMessage('An ERROR in "handleValue"')
        
        
    def updatePort(self, port):
        try:
            if port=='Не выбрано':
                Core.closeSerial()
                self.updateLabel()
    
            else:
                flag=Core.connect_(port)
                self.updateLabel(port, flag)
        except: self.statusBar().showMessage('An ERROR in "updatePort"')
                
                 
        
    def updateLabel(self, port=-1, flag=False):
        try:
            if port!=-1:
            
                if (flag==True):
                        
                    self.j.setText('<font color="green">Arduino успешно подключено к порту '+port+'</font>')
                                   
                        
                else:
                    self.j.setText('<FONT COLOR="red">Не удалось подключиться к порту '+port+'</font>')
            else:
                self.j.setText('<font color="blue">Не подключено</font>')
        except: self.statusBar().showMessage('An ERROR in "updateLabel"')
                       

            
    def closeEvent(self, event):
        Core.closeSerial()


    
    
'''app = QApplication(sys.argv)
core=Core()
contr=Controller()
sys.exit(app.exec_())'''