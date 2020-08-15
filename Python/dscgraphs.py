import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re

import dscmsg

table = dscmsg.chart_get('C:\\Users\\Uzivatel\\Documents\\di_exports\\new4\\',True)

vani = [r'starshooter',r'a7598201',r'b547650a']
cassady = [r'aRADia',r'aradia temporary account']
littlepage = [r'The Neolithian',r'6a739393']

def combine(lst):
    global table
    temptable = []
    global table
    for name in lst:
        for item in range(len(table)):
            if re.search(name,str(table[item])):
                app = table[item]
                app = app[1:]
                temptable.append(app)
                table.remove(table[item])
                break
    outtable = temptable[0]
    for i in range(1,len(temptable)):
        np.add(outtable,temptable[i])
    outtable.insert(0,lst[0]) #add the name
    table.append(outtable)

def comparison(lst): #takes in lists of row names to be displayed
    outtable = [] #TODO: actually make it parse regexes
    global table
    for i in lst:
        outtable.append(table[i])
    return outtable


combine(vani)
combine(cassady)
combine(littlepage)
table.sort()
table = comparison([16,9,12,13,14,18])


if __name__ == "__main__":
    x_axis = range(len(table[0])-1)
    ax = plt.gca()
    for line in table:
        plt.plot(x_axis,line[1:],label=str(line[0]))
    plt.legend()
    plt.show()