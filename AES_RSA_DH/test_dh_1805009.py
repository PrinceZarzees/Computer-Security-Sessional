import diffy_hellman_1805009 as dh
import time
from tabulate import tabulate
l=[128,192,256]
data=[]
for k in l:
    start=time.perf_counter()
    p=dh.generate_p(k)
    end=time.perf_counter()
    p_time=end-start
    start=time.perf_counter()
    pi=(p-1)//2
    g=dh.generate_g(2,p-1,p,pi)
    end=time.perf_counter()
    g_time=end-start
    start=time.perf_counter()
    a=dh.generate_prime(k//2)
    end=time.perf_counter()
    a_time=end-start
    start=time.perf_counter()
    b=dh.generate_prime(k//2)
    end=time.perf_counter()
    b_time=end-start
    start=time.perf_counter()
    A=dh.power(g,a,p)
    end=time.perf_counter()
    A_time=end-start
    start=time.perf_counter()
    B=dh.power(g,b,p)
    end=time.perf_counter()
    B_time=end-start
    start=time.perf_counter()
    key1=dh.power(B,a,p)
    end=time.perf_counter()
    key1_time=end-start
    start=time.perf_counter()
    key2=dh.power(A,b,p)
    end=time.perf_counter()
    key2_time=end-start
    print (key1,key2)
    data.append([k,p_time*1000,g_time*1000,a_time*1000,b_time*1000,A_time*1000,B_time*1000,key1_time*1000,key2_time*1000])

# Generate table
table = tabulate(data, headers=["k","p","g","a","b","A","B","key1","key2"], tablefmt="grid")

# Print table
print(table)
