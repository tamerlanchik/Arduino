from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGroupBox, QCheckBox
from PyQt5.QtGui import QPainter, QBrush, QPen, QPalette
from dictionary import T
class DisplayImg(QWidget):
    
    def __init__(self, size, numb):
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
        
        self.doesShowWayFlag=False
        self.doesShowCirclesFlag=True
        self.doesShowLegsFlag=False
        self.K=21
        self.crossP=[0, 0]
        self.legLenghts=[0]*3
        self.Coords=[0]*3
        self.test=[0, 0]
        if self.numb==0:
            #self.coordCenter=(self.width()//2, self.height()-self.K)
            self.coordCenter=(150, 150)
        elif self.numb==1:
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
        
        self.isShowCircles=QCheckBox(T.IS_SHOW_CIRCLES_DRAW_WIDGET, self)
        self.isShowCircles.stateChanged[int].connect(self.doesDrawCircles)
        
        self.isShowLegs=QCheckBox(T.IS_SHOW_LEGS_DRAW_WIDGET, self)
        self.isShowLegs.stateChanged[int].connect(self.doesDrawLegs)
        
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
        self.painter.end()
    
    def drawTest(self, painter):
        painter.drawLine(0, 0, 100, 100)
    def drawGrid(self, painter):
        painter.setPen(Qt.gray)
        for i in range(0, self.width()+2, 10):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height()+2, 10):
            painter.drawLine(0, i, self.width(), i)
            
        painter.setPen(Qt.black)
        if self.numb==0:
            painter.drawLine(self.width()//2, 0, self.width()//2, self.height())
            
            painter.drawLine(0, self.height()-20, self.width(), self.height()-20)
        elif self.numb==1:
            painter.drawLine(self.width()-21, 0, self.width()-21, self.height())
            painter.drawLine(0, self.height()//2, self.width(), self.height()//2)
            
        if self.doesShowCirclesFlag==True:
            self.showCircles(painter)
        self.showLegs(painter)
    
    def hello(self, data):
        self.legLenghts=data[0]
        self.Coords=data[1]
        self.update()
    def showCircles(self, painter):
        painter.setPen(Qt.red)
        self.painter.translate(QPoint(*self.coordCenter))
        painter.setBrush(Qt.red)
        painter.drawEllipse(QPoint(self.Coords[0], self.Coords[1]), 2, 2) 
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPoint(self.Coords[0], self.Coords[1]), self.legLenghts[1], self.legLenghts[1])
        
        painter.setBrush(Qt.red)
        painter.drawEllipse(QPoint(0, 0), 2, 2) 
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(QPoint(0, 0), self.legLenghts[0], self.legLenghts[0]) 
        
        painter.setBrush(Qt.green)
        painter.drawEllipse(QPoint(self.crossP[0], self.crossP[1]), 2, 2)
        
        painter.setBrush(Qt.blue)
        painter.drawEllipse(QPoint(self.test[0], self.test[1]), 3, 3)         
    def showLegs(self, painter):
        painter.drawLine(0, 0, self.crossP[0], self.crossP[1])
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
    def redrawArea(self, coords, point, pointA):
        #print("Taken: ", coords, point)
        self.Coords=coords
        self.crossP=pointA
        self.test=point
        self.update()
