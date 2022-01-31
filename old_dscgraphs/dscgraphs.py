import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import re

import dscmsg
dscmsg.choosefile()
table = dscmsg.chart_get()

def combine(lst):
    #take two rows and combine them
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


if __name__ == "__main__":
    del table[0][0]
    x_axis = range(len(table[0]))
    ax = plt.gca()
    for line in table[1:]:
        plt.plot(x_axis,line,label=str(line[0]))
    plt.legend()
    plt.show()