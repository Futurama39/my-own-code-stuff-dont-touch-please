import math
def quad(a=0,b=0,c=0,d=0):
    if(d!=0):
        d=(b*b)-4*a*c
    if (d<0):
        print("0 Answers")
    elif(d==0):
        print(b/2*a)
    else:
        print(b+math.sqrt( d )/2*a,end='')
        print(b-math.sqrt( d )/2*a)
quad(1,4,4)