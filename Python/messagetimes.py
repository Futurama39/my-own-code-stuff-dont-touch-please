import os
import math
import csv
import re
from glob import glob
import cProfile

path = "C:\\Users\\Uzivatel\\Documents\\di_exports\\gaytc\\"
username = "Ilucuthen#8498"
utcoffset = -6

out = [[],[]]
pattern = r'\[[0-9-]+T([0-9]+:[0-9]+):[0-9]+\] '+username

def placetime(time):
    time = re.match(r'([0-9]+):([0-9]+)',time)
    hours = int(time.group(1))
    minutes = int(time.group(2))
    pos = (hours+utcoffset) * 60 + minutes
    if pos >= 1440:
        pos -= 1440
    out[1][pos] += 1 #increase message at correct pos

def findtime(line):
    mathchobj = re.match(pattern,line)
    return mathchobj

def main():


    for i in range(0,24):
        if i < 10:
            i = "0"+str(i)
        for j in range(0,60):
            if j < 10:
                j = "0"+str(j)
            out[0].append(str(i)+":"+str(j))
    for i in range(0,1440):
        out[1].append(0)

    files = glob(path+'*.txt')
    print('found ',len(files),' text files!')
    for log in files:
        with open(log,'r',1,"UTF8") as l:
            lines = l.readlines() #serialies all lines of txt into list line by line
            lines = lines[:-6:] #get rid of the last six lines
            lines = lines[4::]
            for line in lines:
                match = findtime(line)
                if match != None:
                    match = match.group(1)
                    placetime(match)

    fileiter = 0
    while True:     #find the lowest <num> for filename "out<num>.csv" that does not exist
        if os.path.isfile(path+'out'+str(fileiter)+'.csv'):
            fileiter+=1
        else:
            break

    with open (path+'out'+str(fileiter)+'.csv','w+',1,'UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(out)

    print("done")

if __name__ == "__main__":
    main()