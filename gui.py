# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import Qt, QSignalMapper, QPoint
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication, QLabel, QHBoxLayout, QComboBox, QAction, QInputDialog, QMessageBox, QPushButton, QDesktopWidget, QLineEdit, QFormLayout, QGroupBox, QSpinBox, QGraphicsScene, QFrame, QCheckBox)
from PyQt5.QtGui import QIcon, QColor, QPainter, QBrush, QPen, QPalette
import os
from controller import Controller


sliderCount=5

setPortText="Текущий порт:"
ERR_openSerial='Не удалось открыть порт.'

class Window(QMainWindow):
    sliderMaxValue=300
    sliderPosition=0 
    def __init__(self):
        super().__init__()
        try:            
            self.controller=Controller()
            self.statusBar().showMessage('Открыто')
            self.setCentralWidget(self.controller)

    
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())
            self.setWindowTitle('Manip arduino')
            self.setWindowIcon(QIcon('icon.png'))
            self.show()
        except:
            print('Init i error')
