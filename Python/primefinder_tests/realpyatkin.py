import time
import pyatkin

iterable_limit =0



while(iterable_limit<=9):

    start = time.process_time()
    Primes = [2]
    i=3
    pyatkin.SieveOfAtkin(10**iterable_limit)


    end = time.process_time()
    print("e+",iterable_limit," executed in : ",end-start," seconds")
    iterable_limit=iterable_limit+1
