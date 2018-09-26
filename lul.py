def pyramid(i,text):
    j=1
    k=0
    while (i>j):
        k=k+1
        print(text,end='')
        if(k==j):
           print()
           k=0
           j=j+1     
    while (j>0):
        k=k+1
        print(text,end='')
        if(k==j):
            print()
            k=0
            j=j-1
pyramid(10,"a ")