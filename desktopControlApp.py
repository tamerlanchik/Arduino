# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout)
from PyQt5.QtGui import QIcon


K1="Колено 1:"
K2="Колено 2:"
K3="Поворот:"
N="Угол:"
rryyry

class QLabel1(QLabel):
    def setText(self, t):
        QLabel.setText(self, str(t)+'°')
        
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        self.n1=QLabel(N, self)
        self.n2=QLabel(N, self)
        self.n3=QLabel(N, self)
        sld1 = QSlider(Qt.Horizontal, self)
        sld1.setMaximum(180)
        self.lName1=QLabel(K1, self)
        self.l1=QLabel1('0'+'°', self)        
        sld1.valueChanged[int].connect(self.l1.setText)
        
        
        sld2 = QSlider(Qt.Horizontal, self)
        sld2.setMaximum(180)
        self.l2=QLabel1('0'+'°', self)
        self.lName2=QLabel(K2, self)
        sld2.valueChanged[int].connect(self.l2.setText)
        
        self.l3=QLabel1('0'+'°', self)
        self.lName3=QLabel(K3, self)
        sld3 = QSlider(Qt.Horizontal, self)  
        sld3.setMaximum(180)
        sld3.valueChanged[int].connect(self.l3.setText) 
        
        hbox1=QHBoxLayout()
        hbox1.addWidget(self.lName1)
        hbox1.addWidget(sld1)
        hbox1.addStretch(1)
        hbox1.addWidget(self.n1)
        hbox1.addWidget(self.l1)
        hbox1.addStretch(1)
        
        hbox2=QHBoxLayout()
        hbox2.addWidget(self.lName2)
        hbox2.addWidget(sld2)
        hbox2.addStretch(1)
        hbox2.addWidget(self.n2)
        hbox2.addWidget(self.l2) 
        hbox2.addStretch(1)


        hbox3=QHBoxLayout()
        hbox3.addWidget(self.lName3)
        hbox3.addWidget(sld3)
        hbox3.addStretch(1)
        hbox3.addWidget(self.n3)
        hbox3.addWidget(self.l3)
        hbox3.addStretch(1)
        
        vbox=QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        
        vbox.addLayout(hbox3)
        
        self.setLayout(vbox)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Manip arduino')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    a=input()
