import math
import decimal
from decimal import Decimal
from decimal import getcontext

getcontext().prec = 1800
def to_e(i=100):
    j=l=0
    while(i>j):
        k=Decimal(1/(math.factorial( j )))
        l=Decimal(l)+Decimal(k)
        j=j+1
    d = decimal.Decimal(l)
    print(d)

to_e(5000)
