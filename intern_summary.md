# 阶段性总结：一个亚裔遗传病位点突变致病性的预测模型
Stage Summary: A Pathogenic Single-nucleotide Variant Prediction Model for Asian Genetic Disease Community

Xinglin (Jason) Jia  :shipit:
> A brief users guide can be found at [users_guide](users_guide.md).  

## 确定问题，了解背景知识

筛选高危位点，几率模型，主效位点

### 第一次讨论
#### 致病位点基于危险程度排序
1. 单个常见SNV
1. 组合SNV  
思考：针对某种疾病，按照数量/发病率(携带者和患者比例)/危险程度/生存曲线等排序，建立针对东亚人的模型
#### 发现未确诊疾病的致病基因，病情分类
思考：可以提出推测哪个位点/基因致病，需要临床后续检测验证，如Sanger等
#### SNV和疾病的关系
现阶段主要观点是：常见疾病由单个常见variant或一些非常见variants组合导致  
思考：得出结果对于研究比较有意义，临床应用不大，结论对提升排序模型有一些意义
#### 从nsSNP预测表型
思考：对胚胎筛查有用？患者是已经有phenotype再去检测，也许对病情发展预测有用？
#### De novo在现有遗传病里的分类
***
### 第二次讨论
#### 糖尿病分型
#### 地中海
#### 单一样本中8000个位点排序
1. 也许可以通过通路筛选
1. 在一些单基因病中精度会很高，比如耳聋
***
### 第三次讨论
#### 单一样本中位点排序
1. 首先基于ACMG标准（系统结论）预测该位点是否致病，并输出概率
1. 其次使用上一模型的结果，基于用户是否选择预测该位点是否会被用户选择/标记，并输出概率
***

## 数据 Data
### 训练数据 Data for training & testing
总共有1402例病人的样本（17,633,323 个 SNV）用来训练和验证模型。  
There are 1402 patients' annotated variants (17,633,323 SNV points in total ) in the database so far, which are used to train and test the model.  
标记过后，每个位点都有以下的所有特征：  
After annotation, every variant has following variables, details are in [Appendix I](#appendix-i): 
> "chrom", " S/p/M", "REVEL/M-CAP", "loc", "gene", "REF", "ALT", "HGVS", "Func.ensGene", "ExonicFunc_refGene", "het/hom", "rs ID", "Converge MAF", "Clinvar", "HGMD", "ensemblID", "MAF in ESP6500", "MAF in 1000g", "MAF in ExAC_ALL", "highest_freq", "SIFT score", "Polyphen2 score", "MutationTaster_score", "MutationTaster_pred", "Polyphen2 HDIV_pred", "SIFT pred", "chrom loc", "heterozygosity", "pheno_related rate", "0|1 in Converge", "gAD_E_EAS", "0|0 in Converge", "1|1 in Converge", "ExAC_EAS", "Reference", "gnomAD exome_ALL", "SplicingPre", "disease", "FinalResult", "depth", "system_result" and "user_confirm". 

### 验证数据 Data for verification
总共有423例新的病人样本用来验证模型。  
There are 423 patients' annotated variants used to verify the model.

### 表型数据 Phenotype data
[phenotype counts](value_counts.txt)

## 现在的进展 Current Progress
### 7/29/2019 update [python script](LR_model_all.py)
A logistic regression model was built using randomly-selected half SNVs to predict pathogenicity risk. The outcome is based on ACMG standard, likely pathogenic/pathogenic are marked as positive, the rest are marked as negative. **A random down-sampling method applied, missing values are filled by feature means.** On the test set, overall accuracy is around 74%, overall sensitivity is 84%, overall AUC is 0.80. [scalar](p_or_not_lr_scalar.sav) [model](p_or_not_lr_model.sav)

The features used are: 
> "SIFT", "polyphen2", "REVEL", "M-CAP", "count", "pheno_score", "C_NaN", "C_association", "C_benign", "C_benign/likely_benign", "C_conflicting_interpretations", "C_likely_benign","C_likely_pathogenic","C_not_provided","C_pathogenic", "C_pathogenic/likely_pathogenic", "C_uncertain_significance", "NaN_ExonicFunc", "frameshift deletion", "frameshift insertion", "frameshift substitution", "nonframeshift deletion", "nonframeshift insertion", "nonframeshift substitution", "nonsynonymous SNV", "stopgain","stoploss","synonymous SNV", "unknown", "DFP", "DM", "DM?", "DP", "FP", "NaN_HGMD" and “R”. The features after “pheno_score” are all dummy variables transformed from “Clinvar”, “ExonicFuc_refGene” and “HGMD”. 

Then another logistic regression model was built using the other half SNVs to predict the final result (user selection). The outcome is based on previous user’s choice, annotated results/confirmed are marked as positive, the rest are marked as negative.  **A random down-sampling method applied, missing values are filled by feature means.** On the test set, overall accuracy is around 79.1%, overall sensitivity is 85.5%, overall AUC is 0.86. [scalar](c_or_not_lr_scalar.sav) [model](c_or_not_lr_model.sav)

This model then used on 423 new data (not the test set) for verification, sensitivity, and specificity for each model are collected and presented below.  
![](verify_new_data.png)


## 未来工作的想法 Future Work Thoughts  
1. 尝试其他机器学习模型，如使用随机森林处理不填充缺失值的数据。Try other machine learning models like a random forest with no filling missing values.  
2. 尝试不同的权重/下取样方法的组合。Try different weights/down-sampling combinations.  
3. 如果可能的话更多的特征/注释应该放在分析里。More features/annotations should have been added into the analysis if possible.  
4. 最终目的应该是辨认之前没有注释过的SNV。The final goal is to identify potential pathogenic SNVs that has no annotated before.
