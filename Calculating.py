import math as m
R1=6
R2=4
x, y=(6, 5)
x1, y1=(13-x, 11-y)
#---------
t=(R1**2-R2**2-x1**2-y1**2)/(-2)
a=x1**2+y1**2
b=2*t*y1
c=t**2-(R2**2)*(x1**2)
D=b**2-4*a*c
print("t, a, b, c", t, a, b, c)
if D<0: print("Does not intersect ", D)
else:
    if D==0:
        Y1=Y2=b/(2*a)
    else:
        Y1 = (b+D**0.5)/(2*a)
        Y2 = (b-D**0.5)/(2*a)
    
    X1=(t-Y1*y1)/x1
    X2=(t-Y2*y1)/x1
    X1+=x
    X2+=x
    Y1+=y
    Y2+=y    	    
    print((X1, Y1), (X2, Y2))
    print(a*Y1*Y1-b*Y1+c)
