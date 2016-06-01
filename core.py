# -*- coding: utf-8 -*-
import serial
import time
class Core():
    portCount=4
    portList=['COM'+str(i) for i in range(1, portCount+1)]
    serialSpeedCases=[9600, 14400, 38400, 57600, 115200]
    axisNumber=3
    displaysNumber=2
    def __init__(self):
        #self.portCount=4
        self.portList=['COM1', 'COM2', 'COM3']
        #self.portList=['COM'+str(i) for i in range(1, self.portCount+1)]
        self.currentPort=1
        self.isConnectedFlag=True
        self.lastUpdateTime=time.time()
        self.Coords=[150]*3
        self.Angles=[0]*3
        self.R1=50
        self.R2=85
        print('ggg')

    def connect_(self, e=-1):
        try:
            if e!=-1:
                self.currentPort=self.portList.index(e)
            try:
                try: self.Serial.close()
                except: pass
                
                self.Serial=serial.Serial(self.portList[self.currentPort], 38400)
                self.isConnectedFlag=True
                return True
            except:
                self.isConnectedFlag=False
                return False
        except:
            print('Error in connect_')
    
    def sendPosition(self):
        try:
            self.calculatingAngles()
            a1, a2, a3=turple(self.Angles)
            if time.time()-self.lastUpdateTime>0.01:
                message=butes( (str(a1)+ '%' + str(a2) + '&' + str(a3) + '$').encode('utf-8'))
                self.Serial.write(message)
                self.lastUpdateTime=time.time()
            return ('Position was sent')
        except:
            print('Error in "sendPosition"')
            return('Failed send position')
    
    def calculatingAngles(self):
        try:
            try:
                x, y, z=tuple(self.Coords)
                
                try:
                    if x!=0.0:
                        self.angled[0]=math.atan( (y-L)/x )
                except:
                    print('Failed in "math.atan ((y-L)/x)"')
                
            except: print('b')
        except: print('v')
                    
                    
    def updateCoords(self, numb, coord):
        self.Coords[numb]=coord
        return 0
    
    def closeSerial(self):
        try:
            self.Serial.close()
        except: print('Error in "closeSerial"')