from decimal import getcontext
from decimal import Decimal
getcontext().prec = 81
print(Decimal(1) / Decimal(7))
