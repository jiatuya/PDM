# A Pathogenic Single-nucleotide Variant Prediction Model for Asian Genetic Disease Community

## Introduction
Whole exome sequencing has been used widely in individual patient diagnosis and large-scale research projects since its first clinical diagnosis in 2009. It is a faster, and more economical way to find potential pathogenic SNVs in patients' genome. Unlike Whole Genome Sequencing (WGS), which sequence every single point in patients' genome, WES only sequences the exon region. In this study, all data are generated using WES.

There are various models out there for SNV pathogenicity prediction/classification, include PolyPhen2, SIFT, M-CAP, SNPs3D, GERP++, REVEL, PhD-SNP, CADD and so on. These models could be classified as 3 types

In spite of various models mentioned above, there is no model tranied and verified specifily for East Asian community. With the raw data collected from hospitals from China, we expect to generate a ensembel model that accurately predict pathogenic SNVs. The purpose of this study is to train a model that could predict and rank nsSNP by pathogenicity and generate a score for each mutation point as reference for clinical decision-making. 



## Data 
There are 1402 patients' annotated variants (17,633,323 points in total ) in the database so far, which are used to train and test the model. As time goes by, the model would learn and improve itself as more data kick in.

After annotation, every variant has following variables, details are in Appendix I: 
> "chrom", " S/p/M", "REVEL/M-CAP", "loc", "gene", "REF", "ALT", "HGVS", "Func.ensGene", "ExonicFunc_refGene", "het/hom", "rs ID", "Converge MAF", "Clinvar", "HGMD", "ensemblID", "MAF in ESP6500", "MAF in 1000g", "MAF in ExAC_ALL", "highest_freq", "SIFT score", "Polyphen2 score", "MutationTaster_score", "MutationTaster_pred", "Polyphen2 HDIV_pred", "SIFT pred", "chrom loc", "heterozygosity", "pheno_related rate", "0|1 in Converge", "gAD_E_EAS", "0|0 in Converge", "1|1 in Converge", "ExAC_EAS", "Reference", "gnomAD exome_ALL", "SplicingPre", "disease", "FinalResult", "depth", "system_result" and "user_confirm". 

The data are collected by PuYun Medical Company from hospitals in Wuhan, China. The bioinformatic analysis and annotation were performed by a medical assistant decision-making system, powered by OceanCloud Gene Company. All data are unpublished.  

## Method
### Data cleaning 
As only about 0.002% points are marked as pathogenic/ likely pathogenic, it is essential to go through a re-sampling approach (thanks to advice from Dr. Blair). In this dataset, as we focus on pathogenic/likely pathogenic points more than the rest, a re-sampling method would apply. 

### Variable selection 
Not all annotations are useful. Non-meaningful variables will be dropped before model training. 

### Machine learning model 
Variant machine learning models are used to find an optimistic one. Models include Regression, SVM, Random Forest, and more. 

### Verification 
New data will be used to verify the existing model. 

## Limitations and Issues
The patients' phenotypes are not evenly distributed, some are 
解释WES的limitation
解释针对某一数据，不同的模型会有不同的表现
解释数据的缺失


## Current Progress
### 7/29/2019 update
A logistic regression model was built using randomly-selected half SNVs to predict pathogenicity risk. The outcome is based on ACMG standard, likely pathogenic/pathogenic are marked as positive, the rest are marked as negative. A random down-sampling method applied, missing values are filled by feature means. On test set, overall accuracy is around 74%, overall sensitivity is 84%, overall AUC is 0.80.

The features used are: 
> "SIFT", "polyphen2", "REVEL", "M-CAP", "count", "pheno_score", "C_NaN", "C_association", "C_benign", "C_benign/likely_benign", "C_conflicting_interpretations", "C_likely_benign","C_likely_pathogenic","C_not_provided","C_pathogenic", "C_pathogenic/likely_pathogenic", "C_uncertain_significance", "NaN_ExonicFunc", "frameshift deletion", "frameshift insertion", "frameshift substitution", "nonframeshift deletion", "nonframeshift insertion", "nonframeshift substitution", "nonsynonymous SNV", "stopgain","stoploss","synonymous SNV", "unknown", "DFP", "DM", "DM?", "DP", "FP", "NaN_HGMD" and “R”. The features after “pheno_score” are all dummy variables transformed from “Clinvar”, “ExonicFuc_refGene” and “HGMD”. 

Then another logistic regression model was built using the other half SNVs to predict final result (user selection). The outcome is based on previous user’s choice, annotated results/confirmed are marked as positive, the rest are marked as negative.  A random down-sampling method applied, missing values are filled by feature means. On test set, overall accuracy is around 79.1%, overall sensitivity is 85.5%, overall AUC is 0.86.

After this 

### Future Work Thoughts
1. Try other mahcine learning model like random forest with no filling missing values.  
2. Try different weights/down-sampling combinations.  
3. More features/annotations should have been added into the analysis if possible.  
4. Final goal is to identify potential pathogenic SNVs that has no annotated before.





## Reference

## Appendix I 
