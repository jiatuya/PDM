# one time code
# select user confirmed new patient data and save in new folder
# 7/26/2019

# output 389 new user confirmed data in new_sample_7_26


import pandas as pd
df = pd.read_csv("new_sample_7_26/allAnalysisIds.csv")
df_selected = df.loc[df["status"] != "SUCCESS"]


id_list = df_selected["#id"].unique()
id_list = [str(i) + "_allsites.csv" for i in id_list]

import os
files = os.listdir("new_sample_7_26/all/")

count = 0
for f in files:
    if f in id_list:
        data = pd.read_csv("new_sample_7_26/all/"+ f, sep="\t")
        if sum(data["user_confirm"]>0):
            data = data[["染色体位置","HGVS","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]]
            data.rename(index=str, columns={"染色体位置": "loc", "表型相关度": "related_rate", "系统结论": "system_result"})
            data.to_csv("new_sample_7_26/files_new/"+ f, sep='\t')
            count = count+1
        else: print(f)
    else:
        print(f)
    print(count)
