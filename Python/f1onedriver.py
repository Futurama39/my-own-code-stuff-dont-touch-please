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
                            break
            else:                                                               #tie lost
                i+=1
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


#RULESETS:
bestraces = 0.85 #How much of the best results (rounded up) are counted for WDC
year = 1975 #year to filter on

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
        self.position = 0   
        self.tied = False 
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

driverlist = sorted(driverlist,key=lambda driver: driver.name)
for i, driver in enumerate(driverlist):
    print(i,": ",driver.name)
driverindex = int(input())
targetdriver = driverlist[driverindex]
placements = []
for i in enumerate(driverlist):
    placements.append(0)
#this will be the position argument for writing positions down
print("starting count")
counter = 0
#"main loop" determing the results of x place
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
        driver.seasonpoints.sort()
        driver.seasonpositions.sort()
        if bestraces == 1:
            driver.ssum()
        resultlist.append(driver)
    if bestraces != 1:
        slengh = math.ceil((len(season)*bestraces)) # how many races to be counted
        for driver in driverlist:
            driver.seasonpoints[:slengh]
            driver.ssum()
    resultlist_sorted = driversort(driverlist)
    #resultlist_sorted = sorted(resultlist,key=lambda driver: driver.totalpoints,reverse=True)
    placements[resultlist_sorted.index(targetdriver)] += 1
    counter += 1
    if counter % 1000 == 0:
        print(counter, "results done")
        

print("saving...")
outtable = []
for i, item in enumerate(placements):
    outtable.append([i+1,item])#+1 here because actual position is one place higher than the index
with open("C:\\Users\\Uzivatel\\Documents\\"+targetdriver.name+".csv","w+",encoding='UTF-8') as f:
    writer = csv.writer(f)
    for row in outtable:
        writer.writerow(row)
print("done!")
input()