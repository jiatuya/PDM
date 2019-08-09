# one time code
# load all 癫痫 sample to a table
# 6/xx/2019

# output a excel table with all points in all patients

import pandas as pd
import numpy as np
import sys

data = pd.read_csv('medical_analysis_phenotype.txt',sep = "\t")
# select variables
df = pd.DataFrame(data[["id","hpo_chinese_name","hpo_id","hpo_name","medical_analysis_id"]])

# frequency stats
stat = df["hpo_chinese_name"].value_counts()
# unique stats
uniq = df["hpo_chinese_name"].unique()
# save result to file
pd.DataFrame(stat).to_csv("value_counts.txt", sep = "\t")

# check if any null
# print("Number of NaN in hpo_chinese_name is "+str(df["hpo_chinese_name"].isnull().sum().sum()))

# give a boolean array about epil appearance
pheno = df["hpo_chinese_name"]
epil = pheno.str.contains("癫痫")
epil_num = sum(epil)

# select samples with epil
dx = df[np.array(epil,dtype = bool)]
filtered_dx = dx[dx['hpo_chinese_name'].notnull()]

# phenotype unique medical id
id_list = dx["medical_analysis_id"].unique()

id_list = [str(i) + "_allsites.csv" for i in id_list]


import os
files = os.listdir("files/")

dx_all = pd.DataFrame()

count = 0
for f in files:
    if f in id_list:
        count += 1
        print(str(count/1404*100) + "%")
        data = pd.read_csv("files/"+ f, sep="\t")
        dx_all = dx_all.append(data)

dx_all_filtered= dx_all[["染色体位置","HGVS","disease","最大频率","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度","S/p/M",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]]

dx_all_filtered = dx_all_filtered.loc[(dx_all_filtered["Clinvar"].notna()) |
                              (dx_all_filtered["HGMD"].notna()) |
                              (dx_all_filtered["FinalResult"].str.contains("athogenic")) |
                              (dx_all_filtered["系统结论"].str.contains("athogenic"))]


from pandas import ExcelWriter
writer = ExcelWriter('dx_all_filtered.xlsx')
dx_all_filtered.to_excel(writer)
writer.save()


