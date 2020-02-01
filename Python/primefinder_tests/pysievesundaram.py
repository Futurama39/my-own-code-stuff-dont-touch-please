import time
import math

iterable_limit =2


def lim_series(lim,i=1):                    #this is a series of decreasing integers becasue with each round of the sieve we don't have to count as high
    out = []
    while(True):
        new = math.ceil((lim-i)/(2*i+1))    #counted from the sieving formula of i+j+2ij<lim
        if i<new:                           #check if we can stop
            out.append(new)
        else:
            return out
        i+=1

def mainloop(lim):                          #main sieving by the Sundaram Sieve algorithm
    global mlist                            #we take this full list (from 1 to limit) and replace any "non primes" in them
    j=1                                     #we do this with the formula i+j+2ij where 1<=i<=j (it's not needed to preform the operation on 2,1 when 1,2 will give same result)
    i=1                                     
    lims=lim_series(lim)                    #the first function is ran to determine how high up we have to count
    listsize= len(lims)                     #looking at the size of the list to establish when to break the main while arg
    while(j<=listsize):
        limit=lims[j-1]                     #taking the relevant limit for each round
        i=j                                 #setting the main var to j, since we established i<=j
        while(i<=limit):
            pos = i+j+2*i*j                 #most important line, gets next position where to set the list to 0
            if pos > lim:                   #check as to not post into an empty position in the list
                pass
            else:
                mlist[pos-1] = 0            #here the relevant position on the main list is replaced with 0, counting it as "discarded"
            i+=1
        j+=1
    return 1                                #irrelevant, just info that the funct exited succesfully

'''lim = int((10**iterable_limit)/2)
start = time.process_time()
mlist = [i+1 for i in range(lim)]
mainloop(lim)
newlist=[]
print(mlist)
for i in mlist:
    if i!=0:
        newlist.append(i)
print(newlist)
Primes = [2]
for i in newlist:
    Primes.append(2*i+1)
    
print(Primes)'''

while(True):
    lim = int((10**iterable_limit)/2)       #the sieve then multiplies everything by 2 so we only need half the limit
    start = time.process_time()
    mlist = [i+1 for i in range(lim)]       #the list from 1-lim
    mainloop(lim)
    newlist=[]                              #in this list we paste just the non-zero part of the previous list
    for i in mlist:
        if i!=0:
            newlist.append(i)
    Primes = [2]                            #here into the Primes we take newlist and multiply every number by 2 and add 1 which gives us the final assembled list of primes
    for i in newlist:
        Primes.append(2*i+1)

    end = time.process_time()
    print("e+",iterable_limit," executed in : ",end-start," seconds")
    iterable_limit+=1