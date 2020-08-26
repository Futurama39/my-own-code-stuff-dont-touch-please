import re
import itertools
import csv
import os

with open(r'D:\Spews of creativity\pyshit\my-own-code-stuff-dont-touch-please\Python\resulttable.txt') as f:
    lines = f.readlines()
'''
pretreatment of results list, from the copied version from wikipedia
returns a list of drivers in this format:
[champ. position, name with nationality, finish in points, ... , total points in season]
first line is race locations
'''
for i in range(len(lines)):
    lines[i] = re.sub(' ','',lines[i])
    lines[i] = lines[i].split('\t')
    for j in range(2,len(lines[i])-1):
        if lines[i][j] == '1':
            lines[i][j] = 25
        elif lines[i][j] == '2':
            lines[i][j] = 18
        elif lines[i][j] == '3':
            lines[i][j] = 15
        elif lines[i][j] == '4':
            lines[i][j] = 12
        elif lines[i][j] == '5':
            lines[i][j] = 10
        elif lines[i][j] == '6':
            lines[i][j] = 8
        elif lines[i][j] == '7':
            lines[i][j] = 6
        elif lines[i][j] == '8':
            lines[i][j] = 4
        elif lines[i][j] == '9':
            lines[i][j] = 2
        elif lines[i][j] == '10':
            lines[i][j] = 1
        else:
            lines[i][j] = 0
races = len(lines[0])-3
lst = list(range(races))

class Driver:
    def __init__(self,i):
        self.num = int(lines[i][0])
        self.name = lines[i][1]
        self.results = lines[i]
        self.results = self.results[:-1]
        self.results = self.results[2:]
        self.points = 0
        self.wins = 0
        self.season_results = [] #because tiebreaks
        self.winlst = []
        for i in lst:
            self.winlst.append(0)

drivers = []

for i in range(len(lines)):
    drivers.append(Driver(i))

combinations_list = []
for i in lst: #each i is cycle length
    comb = list(itertools.combinations(lst,i+1))
    for j in comb:
        combinations_list.append(j)

def compute(season,mode=0):
    for i in drivers:
        i.points = 0
        i.season_results = []

    for race in season:
        for driver in drivers:
            driver.points += driver.results[race]
            driver.season_results.append(driver.results[race])
    
    for driver in drivers:
        driver.season_results.sort(reverse=True)


    maximum = drivers[-1]
    for driver in drivers: #establish the season winner
        if driver.points == 0 or driver.points < maximum.points:
            continue
        if driver.points > maximum.points:
            maximum = driver
            continue
        elif driver.points == maximum.points: #in case of ties we neeed to compare results
            max_points = maximum.season_results
            driver_points = driver.season_results
            for i in range(len(season)):
                if max_points[i] != driver_points[i]:
                    if max_points < driver_points:
                        driver = maximum
                    continue
        maximum = None #tie is made, no winner established
        break 
    if maximum != None:            
        drivers[maximum.num-1].wins += 1
        drivers[maximum.num-1].winlst[len(season)-1] += 1
    else:
        return None
    if mode == 1:
        outtable = [maximum.num]
        outtable.append(season)
        for driver in drivers:
            season_score = 0
            for i in driver.season_results:
                season_score += i
            outtable.append(season_score)
        return outtable

def allresults(index=0):        
    for i in combinations_list:
        compute(i)
        index += 1
        if index % 1000 == 0:
            print('race #',index,' eval\'d')


    fintable = []
    for driver in drivers:
        preptable = [driver.name,driver.wins]
        for num in driver.winlst:
            preptable.append(num)
        fintable.append(preptable)

    out(fintable)

def driverresults(driverobj):
    outtable = []
    index = 0
    for i in combinations_list:
        season = compute(i,1)
        index+=1
        if index % 1000 == 0:
            print('race #',index,' eval\'d')
        if (season != None) and (season[0] == driverobj.num):
            del season[0]
            outtable.append(season)
    out(outtable)

def out(table,i=0):
    path = 'D:\\Spews of creativity\\pyshit\\my-own-code-stuff-dont-touch-please\\Python\\'
    while True:
        if os.path.isfile(path+'out'+str(i)+'.csv'):
            i+=1
        else:
            break
    with open('out'+str(i)+'.csv','w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)

allresults()