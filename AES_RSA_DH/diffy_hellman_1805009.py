import random
def power(a,d,n):
    if (d==0):
        return 1
    if (d%2==0):
        t=power(a,d//2,n)
        return (t*t)%n
    else:
        t=power(a,d//2,n)
        return ((t*a)%n*t)%n
def miller_rabin(n,k):
    if (n%2==0):
        return False
    d=n-1
    s=0
    while(d%2==0):
        s+=1
        d=d//2
    for i in range(k):
        a=random.randrange(2,n-1)
        x=power(a,d,n)
        for j in range(s):
            y=power(x,2,n)
            if(y==1 and x!=1 and x!=n-1):
                return False
            x=y
        if (y!=1):
            return False
    return True
def generate_prime(k):
    while(True):
        n=random.randrange(2**(k-1),2**(k))
        if(miller_rabin(n,5)):
            return n
def generate_p(k):
    while(True):
        n=random.randrange(2**(k-1),2**(k))
        if(miller_rabin(n,5) and miller_rabin((n-1)//2,5)):
            return n
def generate_g(min,max,p,k):
    while(True):
        g=random.randrange(min,max+1)
        if (power(g,2,p)!=1 and power(g,k,p)!=1):
            return g

        




