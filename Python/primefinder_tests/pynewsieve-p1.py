import time

iterable_limit =0



while(True):
    lim = 10**iterable_limit
    start = time.process_time()
    Primes=[]
    i=2
    set1 = [True for i in range(lim+1)]
    while(i*i <=lim):
        if set1[i]==True:
            for x in range(i*i,lim+1,i):
                set1[i]=False
        i+=1
    for x in range(2,lim):
        if set1[x]:
            Primes.append(x)

    end = time.process_time()
    print("e+",iterable_limit," executed in : ",end-start," seconds")
    iterable_limit=iterable_limit+1
