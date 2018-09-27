import decimal
from decimal import getcontext
from decimal import Decimal

getcontext().prec = 100
def topi(i,j=0):
    num=2
    b=1
    a=2
    x=2
    while(i>j):
        if(x%2==0):
            b=b+2
        else:
            a=a+2
        j=j+1
        x=x+1
        num=num*(a/b)
    num=num*2
    print(decimal.Decimal(num))
topi(1000)
