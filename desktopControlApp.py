# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout, QComboBox, QAction, QInputDialog, QMessageBox, QPushButton)
from PyQt5.QtGui import QIcon, QColor
import os
import serial

K=["Колено 1:", "Колено 2:", "Поворот:"]
'''K1="Колено 1:"
K2="Колено 2:"
K3="Поворот:"'''
N="Угол:"
sliderCount=3
setPortText="Текущий порт:"
ERR_openSerial='Не удалось открыть порт.'


class Connector():
    
    def __init__(self):
        
        self.portList=['COM1', 'COM2', 'COM3', 'COM4', 'COM5']
        self.dataBase=open('dataBase.txt', 'r')
        self.currentPort=1
        self.isConnectedFlag=True
        self.temp=self.dataBase.readline().replace('\n', '')
        
        self.currentPosition=[90]*3
        
        try:
            self.currentPort=int(self.temp)
        except:
            self.currentPort=0
        self.connect_()
    
    def connect_(self):
        
        try:
            try: self.SERIAL.close()
            except: pass
            self.SERIAL=serial.Serial(self.portList[self.currentPort], 9600)
            print('Succesfully connected to '+str(self.currentPort))
            self.isConnectedFlag=True
        except:
            fallenConnect=QWidget()
            fallenConnect.bt=QPushButton('OK', fallenConnect)
            reply=QMessageBox.information(fallenConnect, 'Alert', ERR_openSerial, QMessageBox.Ok, QMessageBox.NoButton)
            self.isConnectedFlag=False
            
            
    def updatePort(self, e):
        self.currentPort=self.portList.index(e)
        print(self.currentPort)
        self.connect_()
        
    def sendPosition(self, value, sender):
        v=value
        print(sender+str(value))
        
    def update_dataBase(self):        
        self.dataBase.close()
        self.updateData=open('dataBase.txt', 'w')
        print(self.currentPort, file=self.updateData)
        self.updateData.close()
        print('The database was updated\n')

class QLabel1(QLabel):
    def setText(self, t):
        QLabel.setText(self, str(t)+'°')
        
        
        
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        controller=QWidget()
        controller.sliderBoard=[ [0]*4 for _ in range(sliderCount) ]
        controller.hbox=[0]*sliderCount
        
        self.initUI(controller)       
        
        self.setCentralWidget(controller)        
        
        self.setGeometry(400, 400, 250, 150)
        self.setWindowTitle('Manip arduino')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()
        
    def initUI(self, controller):
        
        controller.vbox=QVBoxLayout()
        
        controller.c=QComboBox(controller)
        controller.c.addItems(core.portList)
        controller.c.setCurrentIndex(core.currentPort)
        controller.c.activated[str].connect(self.updatePort)
        
        controller.setPortLabel=QLabel(setPortText, controller)
        hbox01=QHBoxLayout()
        hbox01.addWidget(controller.setPortLabel)
        hbox01.addWidget(controller.c)
        
        self.j=QLabel('<FONT COLOR="red">Не удалось подключиться к порту '+core.portList[core.currentPort]+'</FONT>')
        
        hbox0=QHBoxLayout()
        hbox0.addWidget(self.j)
        
        controller.vbox.addLayout(hbox01)
        controller.vbox.addLayout(hbox0)
        controller.vbox.addStretch(2)
        
        #----------------------------------- 
        
        '''controller.n1=QLabel(N, controller)
        controller.n2=QLabel(N, controller)
        controller.n3=QLabel(N, controller)'''
        
        for i in range(sliderCount):
            controller.sliderBoard[i][0]=QLabel(K[i], controller)
            controller.sliderBoard[i][1]=QSlider(Qt.Horizontal, controller)
            controller.sliderBoard[i][2]=QLabel(N, controller)
            controller.sliderBoard[i][3]=QLabel1('0°', controller)
            
            controller.sliderBoard[i][1].setMaximum(180)
            controller.sliderBoard[i][1].valueChanged[int].connect(self.handleValue)
            
        
        
        for i in range(sliderCount):
            controller.hbox[i]=QHBoxLayout()
            controller.hbox[i].addWidget(controller.sliderBoard[i][0])
            controller.hbox[i].addWidget(controller.sliderBoard[i][1])
            controller.hbox[i].addStretch(1)
            controller.hbox[i].addWidget(controller.sliderBoard[i][2])
            controller.hbox[i].addWidget(controller.sliderBoard[i][3])
            controller.hbox[i].addStretch(1)
            controller.vbox.addLayout(controller.hbox[i])
            
        
        '''for i in range(SLiderCount):
            controller.sld[i] = QSlider(Qt.Horizontal, controller)
            controller.sld[i].setMaximum(180)
            controller.sld[i].valueChanged[int].connect(self.handleValue)
            controller.lbl[i]=QLabel1('0°', controller)'''
            
        ''' controller.lName1=QLabel(K1, controller)
        controller.lName2=QLabel(K2, controller)
        controller.lName3=QLabel(K3, controller)'''
                
        
        
        '''sld2 = QSlider(Qt.Horizontal, controller)
        sld2.setMaximum(180)
        controller.l2=QLabel1('0°', controller)
        sld2.valueChanged[int].connect(self.handleValue)'''
        
        
        
        
        '''sld3 = QSlider(Qt.Horizontal, controller)  
        sld3.setMaximum(180)
        sld3.valueChanged[int].connect(self.handleValue) 
        controller.l3=QLabel1('0°', controller)'''
                
        '''hbox1=QHBoxLayout()
        hbox1.addWidget(controller.lName1)
        hbox1.addWidget(sld1)
        hbox1.addStretch(1)
        hbox1.addWidget(controller.n1)
        hbox1.addWidget(controller.l1)
        hbox1.addStretch(1)
        
        hbox2=QHBoxLayout()
        hbox2.addWidget(controller.lName2)
        hbox2.addWidget(sld2)
        hbox2.addStretch(1)
        hbox2.addWidget(controller.n2)
        hbox2.addWidget(controller.l2) 
        hbox2.addStretch(1)


        hbox3=QHBoxLayout()
        hbox3.addWidget(controller.lName3)
        hbox3.addWidget(sld3)
        hbox3.addStretch(1)
        hbox3.addWidget(controller.n3)
        hbox3.addWidget(controller.l3)
        hbox3.addStretch(1)
        
        vbox=QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox00)
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        vbox.addLayout(hbox3)'''
        
        controller.setLayout(controller.vbox)
        #self.updateLabel()
    
    def handleValue(self, value):
        sender=self.sender()
        print(str(sender.name()) + ' was pressed')
        #self.sender.setText(value)
        #core.sendPosition(value, self.controller.sender.text())
        print('s')
        
    def updatePort(self, value):
        core.updatePort(value)
        self.updateLabel()
        
    def updateLabel(self):
        
        if (core.isConnectedFlag==True):
                
            self.j.setText('<font color="green">Arduino успешно подключено к порту '+core.portList[core.currentPort]+'</font>')
                           
                
        else:
            self.j.setText('<FONT COLOR="red">Не удалось подключиться к порту '+core.portList[core.currentPort]+'</FONT>')
                  
                       

            
    def closeEvent(self, event):
        core.update_dataBase()
        

app = QApplication(sys.argv)
core=Connector()
gui = Window()
sys.exit(app.exec_())
