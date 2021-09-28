# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 00:17:03 2021

@author: Sritej. N
"""
from nltk import word_tokenize

#taking inputs of both train & test data
docs={}
docs[1]="Kyoto Osaka Taiwan"
docs[2]="Japan Kyoto"
docs[3]="Taipei Taiwan"
docs[4]="Macao Taiwan Shanghai"
docs[5]="London"
docs[6]="Taiwan Taiwan Kyoto"

#storing tokens from dataset in dictionary 
tokens={}
for i in range(1,7):
    t=word_tokenize(docs[i])
    tokens[i]=t

# key is docid, if value is 1 then class is Japan else its class is NotJapan
cIsJapan = {}
cIsJapan[1]=1
cIsJapan[2]=1
cIsJapan[3]=0
cIsJapan[4]=0
cIsJapan[5]=0

#counting how many docs has Japan as class
cAsJapan=0
for i in range(1,6):
    if(cIsJapan[i]==1):
        cAsJapan+=1
        
#calculating probability of classes
ProbOfClass=[0]*2
ProbOfClass[1]=cAsJapan/5
ProbOfClass[0]= 1-ProbOfClass[1]

# storing total no.of tokens in each class, key 0 is class NotJapan 
TotalCountTokens=[0]*2

# storing no.of occurences of each term in a class 
counts={}
for i in range(1,6):
    c=0
    if(cIsJapan[i]==1):
        c=1
        TotalCountTokens[1]+=len(tokens[i])
    else:
        TotalCountTokens[0]+=len(tokens[i])
    for t in tokens[i]:
        if t not in counts:
            counts[t]= [0]*2
        counts[t][c]+=1
        
UniqueTokens=len(counts)      

# calculating conditional probaility .. P( term | class )
condProb={}
for t,v in counts.items():
    if t in tokens[6]:
        condProb[t]=[0]*2
        for i in range(2):
            laplaceNum=counts[t][i]+1
            laplaceDenom=TotalCountTokens[i]+UniqueTokens
            condProb[t][i]=laplaceNum/laplaceDenom

ProbForTest=[0]*2
for c in range(2):
    score=ProbOfClass[c]
    for t in tokens[6]:
        score*=condProb[t][c]
    ProbForTest[c]=score

maxScore=max(ProbForTest)

Predicted_class=""
if(ProbForTest.index(maxScore)==1):
    Predicted_class="Japan"
else:
    Predicted_class="NotJapan"


confusion_matrix = [ [ 0 for i in range(2) ] for j in range(2) ]
TrueClass="Japan"

if(Predicted_class==TrueClass and TrueClass=="Japan"):
    confusion_matrix[0][0]+=1

if(Predicted_class=="Japan" and TrueClass=="NotJapan"):
    confusion_matrix[0][1]+=1
        
if(Predicted_class=="NotJapan" and TrueClass=="Japan"):
    confusion_matrix[1][0]+=1

if(Predicted_class=="NotJapan" and TrueClass=="NotJapan"):
    confusion_matrix[1][1]+=1



true_positive  = confusion_matrix[0][0]
false_positive = confusion_matrix[0][1]
false_negative = confusion_matrix[1][0]
true_negative  = confusion_matrix[1][1]

precision = true_positive/(true_positive + false_positive)
recall    = true_positive/(true_positive + false_negative)
f1_score  = 2*precision*recall/(precision+recall)


       
        
        
        