
#using the international atomic time this is not compliant with UTC standards

days_in_months = [31,28,31,30,31,30,31,31,30,31,30,31]


def nullpoint(date):
    date.month += date.year*12
    date.day += months_to_days(date.month)
    date.hour += date.day*24
    date.minute += date.hour*60
    date.second += date.minute*60
    return date.second

def months_to_days(months,start_year=0,start_month=0):
    leap = False
    out = 0
    if start_year % 4 == 0 and start_year % 400 != 0:
        leap = True
    for x in range(start_month,months+start_month):
        if x % 12 == 1 and leap:
            out+=29
            leap = False
        else:
            out+=days_in_months[(x%12)-1]
        if x % 12 == 0:
            start_year+=1
            if start_year % 4 == 0 and start_year % 400 != 0:
                leap = True
    return out

class TimeObject:
    def __init__(self,year,month=1,day=1,hour=0,minute=0,second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

class DiffObject:
    def __init__(self,year=0,month=0,day=0,hour=0,minute=0,second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
    
a = TimeObject(2001,11,25,13,15)
b = nullpoint(a)
print(b)
