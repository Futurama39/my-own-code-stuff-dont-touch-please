import re
import itertools
import csv
import os
import math

def driversort(lst):
    '''
    insertion sorting, easier to implement and O(n^2) doesn't bother me that much as driver count is like >60 at most
    \nexpects a driver object list with seasonpoints and seasonpositions already sorted
    '''
    iterable = iter(lst)                                                    #init a list of just first element and move the iterable to start from 2nd element
    sorted_list = [lst[0]]
    next(iterable)
    for driver in iterable:                                                 #element to be inserted
        inserted = False #break the loop if any was inserted                                                  
        i=0                                                                 # keep track of element position
        for element in sorted_list:
            if inserted:
                break                                         #comparison for every list item, we break on the right insertion space
            if driver.seasonpoints > element.seasonpoints:
                if not inserted:                      #no tie, insert found
                    sorted_list.insert(i,driver)
                    inserted = True
                continue                                                           #driver inserted, go on to the next one
            elif driver.seasonpoints == element.seasonpoints:                   #driver points equal, need a tie break
                if driver.seasonpositions == element.seasonpositions:               #tie can't be broken
                    driver.tied = True
                    if not inserted:
                        sorted_list.insert(i,driver)
                        inserted = True
                    continue
                else:
                    for j, placement in enumerate(driver.seasonpositions):
                        if placement == element.seasonpositions[j]:                 #places are same on this one
                            continue
                        elif placement < element.seasonpositions[j]:
                            if not inserted:                #tie won
                                sorted_list.insert(i,driver)
                                inserted = True
                                break
                        else:                                                       #tie lost
                            i+=1
                            if i == len(sorted_list) and not inserted:                      #we're on the end of the list so append to the end
                                sorted_list.append(driver)
                                inserted = True
                            break
            else:                                                               #tie lost
                i+=1
                if i == len(sorted_list) and not inserted:                      #we're on the end of the list so append to the end
                    sorted_list.append(driver)
                    inserted = True
    for i,driver in enumerate(sorted_list):                                 #make positions
        if not driver.tied:                                                     #driver is not tied so positions equal
            driver.position = i+1
            continue
        else:
            if i != 0:                                                          #only ran when list not first in list
                if sorted_list[i-1].tied and driver.seasonpositions == sorted_list[i-1].seasonpositions:   #member above in list part of tie, and is of the same tie
                    driver.position = sorted_list[i-1].position   #is a part of the same tie so had to have position of this tie member since they are earlier in the list they are determined already
                else:
                    driver.position = i+1
            else:                                                               #driver is tied with someone below them so will recieve their current position as the "leader" of the tie
                driver.position = i+1
    return sorted_list   

'''
Simulating reduced championships:
    -If only best of x races counted towards WDC, for the shorter variants, a simple fraction rounded up will be assumed.
    -Ties are awarded to both (or more) drivers
'''
#RULESETS:
bestraces = 1 #How much of the best results (rounded up) are counted for WDC
year = 2016 #year to filter on
targetpos = [1,2,3,4,5] #position to rank against

with open(r"C:\Users\Uzivatel\Downloads\newout.csv","r",encoding="UTF-8") as f:
    table = csv.reader(f,delimiter=',')
    table1 = []
    for row in table:
        table1.append(row)
table = table1

filtered_table = []
'''
Table formats:
    Table: [Driver, Points, Year, Round, Constructor,Position],[..]..
'''
for row in range(len(table)):
    for item in range(6):
        try:
            if re.match(r"[0-9]\.[0-9]",table[row][item]) != None: #result is float
                table[row][item] = float(table[row][item])
            else:
                table[row][item] = int(table[row][item])
        except:
            continue

roundmax = 0
for line in table: #filter each entry in table
    if line[2] == year: #entry is a result for a year we want
        filtered_table.append(line)
        if line[3] > roundmax:
            roundmax = line[3]
table = filtered_table

lst = range(roundmax)
combinations_list = [] #enter the total 

for i in lst: #each i is cycle length
    comb = list(itertools.combinations(lst,i+1))
    for j in comb:
        combinations_list.append(j)

class Driver:
    def __init__(self,name):
        self.name = name
        self.seasonpoints = []
        self.seasonpositions = []
        self.fullseason = []
        self.score = 0 #this is the like wins or other not the points
        self.totalpoints = 0
        self.tied = False
        self.position = 0
        for _ in range(roundmax):
            self.fullseason.append(0)
    def ssum(self):
        self.totalpoints = sum(self.seasonpoints)

driverlist = []
drivernamelist=[]
for line in filtered_table:
    if line[0] not in drivernamelist:
        driverlist.append(Driver(line[0]))
        drivernamelist.append(line[0])

for driver in driverlist:
    for entry in table:
        if entry[0] == driver.name:
            driver.fullseason[entry[3]-1] = entry

print("starting count")
#"main loop" determing the results of x place
finaltable = []
for num, tgetpos in enumerate(targetpos):
    for driver in driverlist:
        driver.score = 0
        counter = 0
    for season in combinations_list:
        resultlist = []
        for driver in driverlist:
            driver.seasonpoints = []
            driver.seasonpositions = []
        for driver in driverlist: 
            for race in season:
                '''so here, a combination is like, races (1,5,6) then we need to eval the points results for each driver to determine the WDC and for that we need to eval each race'''
                try:
                    driver.seasonpoints.append(driver.fullseason[race][1])
                    if type(driver.fullseason[race][5]) is str:
                        driver.seasonpositions.append(99)
                    else:
                        driver.seasonpositions.append(driver.fullseason[race][5])
                except TypeError:
                    driver.seasonpoints.append(0)
                    driver.seasonpositions.append(99) #arbitrary 99th place is high enough

        for driver in driverlist:
            driver.seasonpoints.sort(reverse=True)
            driver.seasonpositions.sort()
            if bestraces == 1:
                driver.ssum()
            resultlist.append(driver)
        if bestraces != 1:
            slengh = math.ceil((len(season)*bestraces)) # how many races to be counted
            for driver in driverlist:
                driver.seasonpoints[:slengh]
                driver.ssum()
        resultlist_sorted = driversort(resultlist)
        #resultlist_sorted = sorted(resultlist,key=lambda driver: driver.totalpoints,reverse=True)
        for driver in resultlist_sorted:
            if driver.position == tgetpos:
                driver.score += 1
        counter += 1
        if counter % 10000 == 0:
            print(counter," seasons simulated")
    if num == 0:
        for driver in driverlist:
            finaltable.append([driver.name,driver.score])
    else:
        for i, driver in enumerate(driverlist): 
            finaltable[i].append(driver.score)
print("saving...")

with open(r"C:\Users\Uzivatel\Documents\new_out"+str(1)+".csv","w+",encoding='UTF-8') as f:
    writer = csv.writer(f)
    for row in finaltable:
        writer.writerow(row)
print("done!")
input()
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

allresults()'''