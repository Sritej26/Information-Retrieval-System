# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 13:41:46 2021

@author: Sritej. N
"""
from nltk.tokenize import word_tokenize
import nltk
sno = nltk.stem.SnowballStemmer('english')
for d in range(1,253):
    s=str(d)+".txt"
    path='C:/Users/Sritej. N/Desktop/data/'+s
    T = open(path, encoding = 'utf-8', errors = 'ignore').read()
    des="stem"+s
    f=open (des,"a",encoding="utf-8")
    w=word_tokenize(T)
    for i in w:
        if(i.isalpha()):
            f.write(sno.stem(i))
            f.write(" ")
    f.close()

