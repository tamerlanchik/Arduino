# -*- coding: utf-8 -*-
import sys
import time
from math import fabs

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout, QComboBox, QAction, QInputDialog, QMessageBox, QPushButton)
from PyQt5.QtGui import QIcon, QColor
import os
import serial


K=["Колено 1:", "Колено 2:", "Поворот:", "X1", "X2"]
N="Угол:"
sliderCount=5

setPortText="Текущий порт:"
ERR_openSerial='Не удалось открыть порт.'



class Connector():
    
    def __init__(self):
        
        self.portList=['COM1', 'COM2', 'COM3', 'COM4', 'COM5']
        self.dataBase=open('dataBase.txt', 'r')
        self.currentPort=1
        self.isConnectedFlag=True
        self.temp=self.dataBase.readline().replace('\n', '')
        self.lastUpdateTime=time.time()
        
        try:
            self.currentPort=int(self.temp)
        except:
            self.currentPort=0
    
    def connect_(self, e=-1):
        if e!=-1:
            self.currentPort=self.portList.index(e)
            
        try:
            
            try: self.SERIAL.close()
            except: pass
            self.SERIAL=serial.Serial(self.portList[self.currentPort], 9600)
            self.isConnectedFlag=True
            return True
            
        except:
            
            self.isConnectedFlag=False
            return False
        
        
    def sendPosition(self, value, sender):
        #print(ord(value))
        #print("s"+str(fabs(0.1-(time.time()-self.lastUpdateTime))))
        '''try:
            if time.time()-self.lastUpdateTime>0.05:
                #print("s"+str(fabs(0.1-(time.time()-self.lastUpdateTime))))
                #time.sleep(fabs(0.1-(time.time()-self.lastUpdateTime)))
                             
        except:
            print('a')'''
        #self.SERIAL.write(bytes((str(chr(sender))+'%'+str(chr(value))+'$').encode('utf-8')))
        self.SERIAL.write(bytes((str(chr(sender))+str(chr(value))).encode('utf-8')))
        print(value)
        #self.lastUpdateTime=time.time()          
        
        
    def update_dataBase(self):     
        
        self.dataBase.close()
        self.updateData=open('dataBase.txt', 'w')
        print(self.currentPort, file=self.updateData)
        self.updateData.close()
        print('The database was updated\n')
    
    def closeSerial(self):
        self.SERIAL.close()


        
        
        
class Window(QMainWindow):
    
    def __init__(self):
        self.sliderMaxValue=180
        self.sliderPosition=[self.sliderMaxValue//2+self.sliderMaxValue*i for i in range(sliderCount)]
        super().__init__()
        self.controller=QWidget()
        self.controller.sliderBoard=[ [0]*4 for _ in range(sliderCount) ]
        self.controller.hbox=[0]*sliderCount
        
        self.initUI()       
        
        self.setCentralWidget(self.controller)        
        
        self.setGeometry(400, 400, 250, 70+30*sliderCount)
        self.setWindowTitle('Manip arduino')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()
        
        
    def initUI(self):
        
        self.controller.vbox=QVBoxLayout()
        
        self.controller.c=QComboBox(self.controller)
        self.controller.c.addItem('Не выбрано')
        self.controller.c.addItems(core.portList)
        self.controller.c.activated[str].connect(self.updatePort)
        
        self.controller.setPortLabel=QLabel(setPortText, self.controller)
        hbox01=QHBoxLayout()
        hbox01.addWidget(self.controller.setPortLabel)
        hbox01.addWidget(self.controller.c)
        
        self.j=QLabel('<font color="blue">Не подключено</font>')
        
        hbox0=QHBoxLayout()
        hbox0.addWidget(self.j)
        
        self.controller.vbox.addLayout(hbox01)
        self.controller.vbox.addLayout(hbox0)
        self.controller.vbox.addStretch(2)
        
        #----------------------------------- 
       
        # генерация области с ползунками
        # за один проход создается набор для одного ползунка 
        # и вставляется сначала в горизонтальный блок,
        # а затем - в главный вертикальный
        # \|/
        
        for i in range(sliderCount): 
            
            # создание виджетов
            
            self.controller.sliderBoard[i][0]=QLabel(K[i], self.controller)
            self.controller.sliderBoard[i][1]=QSlider(Qt.Horizontal, self.controller)
            self.controller.sliderBoard[i][2]=QLabel(N, self.controller)
            self.controller.sliderBoard[i][3]=QLabel('0', self.controller)
            
            #----------------------------------
            # первоначальная настройка виджетов
            
            self.controller.sliderBoard[i][1].setMinimum(self.sliderMaxValue*(i))
            self.controller.sliderBoard[i][1].setMaximum(self.sliderMaxValue*(i+1)-1)
            self.controller.sliderBoard[i][1].setValue(self.sliderPosition[i])
            self.controller.sliderBoard[i][1].valueChanged[int].connect(self.handleValue)
            
            #вычисление стартового значения ползунков
            val=self.controller.sliderBoard[i][1].value()-i*self.sliderMaxValue       
            self.controller.sliderBoard[i][3].setText(str(val)+'°')
            
            #-------------------------------------------
            # созданные виджеты компонуются в блоки
            # и вставляются в главный вертикальный слой.
            #-------------------------------------------
            
            self.controller.hbox[i]=QHBoxLayout()
            self.controller.hbox[i].addWidget(self.controller.sliderBoard[i][0])
            self.controller.hbox[i].addWidget(self.controller.sliderBoard[i][1])
            self.controller.hbox[i].addStretch(1)
            self.controller.hbox[i].addWidget(self.controller.sliderBoard[i][2])
            self.controller.hbox[i].addWidget(self.controller.sliderBoard[i][3])
            self.controller.hbox[i].addStretch(1)
            
            self.controller.vbox.addLayout(self.controller.hbox[i])  
            
            # ---------------окончание генерирующего цикла--------------
            
            
        #помещение блока с ползунками в Класс self.controller
        self.controller.setLayout(self.controller.vbox)
    
    def handleValue(self, value):
        sender=value//(self.sliderMaxValue)
        val=value-sender*self.sliderMaxValue
        self.sliderPosition[sender]=val
        self.controller.sliderBoard[sender][3].setText(str(val)+'°')
        core.sendPosition(val, sender)
        
        
    def updatePort(self, port):
        if port!='Не выбрано':
            flag=core.connect_(port)
            self.updateLabel(port, flag)
        else:
            core.closeSerial()
            self.updateLabel()
            
                 
        
    def updateLabel(self, port=-1, flag=False):
        if port!=-1:
        
            if (flag==True):
                    
                self.j.setText('<font color="green">Arduino успешно подключено к порту '+port+'</font>')
                               
                    
            else:
                self.j.setText('<FONT COLOR="red">Не удалось подключиться к порту '+port+'</font>')
        else:
            self.j.setText('<font color="blue">Не подключено</font>')
                  
                       

            
    def closeEvent(self, event):
        core.update_dataBase()
        core.closeSerial()
        
        

app = QApplication(sys.argv)
core=Connector()
gui = Window()
sys.exit(app.exec_())
