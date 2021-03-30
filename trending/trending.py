# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 18:09:46 2021

@author: Sritej. N
"""
import os
import pandas as pd
import requests
import justext
df = pd.read_csv('trending.csv')
d=1
for i in range(len(df)):
    URL = df.iloc[i, 3] 
    
    try:
        print("at {}" .format(i))
        r=requests.get(URL)
        paragraphs = justext.justext(r.content, justext.get_stoplist("English"))
        s=str(d)+".txt"
        d+=1
        f=open (s,"a",encoding="utf-8")
        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                f.write(paragraph.text)
                f.write(" ")
        f.close()
        filesize = os.path.getsize(s)
        if filesize==0:
            d-=1
    except Exception:
        print("connection error at {}".format(i))

# import shutil
# dup=222

# for i in range(1,32):  
#     src="C:/Users/Sritej. N/Desktop/trending/"+str(i)+".txt"
#     dst="C:/Users/Sritej. N/Desktop/data/"+str(dup)+".txt"
#     dup+=1
#     shutil.copyfile(src,dst)
