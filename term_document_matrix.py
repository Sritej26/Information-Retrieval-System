# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:55:15 2021

@author: Sritej. N
"""
from nltk.tokenize import word_tokenize
import pandas as pd
import json
import math
tdm={}
inverted_index={}
dfreq={}

for i in range(1,253):
    s="stem"+str(i)+".txt"
    T = open(s, encoding = 'utf-8', errors = 'ignore').read()
    w=word_tokenize(T)
    for t in w:
        if t not in tdm:
            tdm[t]=[0]*253
        tdm[t][i]+=1
        if t not in inverted_index:
            inverted_index[t]=[]
        if i not in inverted_index[t]:
            inverted_index[t].append(i)
        # try:
        #     inverted_index[t].add(i)
        # except:
        #     inverted_index[t] = {i}
            
for key, values in inverted_index.items():
    dfreq[key]=len(inverted_index[key])

    
tfidf={}
for t,values in tdm.items():
    tfidf[t]=[0]*253
    idf=math.log10(252/dfreq[t])
    for i in range(1,253):
        if(tdm[t][i]>0):
            tf=1+math.log10(tdm[t][i])
            tfidf[t][i]=tf*idf

  
    
    





# df = pd.DataFrame(tfidf)
# df_t=df.T
# df_t.to_csv('tfidf.csv')


# with open("term_document_count.json", "w") as outfile: 
#     json.dump(tdm, outfile)


# with open("inverted_index.json", "w") as outfile: 
#     json.dump(inverted_index, outfile)
