# logestic regression model to predict SNV risk level
# 7/2/2019
# Xinglin Jia

# two Linear models
# first model classifies SNV to 2 levels: non-pathogenic, and pathogenic
# using variables "Clinvar score","HGMD","SIFT","polyphen2","pheno_score","count","REVEL","M-CAP”,”Func_ref"

# second model use predictions from first model to predict if user will select
# this model classifies predicted pathogenic data to 2 levels:
# users are recommended to select from the first result, using the prediction as a reference


import pandas as pd
import numpy as np
from pandas import ExcelWriter
import sys

# read single file
df = pd.read_csv("new_sample_7_26/files_new/20190617231697_allsites.csv", sep="\t")
# select variable
df  = df[["染色体位置","HGVS","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult"]]

# # filter data step 1: keep "Clinvar or HGMD or FinalResult/系统结论 is likely pathogenic/pathogenic"
# df_selected = df.loc[(df["Clinvar"].notna()) |
#                               (df["HGMD"].notna()) |
#                               (df["FinalResult"].str.contains("athogenic")) |
#                               (df["系统结论"].str.contains("athogenic"))]
# check duplicates
dup = df["HGVS"].value_counts()
dup[0]= 1
# delet duplicates by 染色体位置+HGVS
# df_drop_dup = df.drop_duplicates(subset=["染色体位置","HGVS"])
# df_filtered = df_drop_dup

# save duplicates as a col in df
df_dup = pd.DataFrame(dup)
df_filtered = df
df_filtered = df_filtered.set_index("HGVS")
df_filtered["count"] = df_dup
df_filtered["count"].fillna(1)

# split REVEL/M-CAP, drop original
df_filtered[['REVEL','M-CAP']]= df_filtered["REVEL/M-CAP"].str.split('/',expand = True)
df_filtered = df_filtered.drop(['REVEL/M-CAP'], 1)

# see missing value information
df_filtered = df_filtered.replace('-', np.nan)

# Clinvar quanlification
Clinvar_result = [None]* len(df_filtered)
count = 0
for i in df_filtered["Clinvar"]:
    if "likely" in str(i) and "benign" in str(i) and "/" in str(i) :
        Clinvar_result[count]= .125
    elif "likely" in str(i) and "benign" in str(i):
        Clinvar_result[count]= .25
    elif "benign" in str(i):
        Clinvar_result[count]= 0
    elif "uncertain" in str(i) and "significance" in str(i):
        Clinvar_result[count]= .5
    elif "conflicting" in str(i) and "interpretations" in str(i):
        Clinvar_result[count]= .625
    elif "not" in str(i) and "provided" in str(i):
        Clinvar_result[count]= .5
    elif "likely" in str(i) and "pathogenic" in str(i) and "/" in str(i):
        Clinvar_result[count]= .825
    elif "likely" in str(i) and "pathogenic" in str(i):
        Clinvar_result[count]= .75
    elif "pathogenic" in str(i):
        Clinvar_result[count]= 1
    elif "association" in str(i):
        Clinvar_result[count]= 0.5
    count += 1

df_filtered["Clinvar score"] = Clinvar_result

df_filtered["ExonicFunc_refGene"].value_counts()

# ExonicFunc_refGene numeric
Func_ref_result = [None]* len(df_filtered)
count = 0
for i in df_filtered["ExonicFunc_refGene"]:
    if str(i) == "synonymous SNV":
        Func_ref_result[count]= 0
    elif str(i) == "unknown" :
        Func_ref_result[count]= 0.5
    elif str(i) == "nonsynonymous SNV" :
        Func_ref_result[count]= .65
    elif str(i) == "nonframeshift deletion" :
        Func_ref_result[count]= .75
    elif str(i) == "nonframeshift insertion" :
        Func_ref_result[count]= .75
    elif str(i) == "frameshift insertion" :
        Func_ref_result[count] = .85
    elif str(i) == "frameshift deletion" :
        Func_ref_result[count] = .85
    elif str(i) == "stoploss" :
        Func_ref_result[count]= 1
    elif str(i) == "stopgain" :
        Func_ref_result[count]= 1
    count += 1


# 系统结论量化
result_result = [None]* len(df_filtered)
count = 0
for i in df_filtered["系统结论"]:
    if str(i) == "Benign":
        result_result[count]= 0
    elif str(i) == "Likely benign" :
        result_result[count]= .25
    elif str(i) == "Uncertain significance" :
        result_result[count]= .5
    elif str(i) == "Likely pathogenic" :
        result_result[count]= .75
    elif str(i) == "Pathogenic" :
        result_result[count]= 1
    count += 1

