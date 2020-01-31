import time
i=1

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
            return [1,prime]
    return [0]

while(True): #every program gets 15 minutes to perform the best it can so there's no reason to stop 
    start = time.process_time()
    limit = 10**i
    prime = [1,2]
    out = [2]

    l = genlist()

    while True:
        l = sieve(prime[1],l)
        prime = choose_next_prime(prime[1],l)
        if prime[0]==0:
            break
        out.append(prime[1])

    end = time.process_time()
    print("On e+",i," executed in: ",end-start, "seconds")
    i=i+1