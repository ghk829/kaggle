# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 16:44:35 2018

@author: 80504
"""

with open("words.txt",'r') as f:
    line = f.readline();
    while line !="":
        word = line.rstrip()
        print(len(word));
        line = f.readline();
    