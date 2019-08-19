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
[phenotype counts](./value_counts.txt)

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

## Reference

Adzhubei, I. A., Schmidt, S., Peshkin, L., Ramensky, V. E., Bork, P., Kondrashov, A. S., & Sunyaev, S. R. (n.d.). PolyPhen supplementary materials. Nature Methods, 7(4).

Adzhubei, I. A., Schmidt, S., Peshkin, L., Ramensky, V. E., Gerasimova, A., Bork, P., … Sunyaev, S. R. (2010). A method and server for predicting damaging missense mutations. Nature Methods, 7(4), 248–249. https://doi.org/10.1038/nmeth0410-248  

Adzhubei, I., Jordan, D. M., & Sunyaev, S. R. (2013). Predicting functional effect of human missense mutations using PolyPhen-2. Current Protocols in Human Genetics. https://doi.org/10.1002/0471142905.hg0720s76  

Capriotti, E., & Fariselli, P. (2017). PhD-SNPg: A webserver and lightweight tool for scoring single nucleotide variants. Nucleic Acids Research, 45(W1), W247–W252. https://doi.org/10.1093/nar/gkx369  

Davydov, E. V., Goode, D. L., Sirota, M., Cooper, G. M., Sidow, A., & Batzoglou, S. (2010). Identifying a high fraction of the human genome to be under selective constraint using GERP++. PLoS Computational Biology, 6(12). https://doi.org/10.1371/journal.pcbi.1001025  

Ding, W. H., Han, L., Xiao, Y. Y., Mo, Y., Yang, J., Wang, X. F., & Jin, M. (2017). Role of Whole-exome Sequencing in Phenotype Classification and Clinical Treatment of Pediatric Restrictive Cardiomyopathy. Chinese Medical Journal, 130(23), 2823–2828. https://doi.org/10.4103/0366-6999.219150  

Dong, C., Wei, P., Jian, X., Gibbs, R., Boerwinkle, E., Wang, K., & Liu, X. (2015). Comparison and integration of deleteriousness prediction methods for nonsynonymous SNVs in whole exome sequencing studies. Human Molecular Genetics, 24(8), 2125–2137. https://doi.org/10.1093/hmg/ddu733  

Jarvik, E. R., Jamal, S. M., Rosenthal, E. A., Cooper, G. M., Kim, D. S., Ranchalis, J., … Taylor, K. D. (2015). Actionable exomic incidental findings in 6503 participants: challenges of variant classification. Genome Research, 25(3), 305–315. https://doi.org/10.1101/gr.183483.114  

Katsonis, P., Koire, A., Wilson, S. J., Hsu, T. K., Lua, R. C., Wilkins, A. D., & Lichtarge, O. (2014). Single nucleotide variations: Biological impact and theoretical interpretation. Protein Science, 23(12), 1650–1666. https://doi.org/10.1002/pro.2552  

Korvigo, I., Afanasyev, A., Romashchenko, N., & Skoblov, M. (2018). Generalising better: Applying deep learning to integrate deleteriousness prediction scores for whole-exome SNV studies. PLoS ONE, 13(3), 1–17. https://doi.org/10.1371/journal.pone.0192829  

Pena, L. D. M., Jiang, Y. H., Schoch, K., Spillmann, R. C., Walley, N., Stong, N., … Robertson, A. K. (2018). Looking beyond the exome: A phenotype-first approach to molecular diagnostic resolution in rare and undiagnosed diseases. Genetics in Medicine, 20(4), 464–469. https://doi.org/10.1038/gim.2017.128  

Ramensky, V., Bork, P., & Sunyaev, S. (2002). Human non-synonymous SNPs: server and survey. Nucleic Acids Research, 30(17), 3894–3900.  

Richards, S., Aziz, N., Bale, S., Bick, D., Das, S., Gastier-Foster, J., … Rehm, H. L. (2015). Standards and guidelines for the interpretation of sequence variants: A joint consensus recommendation of the American College of Medical Genetics and Genomics and the Association for Molecular Pathology. Genetics in Medicine, 17(5), 405–424. https://doi.org/10.1038/gim.2015.30  

Shendure, J. (2014). A general framework for estimating the relative pathogenicity of human genetic variants, 46(3), 310–315. https://doi.org/10.1038/ng.2892.A  

Shihab, H. A., Rogers, M. F., Gough, J., Mort, M., Cooper, D. N., Day, I. N. M., … Campbell, C. (2015). An integrative approach to predicting the functional effects of non-coding and coding sequence variation. Bioinformatics, 31(10), 1536–1543. https://doi.org/10.1093/bioinformatics/btv009  

