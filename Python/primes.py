primes = [2]

def isprime(num):
    check =  0
    try:
        while True:
            if num % primes[check] == 0:
                return False
            else:
                check = check+1
    except:
        return True

def find_primes(i=50):
    j=0
    num = 3 
    while(i>j):
        if isprime(num):
            primes.append(num)
            j = j+1
        num = num+1

find_primes(100)
print(primes)
