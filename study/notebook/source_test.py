# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 23:29:18 2018

@author: 80504
"""

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

import os
import sys
sys.path.append('C:/Users/80504/study/git/kaggle/study/NM_Source')
import numpy as np
A = np.array([[3,-1,4],[-2,0,5],[7,2,-2]])
B=A.astype(float).copy()
print(B)
print(LUdecomp(B))
print(B)
print(LUdecomp(B))