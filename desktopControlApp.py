# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout, QComboBox, QAction, QInputDialog)
from PyQt5.QtGui import QIcon


K1="Колено 1:"
K2="Колено 2:"
K3="Поворот:"
N="Угол:"
setPortText="Текущий порт:"

class QLabel1(QLabel):
    def setText(self, t):
        QLabel.setText(self, str(t)+'°')
        
class Window(QMainWindow):
    

    def __init__(self):
        super().__init__()
        self.port='COM1'
        
        controller=QWidget()
        
        self.initUI(controller)
        
        
        self.setCentralWidget(controller)
        
        
        self.setGeometry(400, 400, 250, 150)
        self.setWindowTitle('Manip arduino')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()        
    
    
        
    def writePort(self, porto):
        self.port=porto
        print(self.port)
        
    def makeToolBar(self, setPort):
        
       
        
        
        '''setPort=QWidget()
        combo=QComboBox(setPort)
        combo.addItems(["1", "2", "3", "4", "5"])
        l=QLabel("Номер порта: COM", setPort)
        b=QPushButton("OK", setPort)
        b.clicked.connect(setPert.close)
        setPort.h=QHBoxLayout()
        setPort.h.addWidget(l)
        setPort.h.addWidget(combo)
        setPort.h.addWidget(b)
        
        setPort.addLayout(setPort.h)
        
        setPort.show()'''
        
    def initUI(self, controller):
        
        controller.c=QComboBox(controller)
        controller.c.addItems(["COM1", "COM2", "COM3", "COM4", "COM5"])
        controller.c.activated[str].connect(self.writePort)
        controller.setPortLabel=QLabel(setPortText, controller)
        hbox0=QHBoxLayout()
        hbox0.addWidget(controller.setPortLabel)
        hbox0.addWidget(controller.c)
                
        controller.n1=QLabel(N, controller)
        controller.n2=QLabel(N, controller)
        controller.n3=QLabel(N, controller)
        sld1 = QSlider(Qt.Horizontal, controller)
        sld1.setMaximum(180)
        controller.lName1=QLabel(K1, controller)
        controller.l1=QLabel1('0'+'°', controller)        
        sld1.valueChanged[int].connect(controller.l1.setText)
        
        
        sld2 = QSlider(Qt.Horizontal, controller)
        sld2.setMaximum(180)
        controller.l2=QLabel1('0'+'°', controller)
        controller.lName2=QLabel(K2, controller)
        sld2.valueChanged[int].connect(controller.l2.setText)
        
        controller.l3=QLabel1('0'+'°', controller)
        controller.lName3=QLabel(K3, controller)
        sld3 = QSlider(Qt.Horizontal, controller)  
        sld3.setMaximum(180)
        sld3.valueChanged[int].connect(controller.l3.setText) 
        
        hbox1=QHBoxLayout()
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
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        vbox.addLayout(hbox3)
        
        controller.setLayout(vbox)
        
        controller.setGeometry(0, 0, 1000, 1500)
        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    a=input()
