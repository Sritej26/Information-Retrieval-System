# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 15:55:15 2021

@author: Sritej. N
"""
from nltk.tokenize import word_tokenize
import pandas as pd
import json
import math
import nltk
from nltk.corpus import stopwords
#from collections import Counter
from heapq import nlargest
import matplotlib.pyplot as plt


stops = set(stopwords.words("english"))         

#stemmer          
sno = nltk.stem.SnowballStemmer('english')

tdm={}
inverted_index={}
dfreq={}

#term_document_matrix and inverted_index
for i in range(1,253):
    path="C:/Users/Sritej. N/Desktop/stemming/stem"+str(i)+".txt"
    T = open(path, encoding = 'utf-8', errors = 'ignore').read()
    w=word_tokenize(T)
    for t in w:
        if t not in tdm:
            tdm[t]=[0]*253
        tdm[t][i]+=1
        if t not in inverted_index:
            inverted_index[t]=[]
        if i not in inverted_index[t]:
            inverted_index[t].append(i)
            
#document_frequency        
for key, values in inverted_index.items():
    dfreq[key]=len(inverted_index[key])
    
for key,value in dfreq.items():
    s=key+"-df="+str(value)
    inverted_index[s]=inverted_index[key]
    del inverted_index[key]
    
#calculating tf idf for each token_document pair
tfidf={}
for t,values in tdm.items():
    tfidf[t]=[0]*253
    idf=math.log10(252/dfreq[t])
    for i in range(1,253):
        if(tdm[t][i]>0):
            tf=1+math.log10(tdm[t][i])
            tfidf[t][i]=tf*idf

#calculating tfidf vector lengths of docs
doc_length={}
for i in range(1,253):
    length=0
    for t,v in tdm.items():
        length+=v[i]*v[i]
    doc_length[i]=math.sqrt(length)


Queries=[]     
Queries.append("what is trending on twitter")
Queries.append("Recent Technological changes or advancements")
Queries.append("Movements led by Mahatma Gandhi")
Queries.append("Indian festivals different from holi,diwali celebrated across different countries of world")
Queries.append("Live or latest cricket score and news")

count=0
query_Avg_prec={}

for query in Queries:
    query_tokens= word_tokenize(query)
    query_noStopWord = [w for w in query_tokens if not w in stops]
    query_stemmed=[sno.stem(w) for w in query_noStopWord if w.isalpha()]

    query_tfidf={}
    for q in set(query_stemmed):
        idf=math.log10(252/dfreq[q])
        tf=1+math.log10(query_stemmed.count(q))
        query_tfidf[q]=tf*idf
    query_length=0
    
    for key,value in query_tfidf.items():
        query_length+=value*value
    query_length=math.sqrt(query_length)
    
    cosine_similarity={}
    for i in range(1,253):
        score=0
        for key,value in query_tfidf.items():
            score+= value*tfidf[key][i]
        denominator=doc_length[i]*query_length
        cosine_similarity[i]=score/denominator
    
    
    
    # Getting Top10 highest cosine_similarity docs w.r.t query
    Top10 = nlargest(10, cosine_similarity, key = cosine_similarity.get)
    
    count+=1
    path="C:/Users/Sritej. N/Desktop/Relevance_Judgements/Relevance"+str(count)+".txt"
    J= open(path, encoding = 'utf-8', errors = 'ignore').read()
    relevant_docs=word_tokenize(J)
    
    p=0
    precision=0
    Avg_pre=0
    
    for i in range(10):
        if str(Top10[i]) in set(relevant_docs):
           p+=1
           precision=p/(i+1)
           Avg_pre+=precision
        
    Avg_pre/=len(relevant_docs)
    query_Avg_prec[count]=Avg_pre

MAP=0
for key,value in query_Avg_prec.items():
    MAP+=value
MAP=MAP/5

fig = plt.figure(figsize = (5, 5))
plt.bar(query_Avg_prec.keys(),query_Avg_prec.values(),width=0.4)
plt.xlabel("Query Numbers")
plt.ylabel("Average Precision values")
plt.title("Average Precision of Queries")
#converting dictionary to dataframe and then to csv
df = pd.DataFrame(tfidf)
df_t=df.T
df_t.to_csv('tfidf.csv')

#converting dictionary to jason format
with open("term_document_count.json", "w") as outfile: 
    json.dump(tdm, outfile)


with open("inverted_index.json", "w") as outfile: 
    json.dump(inverted_index, outfile)
