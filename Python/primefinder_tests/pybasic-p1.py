import time

iterable_limit =0

def check(i):
    for x in Primes:
        if i % x == 0:
            return 0
    return 1

while(iterable_limit<=8):

    start = time.process_time()
    Primes = [2]
    i=3


    while(i<(10**iterable_limit)):
        if(check(i))==1:
            Primes.append(i)
        i=i+1

    end = time.process_time()
    print("e+",iterable_limit," executed in : ",end-start," seconds")
    iterable_limit=iterable_limit+1
