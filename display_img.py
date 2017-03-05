from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QCheckBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QPalette
from dictionary import T
class DisplayImg(QWidget):
    
    def __init__(self, size, numb,  Dest,  Rs):
        super().__init__()
        
        #-----РЎР»СѓР¶РµР±РЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ---------
        #self.legLenght=legLenght
        #----------------------------------
        self.size=size
        self.setFixedHeight(size+1)
        self.setFixedWidth(size+1)
        Pal=QPalette()
        Pal.setColor(QPalette.Background, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(Pal)
        self.numb=numb
        self.err = False
        
        self.doesShowWayFlag=False
        self.doesShowCirclesFlag=True
        self.doesShowLegsFlag=False
        self.K=21
        self.crossP=[0, 0,  0]
        self.legLenghts= Rs
        self.Dest=Dest
        if self.numb==0:
            self.Mask = (1,  1,  0)
            self.coordCenter=(self.width()//2, self.height()-self.K)
            #self.coordCenter=(150, 150)
        elif self.numb==1:
            self.Mask = (1,  0,  1)
            #self.coordCenter=(self.width()-self.K, self.height()//2)
            self.coordCenter=(100, 230)
        try:  
            self.painter=QPainter(self)           
        except:
            print('Cant init display '+str(self.numb))

    
    def createControls(self):
        self.mainBox=QVBoxLayout(self)
        self.mainGroupBox=QGroupBox(self)
        
        self.doesShowWayCheck=QCheckBox(T.IS_SHOW_WAY_DRAW_WIDGET, self)
        self.doesShowWayCheck.stateChanged[int].connect(self.doesDrawWays)
        self.doesShowWayCheck.setCheckState(self.doesShowWayFlag)
        
        self.isShowCircles=QCheckBox(T.IS_SHOW_CIRCLES_DRAW_WIDGET, self)
        self.isShowCircles.stateChanged[int].connect(self.doesDrawCircles)
        self.isShowCircles.setCheckState(self.doesShowCirclesFlag)
        
        self.isShowLegs=QCheckBox(T.IS_SHOW_LEGS_DRAW_WIDGET, self)
        self.isShowLegs.stateChanged[int].connect(self.doesDrawLegs)
        self.isShowLegs.setCheckState(self.doesShowLegsFlag)
        
        self.clearButton=QPushButton(T.IS_CLEAR_BUTTON_DRAW_WIDGET, self)
        self.clearButton.clicked.connect(self.clearDisplay)
        
        self.mainBox.addWidget(self.doesShowWayCheck)
        self.mainBox.addWidget(self.isShowCircles)
        self.mainBox.addWidget(self.isShowLegs)
        self.mainBox.addWidget(self.clearButton)
        self.mainBox.addStretch(1)
        
        self.mainGroupBox.setLayout(self.mainBox)
        return self.mainGroupBox
        
    def paintEvent(self, e):
        self.painter.begin(self)
        #self.painter.translate(QPoint(*self.coordCenter)) 
        self.drawGrid(self.painter)
        self.showCircles(self.painter)
        self.showLegs(self.painter)
        self.painter.end()
    
    def drawGrid(self, painter):
        painter.setPen(Qt.gray)
        for i in range(0, self.width()+2, 10):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height()+2, 10):
            painter.drawLine(0, i, self.width(), i)
            
        painter.setPen(Qt.black)

        painter.drawLine(self.coordCenter[0], 0, self.coordCenter[0], self.height())
        painter.drawLine(0, self.coordCenter[1], self.width(), self.coordCenter[1])
    
    def hello(self, data):
        self.legLenghts=data[0]
        self.Dest=data[1]
        self.update()
    def showCircles(self, painter):
        if self.doesShowCirclesFlag == True:
            self.painter.translate(QPoint(*self.coordCenter))
            
            painter.setBrush(Qt.red)
            painter.setPen(Qt.red)
            painter.drawEllipse(QPoint(self.Dest[0], self.Dest[self.numb+1]), 2, 2)
            painter.drawEllipse(QPoint(0, 0), 2, 2)
            
            if self.err == False:
                painter.setPen(Qt.red)
            else:
                painter.setPen(Qt.blue) 
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPoint(0, 0), self.legLenghts[0], self.legLenghts[0])
            
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPoint(self.Dest[0], self.Dest[self.numb+1]), self.legLenghts[1], self.legLenghts[1])            
            
                
    def showLegs(self, painter):
        if self.doesShowLegsFlag == True:
            if self.numb == 0:
                painter.drawLine(0, 0, self.crossP[0], self.crossP[self.numb+1])
                painter.drawLine(self.crossP[0],  self.crossP[self.numb+1],  self.Dest[0],  self.Dest[self.numb+1])
            else:
                painter.drawLine(0,  0,  self.Dest[0],  self.Dest[2])
    #----SLOTS----------------------
    def doesDrawCircles(self, flag):
        self.doesShowCirclesFlag=bool(flag)
        self.update()
    def doesDrawWays(self, flag):
        self.doesShowWayFlag=bool(flag)
        self.update()
    def doesDrawLegs(self, flag):
        self.doesShowLegsFlag=bool(flag)
        self.update()
    def clearDisplay(self):
        self.doesShowWayFlag=False
        self.update()
    def redrawArea(self, cA = 'a',  cB = 'a',  err = False):
        if cA != 'a':
            self.crossP=cA
        if cB != 'a':
            self.Dest=cB
        self.err = err
        self.update()
