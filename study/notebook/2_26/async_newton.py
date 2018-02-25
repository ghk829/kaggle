# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:25:14 2018

@author: 80504
"""

import sys
sys.path.append('C:/Users/80504/study/git/kaggle/study/NM_Source') 
from multiprocessing import Process
import numpy as np
from gaussPivot import *
import math
from multiprocessing import Pool
import multiprocessing
import time
#override
def newtonRaphson(x,tol=1.0e-9):
    def f(x):
        return x*x-1
    
    def jacobian(f,x):
        h = 1.0e-4
        n = len(x)
        jac = np.zeros((n,n))
        f0 = f(x)
        for i in range(n):
            temp = x[i]
            x[i] = temp + h
            f1 = f(x)
            x[i] = temp
            jac[:,i] = (f1 - f0)/h
        return jac,f0
    
    for i in range(30):
        jac,f0 = jacobian(f,x)
        if math.sqrt(np.dot(f0,f0)/len(x)) < tol:
            print(x)
        dx = gaussPivot(jac,-f0)
        x = x + dx
        if math.sqrt(np.dot(dx,dx)) < tol*max(max(abs(x)),1.0): return x
    print('Too many iterations')

 
if __name__ == '__main__':
    print("The Number of Core is",multiprocessing.cpu_count())
    start_time = time.time()
    numbers = [];
    for elem in range(-1000,1000):
        numbers.append(np.array([1.0*elem]))
    pool =  Pool(processes=4)
    pool.map(newtonRaphson,numbers)
    print("The DT is",time.time()-start_time) 