# -*- coding: utf-8 -*-
import serial
import time
import math
class Core():
    portCount=4
    portList=['COM'+str(i) for i in range(1, portCount+1)]
    serialSpeedCases=[9600, 14400, 38400, 57600, 115200]
    axisNumber=3
    currentPort=1
    displaysNumber=2
    isConnectedFlag=True
    legLenght=[50, 80, 30]
    currentSpeed=2
    Coords=[150]*3
    Angles=[0]*3
    R1=50
    R2=85
    axisRange=[max(legLenght)*axisNumber]*axisNumber
    
    def __init__(self):
        self.lastUpdateTime=time.time()
        
    def getData(self):
        ans=(self.portList, self.currentPort, self.portCount, self.serialSpeedCases, self.axisNumber, self.displaysNumber, self.legLenght, self.isConnectedFlag, self.axisRange)
        return ans
    
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
            return False
    
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
    
    def calculatingAngles(self, sender, value):
        try:
            try:
                self.Coords[sender]=value
            except: print('Err in update coords')
            try:
                x=self.Coords[0]
                y=self.Coords[1]
                z=self.Coords[2]
            except:
                print('Error in xyz')
                
            try:
                if x!=0:
                    self.Angles[0]=math.pi//2+math.atan(y/x)
                else:
                    self.Angles[0]=math.pi/2
            except: print("Failed in math.atan((y-L)/x)", y, x, self.Angles)
            
            try:
                try:
                    self.R1*=math.cos(self.Angles[0])
                    self.R2*=math.cos(self.Angles[0])
                except: print("2"); print(str(self.R1), str(self.R2), str(self.Angles[0]))
                
                try:
                    self.Angles[0]=math.degrees(self.Angles[0])
                except: print("4")
                
                try:
                    e=(self.R2**2 - self.R1**2 - z**2 - y**2) / (-2)
                except: print("3")
                
            except: print("1")
            
            try:
                a=y**2 + z**2
                b=(-2)*e*y
                c=e**2 - (self.R1**2)*(z**2)
        
                D=b**2-4*a*c
            except: print('Error in calculating coeffs')
            
            try:
                if D<0: 
                    print('Не пересекаются')
                    return [0]*self.axisNumber
                
                elif D==0:
                    Y=(-b)/(2*a)
                    
                elif D>0:
                    Y1=(-b + D**0.5) / (2*a)
                    Y2=(-b - D**0.5) / (2*a)
                    
                    Y=max(Y1, Y2)
                
                else:
                    print('Error')
                    return [0]*self.axisNumber
                    
                Z = (e - Y*y) / z
                
                l2 = z**2 + y**2
                self.Angles[0]=int(self.Angles[0])
                alpha = math.atan2(Y, Z)
                self.Angles[1] = int(math.pi+math.degrees( alpha ))
                
                
                beta=(self.R1**2 +self.R2**2 -l2)/(2*self.R1*self.R2)
                beta = math.acos( beta )
                self.Angles[2] = int(math.degrees(beta))
                return self.Angles
            except: print("b")
        except: 
            print("Error in calculatingAngles")
            return [0]*self.axisNumber
                    
                    
    def updateCoords(self, numb, coord):
        self.Coords[numb]=coord
        return 0
    
    def changePortState(self, newState):
        try:
            if newState==True:
                try:
                    self.Serial=serial.Serial(self.portList[self.currentPort], self.serialSpeedCases[self.currentSpeed])
                    self.isConnectedFlag=True
                    return True
                except:
                    self.isConnectedFlag=False
                    return False
            else:
                try:
                    self.closeSerial()
                    self.isConnectedFlag=False
                except:
                    pass
                return False
        except: print('rrr')
    
    def closeSerial(self):
        try:
            self.Serial.close()
        except: print('Error in "closeSerial"')
        
