#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 20:13:01 2019

@author: carrascod
"""

import pandas as pd
import requests
import io
import numpy as np

base_url = "http://www3.nd.edu/~mcdonald/Data/Finance_Word_Lists"

url  = ("LoughranMcDonald_Positive.csv",
                   "LoughranMcDonald_Negative.csv",
                   "LoughranMcDonald_Uncertainty.csv",
                   "LoughranMcDonald_Litigious.csv",
                   "LoughranMcDonald_ModalStrong.csv",
                   "LoughranMcDonald_ModalWeak.csv")

category = ("positive", "negative", "uncertainty",
            "litigious", "modal_strong", "modal_weak")

words = []

for i in range(len(category)):
    r = requests.post(base_url+'/'+url[i])
    if r.ok:
        data = r.content.decode('utf8')
        words.append(pd.Series.tolist((pd.read_csv(io.StringIO(data), squeeze=True)).T))

url_f = [base_url + s  for s in url]

df = pd.DataFrame({'url': url_f, 
                   'words': words}, index=category)


df["words"] = df["words"].apply(", ".join) #Delete brackets from the list
df = df.rename_axis('category')

df.to_csv("lm_words.csv")
