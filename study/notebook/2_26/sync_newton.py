# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:22:25 2018

@author: 80504
"""
import numpy as np
import sys
sys.path.append('C:/Users/80504/study/git/kaggle/study/NM_Source') 
from newtonRaphson2 import *
import time
#override
 
if __name__ == '__main__':
    start_time = time.time()
    numbers = [];
    for elem in range(-1000,1000):
        numbers.append(np.array([1.0*elem]))
    for number in numbers:
        newtonRaphson2(lambda x:x*x-1,number)
    print("The DT is",time.time()-start_time)       
