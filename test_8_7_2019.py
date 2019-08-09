from LR_model_all import LR_model_all
import pandas as pd
import os
files = os.listdir("new_sample_7_26/files_new/")

col_names =  ["filename", "p_or_not_tn", "p_or_not_fp", "p_or_not_fn", "p_or_not_tp",
              "p_or_not_sensitivity", "p_or_not_specificity",
                "c_or_not_tn", "c_or_not_fp", "c_or_not_fn", "c_or_not_tp",
                "c_or_not_sensitivity", "c_or_not_specificity"]
df = pd.DataFrame(columns = col_names)

count = 0
for i in files:
    print(i)
    data = pd.read_csv("new_sample_7_26/files_new/"+ i, sep="\t")
    if len(data) > 100:
        if set(["染色体位置","HGVS","REVEL/M-CAP",
                   "SIFT score","Polyphen2 score","表型相关度",
                   "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]).issubset(data.columns):
            dir = "new_sample_7_26/files_new/" + i
            p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp,p_or_not_sensitivity, p_or_not_specificity, c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp,c_or_not_sensitivity, c_or_not_specificity = LR_model_all(dir)
            df.loc[len(df)] = [i, p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp,p_or_not_sensitivity, p_or_not_specificity,c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp,c_or_not_sensitivity, c_or_not_specificity]
    count = count+1
    print(count/len(files))

df.to_csv("test_result_8_7_2019", sep='\t')
