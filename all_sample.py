# load all sample to a table and save as cvs

import pandas as pd
import numpy as np
import os
files = os.listdir("files/")


count = 0
for f in files:
    count += 1
    data = pd.read_csv("files/"+ f, sep="\t")
    if set(["染色体位置","HGVS","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]).issubset(data.columns):
        data = data[["染色体位置","HGVS","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]]
        data.rename(index=str, columns={"染色体位置": "loc", "表型相关度": "related_rate", "系统结论": "system_result"})
        data.to_csv("files_new/"+ f, sep='\t')
    else:
        print(f)
    print(str(count/1404*100) + "%")


