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
    legLenght=[50, 50, 30]
    currentSpeed=2
    Coords=[-100]*3
    preCoords=[150]*3
    preAngles=[0]*3
    Angles=[0]*3
    axisRange=[max(legLenght)*axisNumber]*axisNumber
    
    def __init__(self):
        self.lastUpdateTime=time.time()
        
    def hello(self):
        return(self.legLenght, self.Coords)
    def getData(self):
        ans=(self.portList, self.Coords, self.currentPort, self.portCount, self.serialSpeedCases, self.axisNumber, self.displaysNumber, self.legLenght, self.isConnectedFlag, self.axisRange)
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
                x1, y1=self.Coords[0], self.Coords[1]
                R1=self.legLenght[0]
                R2=self.legLenght[1]
            except: print("Cannot change the destination coord")
            #---------
            D=-1
            print("Start calculating")
            try:
                try:
                    t=(R1**2-R2**2-x1**2-y1**2)/(-2)
                    a=x1**2+y1**2
                    b=2*t*y1
                    c=t**2-(R2**2)*(x1**2)
                    D=b**2-4*a*c
                    print("t, a, b, c, x1, y1", t, a, b, c, x1, y1)
                except:
                    print("Cannot prepare A, B, C")
                if D<0 and a!=0:
                    print("Does not intersect ", D)
                    return(self.Coords, (0, 0), (0, 0), (0, 0))
                else:
                    if D==0:
                        Y1, Y2=b/(2*a), b/(2*a)
                        print("D=0")
                    else:
                        Y1 = (b+D**0.5)/(2*a)
                        Y2 = (b-D**0.5)/(2*a)
                    if x1==0:
                        X1=x1
                        X2=x1
                    else:
                        X1=(t-Y1*y1)/x1
                        X2=(t-Y2*y1)/x1 	    
                    print((X1, Y1), (X2, Y2))
            except: 
                print("An error during calculating coords; D ", D, X1, Y1, X2, Y2)
            try:
                '''if abs(self.preCoords[0]-X1)<abs(self.preCoords[0]-X2):
                    self.preCoords=[X1, Y1, 0]
                    X, Y=X1, Y1
                    #return((X1, Y1))
                else:
                    self.preCoords=[X2, Y2, 0]
                    X, Y=X2, Y2
                    #return((X2, Y2))'''
                a1=math.asin(Y1/R1)
                a2=math.asin(Y2/R1)
                if X1<0:
                    a1=math.pi-a1
                if X2<0:
                    a2=math.pi-a2
                if abs(self.preAngles[0]-a1)<abs(self.preAngles[0]-a2):
                    alpha=a1
                    X=X1
                    Y=Y1
                else:
                    alpha=a2
                    X=X2
                    Y=Y2
                self.preAngles[0]=alpha
            except:
                print("Cannot send coords")
            try:
                '''alpha=math.asin(Y/R1)
                if X<0:
                    alpha=math.pi-alpha'''
                beta=math.atan( (self.Coords[1]-Y)/R2)
                XA=R1*math.cos(alpha)
                YA=R1*math.sin(alpha)
                return(self.Coords, (X, Y), (XA, YA), (alpha, beta))
            except:
                print("Error in send data")
                return(self.Coords, (0, 0), (0, 0), (0, 0))
                
            
        except: 
            print("Error in calculatingAngles")
            return(self.Coords, (0, 0), (0, 0), (0, 0))
        '''try:
            self.Coords[sender]=value
            return self.Coords
        except: print("Cannot change the destination coord")'''        
                    
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
        
