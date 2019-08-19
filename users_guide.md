# logistic regression model to predict SNV risk level and user selection 
逻辑回归模型预测SNV的致病性和用户选择

7/26/2019  
Xinglin (Jason) Jia  
贾兴霖  

Two Logistic regression models, first model classifies SNV to 2 levels: non-pathogenic, and pathogenic
using variables "Clinvar score", "HGMD", "SIFT", "polyphen2", "pheno_score", "count", "REVEL","M-CAP”,”ExonicFunc_refGene";  
两个逻辑回归模型,第一个模型把SNV分类为两类，非致病和致病;  
the second model use predictions from first model to predict if user will select. This model classifies predicted pathogenic data to 2 levels: selected, not selected.  
第二个模型使用第一个模型的结果预测用户是否选择该SNV，该模型把SNV分类成两类，选择与不选择  


Users are recommended to select from the first result, using the prediction as a reference.  
推荐用户通过第一个模型的预测选择，将第二个模型的结果作为参考量  


## users's guide 使用方法 
Put LR_model_all.py, c_or_not_lr_model.sav, c_or_not_lr_scalar.sav, p_or_not_lr_model.sav, p_or_not_lr_scalar.sav in a same folder, open LR_model_all.py using python3,  
将 LR_model_all.py, c_or_not_lr_model.sav, c_or_not_lr_scalar.sav, p_or_not_lr_model.sav, p_or_not_lr_scalar.sav放在同一个文件夹，使用python 3打开LR_model_all.py  
all procedures are put in one function LR_model_all, input a table, output 6 columns:  
数据处理流程和调出模型等流程都被做成了一个方程LR_model_all，输入为一张表格，输出六列数值：  
1st column is chromosome and location, 2nd column is HGVS information, third column p_pred is prediction of pathogenic or not, 4th column p_prob is the probability of the third column being 0, 5th column c_pred is prediction of user select or not, 6th column c_prob is the probability of the sixth column being 0  
第一列染色体位置，第二列HGVS，第三列p_pred预测是否致病，第四列p_prob为p_pred为0的概率，第五列c_pred预测用户是否选择，第六列c_prob为c_pred为0的概率
