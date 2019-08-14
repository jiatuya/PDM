# A Pathogenic Single-nucleotide Variant Prediction Model for Asian Genetic Disease Community

> Note: This is a detailed Intro to this project. A brief users guide can be found at [users_guide](users_guide.md).  


Xinglin (Jason) Jia  :shipit:
## Introduction
In a human genome, there are about 180,000 exons, constituting about 1% of the whole human genome. Following the central dogma, exons are transcribed to mRNA, then translated to the protein that directly associated with phenotype expression. It is believed that non-silence mutations, especially the non-synonymous Single Nucleotide Variants (nsSNV) on exons might lead to various Mendelian and common polygenic diseases including cancer. It is essential to identify and understand the genetic variants that alter protein sequences. Whole Exome Sequencing (WES) is a technique that sequences the exon region in a genome. It firstly only selects exon regions, then sequence using next-generation high-throughput sequencing technology. WES is faster and more economical compared to Whole Genome Sequencing (WGS) which sequences every single nucleotide in the patients' genome, and it overcomes the limitation of designed microarray chips. It has been widely used in individual patient diagnosis and large-scale research projects since its first clinical diagnosis in 2009. 

Along with the massive data generated, there are various SNV pathogenicity prediction models has been developed in the past 20 years. The first type based on a structural metric of nsSNV impact, that they assume the diseased is solely based on the structure change of protein. These methods used statistical or empirical effectively energy function and require a structure for the region of the protein user investigation. The second type based on evolutionary principles, that assumes overrepresented substitutions in a protein family are neutral on protein function while the underrepresented ones are deleterious. The third type using both structure and homology, along with other information such as function annotation and biochemical prosperities. This type typically uses supervised machine learning techniques to handle different features and deal with noise and missing data. Commonly used machine learning techniques include Support Vector Machines, Naive Bayes, Neural Networks, Random Forests, and Decision Trees. 

In spite of various models mentioned above, there is no model out there trained and verified specifically for the East Asian community. With the raw data collected from hospitals from China, we expect to train an ensemble model that accurately predict pathogenic SNVs to support clinical decision-making. 



## Data 
There are 1402 patients' annotated variants (17,633,323 SNV points in total ) in the database so far, which are used to train and test the model. As time goes by, the model would learn and improve itself as more data kick in.

After annotation, every variant has following variables, details are in [Appendix I](#appendix-i): 
> "chrom", " S/p/M", "REVEL/M-CAP", "loc", "gene", "REF", "ALT", "HGVS", "Func.ensGene", "ExonicFunc_refGene", "het/hom", "rs ID", "Converge MAF", "Clinvar", "HGMD", "ensemblID", "MAF in ESP6500", "MAF in 1000g", "MAF in ExAC_ALL", "highest_freq", "SIFT score", "Polyphen2 score", "MutationTaster_score", "MutationTaster_pred", "Polyphen2 HDIV_pred", "SIFT pred", "chrom loc", "heterozygosity", "pheno_related rate", "0|1 in Converge", "gAD_E_EAS", "0|0 in Converge", "1|1 in Converge", "ExAC_EAS", "Reference", "gnomAD exome_ALL", "SplicingPre", "disease", "FinalResult", "depth", "system_result" and "user_confirm". 

The data are collected by PuYun Medical Company from hospitals in Wuhan, China. The bioinformatic analysis and annotation were performed by a medical assistant decision-making system, powered by OceanCloud Gene Company. All data are unpublished.  

## Methods
***Data Re-sampling***  
As only about 0.002% SNVs in the cleaned dataset is marked as pathogenic/likely pathogenic, it is essential to go through a re-sampling approach (thanks to advice from Dr. Blair). In this dataset, as we focus on pathogenic/likely pathogenic points more than the rest, a re-sampling method would apply.

***Variable Selection***  
Not all annotations are useful. Non-meaningful variables will be dropped before model training. Categorical variables were transferred to dummies.

***Machine Learning Model***  
Variant machine learning models are used to find an optimistic one. Models include Regression, SVM, Random Forest, and more. 

***Verification***  
New data will be used to test the performance of the existing model. 

## Limitations and Issues
The patients' phenotypes are not evenly distributed. Not all phenotype data were available, for existing data there were more epilepsy patients than others (see [phenotype counts](value_counts.txt)). This study combined SNVs from all 1404 patients, which lead to a question that whether this model had a bias to the majority phenotype SNVs even duplicates were removed.  

So many missing values were in the raw dataset, especially in the columns **"Clinvar"** and **"HGMD"**, which are two databases that record SNVs pathogenicity with published evidence. These two features were transferred to dummies.

## Current Progress
### 7/29/2019 update [python script](LR_model_all.py)
A logistic regression model was built using randomly-selected half SNVs to predict pathogenicity risk. The outcome is based on ACMG standard, likely pathogenic/pathogenic are marked as positive, the rest are marked as negative. **A random down-sampling method applied, missing values are filled by feature means.** On the test set, overall accuracy is around 74%, overall sensitivity is 84%, overall AUC is 0.80. [scalar](p_or_not_lr_scalar.sav) [model](p_or_not_lr_model.sav)

The features used are: 
> "SIFT", "polyphen2", "REVEL", "M-CAP", "count", "pheno_score", "C_NaN", "C_association", "C_benign", "C_benign/likely_benign", "C_conflicting_interpretations", "C_likely_benign","C_likely_pathogenic","C_not_provided","C_pathogenic", "C_pathogenic/likely_pathogenic", "C_uncertain_significance", "NaN_ExonicFunc", "frameshift deletion", "frameshift insertion", "frameshift substitution", "nonframeshift deletion", "nonframeshift insertion", "nonframeshift substitution", "nonsynonymous SNV", "stopgain","stoploss","synonymous SNV", "unknown", "DFP", "DM", "DM?", "DP", "FP", "NaN_HGMD" and “R”. The features after “pheno_score” are all dummy variables transformed from “Clinvar”, “ExonicFuc_refGene” and “HGMD”. 

Then another logistic regression model was built using the other half SNVs to predict the final result (user selection). The outcome is based on previous user’s choice, annotated results/confirmed are marked as positive, the rest are marked as negative.  **A random down-sampling method applied, missing values are filled by feature means.** On the test set, overall accuracy is around 79.1%, overall sensitivity is 85.5%, overall AUC is 0.86. [scalar](c_or_not_lr_scalar.sav) [model](c_or_not_lr_model.sav)

This model then used on 423 new data (not the test set) for verification, sensitivity, and specificity for each model are collected and presented below.  
![](verify_new_data.png)


### Future Work Thoughts
1. Try other machine learning models like a random forest with no filling missing values.  
2. Try different weights/down-sampling combinations.  
3. More features/annotations should have been added into the analysis if possible.  
4. The final goal is to identify potential pathogenic SNVs that has no annotated before.

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
