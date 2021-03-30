# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 14:32:24 2021

@author: Sritej. N
"""
# from search_engines import Yahoo


# engine = Yahoo()
# results = engine.search("tour with friends", 8)
# engine.output("csv")
import os
import pandas as pd
import requests
# from dragnet import extract_content
import justext
df = pd.read_csv('cricket.csv')
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
    