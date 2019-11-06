def factor(i,j=1):
    out=list()
    while i+1>j:
        if i%j==0:
            out.append(j)
        j=j+1
    return out


def main(limit):
    print(1)
    i=2
    while limit>0:
        y=sum(factor(i))
        print(y)
        i=y
        limit=limit-1           

main(100)

'''def main(limit):
    print(1)
    i=2
    while limit>0:
        inp = factor(i)
        j=0; y=0
        try:
            while True:
                x=inp[j]
                y=y+x
                j=j+1
        except:
            pass
        print(y)
        i=y
        inp = list()            
        limit = limit-1
'''