Sunyaev, S. R., Eisenhaber, F., Rodchenkov, I. V., Eisenhaber, B., Tumanyan, V. G., & Kuznetsov, E. N. (1999). PSIC: profile extraction from sequence alignments with position-specific counts of independent observations. Protein Engineering, Design and Selection, 12(5), 387–394. https://doi.org/10.1093/protein/12.5.387  

Tipping Michael. (2001). Sparse Bayesian Learning and the Relevance Vector Machine. Journal of Machine Learning Research. Retrieved from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.568.7983&rep=rep1&type=pdf  

Wang, X., Shen, X., Fang, F., Ding, C. H., Zhang, H., Cao, Z. H., & An, D. Y. (2019). Phenotype-driven virtual panel is an effective method to analyze Wes data of neurological disease. Frontiers in Pharmacology, 9(s1), 1–11. https://doi.org/10.3389/fphar.2018.01529  

Yue, P., Melamud, E., & Moult, J. (2006). SNPs3D: Candidate gene and SNP selection for association studies. BMC Bioinformatics, 7, 1–15. https://doi.org/10.1186/1471-2105-7-166  

## Appendix I 
| Feature  | Note | Example (not from a same SNV) |Selected in filtered dataset|
| ---------- | -----------|-----------|-----------|
| chrom   |  chromosome number | chr1|| 
| S/p/M   |  prediction for SIFT, Polyphen2 and M-CAP  |T/B/P| |
| REVEL/M-CAP  | score for REVEL and M-CAP |0.034/-1.0|:heavy_check_mark: |  
| loc  |  location on chromosome  |12921132| |
|  gene |  gene name  | PRAMEF2||
|REF   |  reference single nucletide | A||
| ALT  |  alternative single nucletide  |G| |
|  HGVS |  HGVS annotation for the SNV  |PRAMEF2:NM_023014: exon4:c.923A>G:p.E308G|:heavy_check_mark:|
| Func.ensGene | type of the SNV location |exonic|    |
| ExonicFunc_refGene | mutation type|nonsynonymous SNV|  :heavy_check_mark:  |
| het/hom  |  heterozygous/homozygous  |het||
| rs ID  |  reference SNP ID number |rs9730080||
| Converge MAF  ||  0.200846  ||
| Clinvar  | Clinvar classification  |pathogenic:1 |:heavy_check_mark:|
| HGMD  | HGMD classification  | DM|:heavy_check_mark:|
| ensemblID  | Ensembl Genomes ID |  ENSG00000219481 ||
| MAF in ESP6500 | frequency in ESP-6500 variants|0.0028	 |   |
| MAF in 1000g  | frequency in 1000 Genomes project|  0.04556 ||
| MAF in ExAC_ALL  |frequency in the Exome Aggregation Consortium| 0.0198 |  |
| highest_freq  |  highest freq among above three variables | 0.04556||
|SIFT score | SIFT prediction score|0.014|:heavy_check_mark:|
| Polyphen2 score  |  Polyphen2 prediction score  |0.448	|:heavy_check_mark:|
|  MutationTaster_score |  MutationTaster prediction score  |1||
|  MutationTaster_pred | MutationTaster classification   |P	||
|  Polyphen2 HDIV_pred |  Polyphen2 classification  |B||
| SIFT pred  | SIFT classification   |D||
| chrom loc  | chromosome # + location  | chrX:50350408	|:heavy_check_mark:|
|  heterozygosity |heterozygosity |  0.382716  ||
|  pheno_related rate | how much this SNV related to phenotype | 1.94 |:heavy_check_mark:|
| 0/1 in Converge  |  population annotation   |359	||
| gAD_E_EAS  |  population annotation    |0.1205||
|  0/0 in Converge | population annotation  |  30	 ||
| 1/1 in Converge  |  population annotation  | 10251	 ||
| ExAC_EAS  |   population annotation   |0.0012	||
|  Reference |   PubMed ID |2495303||
| gnomAD exome_ALL  |population annotation  |  0.016	  ||
|  SplicingPre |  splicing prediction|  no |:heavy_check_mark:|
| disease  | related disease   |SIMPSON-GOLABI-BEHMEL综合征1型；SGBS1 肾母细胞瘤1；WT1||
|  FinalResult | union set of system result and user confirm |Uncertain significance |:heavy_check_mark:|
| depth  | sequencing depth   |122||
| system_result  |suggestion based on ACMG standard|  Pathogenic  |:heavy_check_mark:|
| user_confirm  |describe if user select this SNV for final result or not, selected = 1, marked = 2, not selected = 0 |  1 |:heavy_check_mark:|
