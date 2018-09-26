def col(n,c=0):
    while(n!=1):
        c=c+1
        print(n)
        if n%2==0:
            n=n/2
        else:
            n=(n*3)+1
    print(1)
    print("Steps: ",end='')
    print(c)
col(5)