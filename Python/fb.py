def fb(f=3,b=5,i=0,j=100):
    if (j<=i):
        print("Error: Starting value has to be lower than ending value.")
    while(i<j):       
        if(i%f==0):
            print("Fizz",end='')
        if(i%b==0):
            print("Buzz",end='')
        if(i%f!=0 and i%b!=0):
            print(i,end='')
        print()
        i=i+1
fb(3,7,140,18)