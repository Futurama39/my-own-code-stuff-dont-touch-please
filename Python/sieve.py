import time
i=1
while(i<9): #i>8 is evil
    start = time.process_time_ns()
    limit = 10**i

    def genlist(j=0):
        li = []
        while(j<limit+1):
            j=j+1
            li.append(j)
        return li

    def sieve(prime,li,i=0):
        i=prime*2
        while(i<limit+1):
            li[i-1]=0
            i=i+prime
        return li

    def choose_next_prime(prime,li):
        while(prime<limit):
            prime=prime+1
            if li[prime-1] != 0:
                return prime
        raise ProcessLookupError()

    prime = 2
    out = [2]
    l = genlist()
    try:
        while True:
            l = sieve(prime,l)
            prime = choose_next_prime(prime,l)
            out.append(prime)
    except ProcessLookupError:
        end = time.process_time_ns()
        print("On e+",i," executed in: ",end-start, "nanoseconds")
        i=i+1