def fb(f=3,b=5,i=1):
    output=" "
    while i<100:
        if i%f==0:
            output=output+"Fizz"
        if i%b==0:
            output=output+"Buzz"
        if output==" ":
            output=i
        print(output)
        i+=1    
fb(3,7)