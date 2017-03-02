import math as m

r=4
R=6
x, y=(6, 5)
x2, y2=(13, 11)

x1, y1=(0, 0)
x2, y2=(x2-x, y2-y)
L2=(x2-x1)**2+(y2-y1)**2

X=(r*r+R*R-L2)/(2*r*R)
t=m.atan( (y2-y1)/(x2-x1) )
if t<0: t=(m.pi+t)*(-1)
h=(r*R*m.sin(m.acos(X)))/(L2**0.5)
bet= abs(t+ m.asin(h/(L2**0.5)))
gamm= bet -m.pi+m.acos(X)
Ax=x1-r*m.cos(bet)+x
Ay=y1+r*m.sin(bet)+y
print("bet: ", m.degrees(bet), " gamm: ", m.degrees(gamm), " L²: ", L2, " X: ", X, " T: ", m.degrees(t), " Ang X: ", m.degrees(m.acos(X)))
print(Ax, Ay)
