# -*- coding: utf-8 -*-
import serial
import time
import math
def sign(x):
    if x >= 0:
        return 1
    else:
        return -1
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
    Coords=[1,  -70,  -100]
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
            except: return("Cannot change the destination coord", self.Coords)
            #---------
            D=-1
            try:
                try:
                    print(self.Coords)
                    if self.Coords[2] <= (R1 + R2):
                        #self.Coords[1] = ( (R1 + R2) ** 2 - self.Coords[2] ** 2 ) ** 0.5
                        teta = math.atan2(self.Coords[2],  self.Coords[0])
                        #ZB = (R1 + R2) * math.sin(teta)
                    else:
                        r = 1 / 0
                except:
                    return("Cannot prepare teta",  self.Coords)
                try:
                    t=(R1**2-R2**2-x1**2-y1**2)/(-2)
                    a=x1**2+y1**2
                    b=2*t*y1
                    c=t**2-(R2**2)*(x1**2)
                    D=b**2-4*a*c
                    #print("t, a, b, c, x1, y1", t, a, b, c, x1, y1)
                except:
                    return ("Cannot prepare A, B, C",  self.Coord)
                if D<0 and a!=0:
                    #print("Does not intersect ", D)
                    return("Does not intersect ",  self.Coords)
                else:
                    if D==0:
                        Y1, Y2=b/(2*a), b/(2*a)
                    else:
                        Y1 = (b+D**0.5)/(2*a)
                        Y2 = (b-D**0.5)/(2*a)
                    if x1==0:
                        if R1 < Y1 or R1 < Y2:
                            print("Error-2",  self.Coords)
                            return("Does not intersect (2)",  self.Coords)
                        else:
                            X1 = (R1 ** 2 - Y1 ** 2) ** 0.5
                            X2 = -(R1 ** 2 - Y1 ** 2) ** 0.5
                            print("aaa",  X1,  X2)
                    else:
                        X1=(t-Y1*y1)/x1
                        X2=(t-Y2*y1)/x1 	    
                    print(self.Coords,  (X1, Y1), (X2, Y2),  a,  b,  c)
            except: 
                return(("An error during calculating coords; D ", D, X1, Y1, X2, Y2))
            try:
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
                beta=math.asin( (self.Coords[1]-Y)/R2)
                if self.Coords[0] - X < 0:
                    beta = math.pi - beta
            except:
                return("Cannot calc coords",  self.Coords)
            try:
                XA=R1*math.cos(alpha)
                YA=R1*math.sin(alpha)
                XB =  XA + R2 * math.cos(beta)
                YB =  YA + R2 * math.sin(beta)
                
                XA = round(XA,  2)
                YA = round(YA,  2)
                XB = round(XB,  2)
                YB = round(YB,  2)
                #ZB = round(ZB,  2)
                alpha = round(alpha,  2)
                beta = round(beta,  2)
                teta = round(teta,  2)
                self.Angles = [alpha,  beta,  teta]
                return((self.Coords, (XA, YA,  0), (XB,  YB,  0),  (alpha, beta, teta)))
            except:
                return("Error in send data",  self.Coords)
                
            
        except: 
            return("Error in calculatingAngles")      
                    
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
        
