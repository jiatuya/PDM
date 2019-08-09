# logestic regression model to predict SNV risk level and user selection
# 7/26/2019
# Xinglin (Jason) Jia

# two Linear models
# first model classifies SNV to 2 levels: non-pathogenic, and pathogenic
# using variables "Clinvar score","HGMD","SIFT","polyphen2","pheno_score","count","REVEL","M-CAP”,”Func_ref"

# second model use predictions from first model to predict if user will select
# this model classifies predicted pathogenic data to 2 levels:
# users are recommended to select from the first result, using the prediction as a reference

def LR_model_all(filedir):
    import pandas as pd
    import numpy as np

    # read single file
    df = pd.read_csv(filedir, sep="\t")
    # select variable
    df = df[["染色体位置","HGVS","REVEL/M-CAP",
                       "SIFT score","Polyphen2 score","表型相关度",
                       "Clinvar","HGMD","ExonicFunc_refGene","系统结论","FinalResult","user_confirm"]]

    # drop mistake lines in appending original files
    df = df.loc[df["HGMD"] != "HGMD"]
    # combine 染色体位置 and HGVS as a new variable
    df["loc_HGVS"] = df["染色体位置"].map(str) + df["HGVS"]
    df = df.loc[df["loc_HGVS"].notna()]
    # check duplicates
    dup = df["loc_HGVS"].value_counts()
    # delete duplicates by 染色体位置+HGVS
    # note: len = 820159 after this step
    df_filtered = df.drop_duplicates("loc_HGVS")
    # save duplicates as a col in df
    df_dup = pd.DataFrame(dup)
    # index = loc_HGVS, added counts in df
    df_filtered = df_filtered.set_index("loc_HGVS")
    df_filtered["count"] = df_dup

    # split REVEL/M-CAP, S/p/M, drop original
    df_filtered[['REVEL','M-CAP']]= df_filtered["REVEL/M-CAP"].str.split('/',expand = True)
    df_filtered = df_filtered.drop(['REVEL/M-CAP'], 1)
    # remove non-meaningful values "-" and "-1.0"
    # note: "-" and "-1.0" means NaN in upstream analysis
    df_filtered = df_filtered.replace('-', np.nan)
    df_filtered = df_filtered.replace('-1.0', np.nan)

    # filter out meaningless data
    # note: len = 363511 after this step
    df_filtered = df_filtered.loc[(df_filtered["SIFT score"].notna()) |
                                (df_filtered["Polyphen2 score"].notna()) |
                                (df_filtered["表型相关度"].notna()) |
                                (df_filtered["Clinvar"].notna()) |
                                (df_filtered["HGMD"].notna()) |
                                (df_filtered["REVEL"].notna()) |
                                (df_filtered["M-CAP"].notna())]

    # Clinvar quanlification
    Clinvar_result = [None]* len(df_filtered)
    count = 0
    for i in df_filtered["Clinvar"]:
        if "likely" in str(i) and "benign" in str(i) and "/" in str(i) :
            Clinvar_result[count]= "C_benign/likely_benign"
        elif "likely" in str(i) and "benign" in str(i):
            Clinvar_result[count]= "C_likely_benign"
        elif "benign" in str(i):
            Clinvar_result[count]= "C_benign"
        elif "uncertain" in str(i) and "significance" in str(i):
            Clinvar_result[count]= "C_uncertain_significance"
        elif "conflicting" in str(i) and "interpretations" in str(i):
            Clinvar_result[count]= "C_conflicting_interpretations"
        elif "not" in str(i) and "provided" in str(i):
            Clinvar_result[count]= "C_not_provided"
        elif "likely" in str(i) and "pathogenic" in str(i) and "/" in str(i):
            Clinvar_result[count]= "C_pathogenic/likely_pathogenic"
        elif "likely" in str(i) and "pathogenic" in str(i):
            Clinvar_result[count]= "C_likely_pathogenic"
        elif "pathogenic" in str(i):
            Clinvar_result[count]= "C_pathogenic"
        elif "association" in str(i):
            Clinvar_result[count]= "C_association"
        else:
            Clinvar_result[count]= "C_NaN"
        count += 1

    df_filtered["Clinvar"] = Clinvar_result

    # 系统结论量化
    result_result = [None]* len(df_filtered)
    count = 0
    for i in df_filtered["系统结论"]:
        if str(i) == "Benign":
            result_result[count]= 0
        elif str(i) == "Likely benign" :
            result_result[count]= 1
        elif str(i) == "Uncertain significance" :
            result_result[count]= 2
        elif str(i) == "Likely pathogenic" :
            result_result[count]= 3
        elif str(i) == "Pathogenic" :
            result_result[count]= 4
        count += 1

    # transfer categorical to dummy variables
    df_Clinvar_dummy = pd.get_dummies(df_filtered["Clinvar"])
    df_filtered["ExonicFunc_refGene"] = df_filtered["ExonicFunc_refGene"].fillna("NaN_ExonicFunc")
    df_ExonicFunc_dummy = pd.get_dummies(df_filtered["ExonicFunc_refGene"])
    df_filtered["HGMD"] = df_filtered["HGMD"].fillna("NaN_HGMD")
    df_HGMD_dummy = pd.get_dummies(df_filtered["HGMD"])


    # new df to save training data
    df_model = pd.DataFrame()
    # location information
    df_model["loc"] = df_filtered["染色体位置"]
    df_model["HGVS"] = df_filtered["HGVS"]
    # outcome
    df_model["result"] = result_result
    df_model["user_confirm"] = pd.to_numeric(df_filtered["user_confirm"])
    # annotations
    df_model["SIFT"] = pd.to_numeric(df_filtered["SIFT score"])
    df_model["SIFT"] = df_model["SIFT"].fillna(df_model["SIFT"].mean())
    df_model["polyphen2"] = pd.to_numeric(df_filtered["Polyphen2 score"])
    df_model["polyphen2"] = df_model["polyphen2"].fillna(df_model["polyphen2"].mean())
    df_model["REVEL"] = pd.to_numeric(df_filtered["REVEL"])
    df_model["REVEL"] = df_model["REVEL"].fillna(df_model["REVEL"].mean())
    df_model["M-CAP"] = pd.to_numeric(df_filtered["M-CAP"])
    df_model["M-CAP"] = df_model["M-CAP"].fillna(df_model["M-CAP"].mean())
    df_model["count"] = pd.to_numeric(df_filtered["count"])
    df_model["pheno_score"] = pd.to_numeric(df_filtered["表型相关度"])
    df_model["pheno_score"] = df_model["pheno_score"].fillna(df_model["pheno_score"].mean())
    df_model["pheno_score"] = df_model["pheno_score"].fillna(0)

    # join dummy df to df_model
    df_model = df_model.join(df_Clinvar_dummy, how='outer')
    df_model = df_model.join(df_ExonicFunc_dummy, how='outer')
    df_model = df_model.join(df_HGMD_dummy, how='outer')

    for i in ["SIFT","polyphen2","REVEL","M-CAP","count","pheno_score",
                                 "C_NaN","C_association","C_benign","C_benign/likely_benign","C_conflicting_interpretations",
                                "C_likely_benign","C_likely_pathogenic","C_not_provided","C_pathogenic",
                                 "C_pathogenic/likely_pathogenic", "C_uncertain_significance", "NaN_ExonicFunc",
                                "frameshift deletion", "frameshift insertion", "frameshift substitution",
                                "nonframeshift deletion", "nonframeshift insertion", "nonframeshift substitution",
                                "nonsynonymous SNV", "stopgain","stoploss","synonymous SNV", "unknown","DFP","DM","DM?","DP",
                                "FP","NaN_HGMD","R"]:
        if i not in df_model.columns:
            df_model[i] = 0

    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import Perceptron
    from sklearn import metrics
    from sklearn.externals import joblib

    df_model_mean_l_b_p = df_model.loc[df_model["result"]>=0]
    df_model_mean_l_b_p["p_or_not"] = np.nan
    df_model_mean_l_b_p.loc[df_model_mean_l_b_p.result < 3, 'p_or_not'] = "0"
    df_model_mean_l_b_p.loc[df_model_mean_l_b_p.result >= 3, 'p_or_not'] = "1"
    df_model_mean_l_b_p.loc[df_model_mean_l_b_p.user_confirm < 1, 'c_or_not'] = "0"
    df_model_mean_l_b_p.loc[df_model_mean_l_b_p.user_confirm >= 1, 'c_or_not'] = "1"

    X = df_model_mean_l_b_p[["SIFT","polyphen2","REVEL","M-CAP","count","pheno_score",
                                 "C_NaN","C_association","C_benign","C_benign/likely_benign","C_conflicting_interpretations",
                                "C_likely_benign","C_likely_pathogenic","C_not_provided","C_pathogenic",
                                 "C_pathogenic/likely_pathogenic", "C_uncertain_significance", "NaN_ExonicFunc",
                                "frameshift deletion", "frameshift insertion", "frameshift substitution",
                                "nonframeshift deletion", "nonframeshift insertion", "nonframeshift substitution",
                                "nonsynonymous SNV", "stopgain","stoploss","synonymous SNV", "unknown","DFP","DM","DM?","DP",
                                "FP","NaN_HGMD","R"]]
    y_test = df_model_mean_l_b_p["p_or_not"]

    # load scalar from disk
    loaded_scalar = joblib.load("p_or_not_lr_scalar.sav")
    X_std = loaded_scalar.transform(X)


    # load model from disk
    loaded_model = joblib.load("p_or_not_lr_model.sav")

    predictions = loaded_model.predict(X_std)
    prob = loaded_model.predict_proba(X_std)
    df_pred = pd.DataFrame()
    df_pred["loc"] = df_model["loc"]
    df_pred["HGVS"] = df_model["HGVS"]
    df_pred["p_pred"] = predictions
    df_pred["p_prob"] = np.nan
    df_pred["p_prob"] = prob

    # from sklearn.metrics import confusion_matrix
    # y_true = df_pred["p_or_not"]
    # y_pred = df_pred["p_pred"]
    # p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp = confusion_matrix(y_true, y_pred).ravel()
    # p_or_not_sensitivity = p_or_not_tp / (p_or_not_tp+p_or_not_fn)
    # p_or_not_specificity = p_or_not_tn / (p_or_not_tn+p_or_not_fp)

    #################################################################################################
    #################################################################################################
    # second model for user selection
    y_test = df_model_mean_l_b_p["c_or_not"]

    # load scalar from disk
    loaded_scalar = joblib.load("c_or_not_lr_scalar.sav")
    X_std = loaded_scalar.transform(X)

    # load model from disk
    loaded_model = joblib.load("c_or_not_lr_model.sav")

    predictions = loaded_model.predict(X_std)
    prob = loaded_model.predict_proba(X_std)
    df_pred["c_pred"] = predictions
    df_pred["c_prob"] = np.nan
    df_pred["c_prob"] = prob

    # from sklearn.metrics import confusion_matrix
    # y_true = df_pred["c_or_not"]
    # y_pred = df_pred["c_pred"]
    # c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp = confusion_matrix(y_true, y_pred).ravel()
    #
    # c_or_not_sensitivity = c_or_not_tp / (c_or_not_tp+c_or_not_fn)
    # c_or_not_specificity = c_or_not_tn / (c_or_not_tn+c_or_not_fp)

    # return (p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp,
    #         p_or_not_sensitivity, p_or_not_specificity,
    #         c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp,
    #         c_or_not_sensitivity, c_or_not_specificity)
    return (df_pred)

# p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp,p_or_not_sensitivity, p_or_not_specificity, c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp,c_or_not_sensitivity, c_or_not_specificity = LR_model_all("new_sample_7_26/files_new/20190712274621_allsites.csv")
# print(p_or_not_tn, p_or_not_fp, p_or_not_fn, p_or_not_tp,p_or_not_sensitivity, p_or_not_specificity, c_or_not_tn, c_or_not_fp, c_or_not_fn, c_or_not_tp,c_or_not_sensitivity, c_or_not_specificity)


temp = LR_model_all("new_sample_7_26/all/20190725294310_allsites.csv")
print(temp)
