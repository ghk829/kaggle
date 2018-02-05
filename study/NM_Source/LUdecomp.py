## module LUdecomp
''' a = LUdecomp(a)
    LUdecomposition: [L][U] = [a]

    x = LUsolve(a,b)
    Solution phase: solves [L][U]{x} = {b}
'''
import numpy as np

def LUdecomp(a):
    n = len(a)
    tmp = a.copy();
    for k in range(0,n-1):
        for i in range(k+1,n):
           if tmp[i,k] != 0.0:
               lam = tmp[i,k]/tmp[k,k]
               tmp[i,k+1:n] = tmp[i,k+1:n] - lam*tmp[k,k+1:n]
               tmp[i,k] = lam
    return tmp

def LUsolve(a,b):
    n = len(a)
    for k in range(1,n):
        b[k] = b[k] - np.dot(a[k,0:k],b[0:k])
    b[n-1] = b[n-1]/a[n-1,n-1]    
    for k in range(n-2,-1,-1):
       b[k] = (b[k] - np.dot(a[k,k+1:n],b[k+1:n]))/a[k,k]
    return b