# FinalResult quanlification
final_result = [None]* len(df_filtered)
count = 0
for i in df_filtered["FinalResult"]:
    if str(i) == "Benign":
        final_result[count]= 0
    elif str(i) == "Likely benign" :
        final_result[count]= .25
    elif str(i) == "Uncertain significance" :
        final_result[count]= .5
    elif str(i) == "Likely pathogenic" :
        final_result[count]= .75
    elif str(i) == "Pathogenic" :
        final_result[count]= 1
    count += 1

# HGMD quanlification
HGMD_result = [None]* len(df_filtered)
count = 0
for i in df_filtered["HGMD"]:
    if str(i) == "DFP":
        HGMD_result[count]= 0
    elif str(i) == "FP" :
        HGMD_result[count]= 0
    elif str(i) == "R" :
        HGMD_result[count]= 0
    elif str(i) == "DP" :
        HGMD_result[count]= 0
    elif str(i) == "DM?" :
        HGMD_result[count]= .75
    elif str(i) == "DM" :
        HGMD_result[count]= 1
    count += 1

# new df to save training data
df_model = pd.DataFrame()
df_model["loc"] = df_filtered["染色体位置"]
df_model["result"] = result_result
df_model["final_result"] = final_result
df_model["Clinvar score"] = Clinvar_result
df_model["HGMD"] = HGMD_result
df_model["SIFT"] = df_filtered["SIFT score"]
df_model["polyphen2"] = df_filtered["Polyphen2 score"]

df_model["count"] = df_filtered["count"]
df_model["REVEL"] = pd.to_numeric(df_filtered["REVEL"])
df_model["M-CAP"] = pd.to_numeric(df_filtered["M-CAP"])
df_model["Func_ref"] = Func_ref_result

df_model["pheno_score"] = df_filtered["表型相关度"]

df_model = df_model.set_index("loc", append=True)

# fill missing value with mean of training set
df_model_mean = pd.DataFrame()
df_model_mean["result"] = df_model["result"]
df_model_mean["final_result"] = df_model["final_result"]
df_model_mean["Clinvar_score"]= df_model["Clinvar score"].fillna(0.257771)
df_model_mean["HGMD"]= df_model["HGMD"].fillna(0.511506)
df_model_mean["SIFT"]= df_model["SIFT"].fillna(0.133229)
df_model_mean["polyphen2"]= df_model["polyphen2"].fillna(0.416009)
df_model_mean["count"]= df_model["count"].fillna(1)
df_model_mean["REVEL"]= df_model["REVEL"].fillna(0.283482)
df_model_mean["M-CAP"]= df_model["M-CAP"].fillna(-0.446159)
df_model_mean["Func_ref"]= df_model["Func_ref"].fillna(-0.008085)
df_model_mean["pheno_score"]= df_model["pheno_score"].fillna(10.281871)


from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
X = df_model_mean[["Clinvar_score","HGMD","SIFT","polyphen2","pheno_score","count","REVEL","M-CAP","Func_ref"]]

# normalize data
sc = StandardScaler()
sc.fit(X)
X_std = sc.transform(X)
print(X_std[1])
print(X_std[2][1])
print("#######################################")

pred_result = [None]* len(df_model_mean)

for i in range(len(df_model_mean)):
    pred_result[i] = X_std[i][0]*-0.16514471+X_std[i][1]*-0.1889155+X_std[i][2]*-0.24703824+X_std[i][3]*-0.11130814+X_std[i][4]*-0.04335512
    + X_std[i][5]*-0.5799974+ X_std[i][6]*0.24598562 + X_std[i][7]*0.62559867 + X_std[i][8]*1.56123627

print(pred_result)

pred_final_result = [None]* len(df_model_mean)
count = 0
for i in range(len(df_model_mean)):
    if i > .5:
        pred_result[count] = X_std[count][0]*0.84735134+X_std[count][1]*0.31442418+X_std[count][2]*-0.10786632+X_std[count][3]*0.02408951+X_std[count][4]*0.04404152
        + X_std[count][5]*-0.79827854+ X_std[count][6]*0.08158471 + X_std[count][7]*0.65929051 + X_std[count][8]*0.36921554
        count += 1
    else:
        pred_final_result[count] == 0

df_model["pred_final_result"] = df_model_mean["pred_final_result"]

# # p or not
# [[-0.16514471 -0.1889155  -0.24703824 -0.11130814 -0.04335512 -0.5799974 0.24598562  0.62559867  1.56123627]]
# # likely p or not
# [[ 0.84735134  0.31442418 -0.10786632  0.02408951  0.04404152 -0.79827854 0.08158471  0.65929051  0.36921554]]

from pandas import ExcelWriter
writer = ExcelWriter('20190221032251_pred.xlsx')
df_model.to_excel(writer)
writer.save()
