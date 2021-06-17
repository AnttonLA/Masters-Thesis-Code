@ Antton Lamarka, 2021-06-17
# Global README file for the complete Master's Thesis Project in Bioinformatics at Lund University 2021

This file describes the overall steps I've taked while working on my Master's Thesis. It is as comprehensive as possible, but some of the less relevant steps have been left out. Many of the steps refer to external files, usually jupyer notebooks or other scripts. These files contain more detailed descriptions of each individual step. The files can be found on my GitHub: https://github.com/AnttonLA/Masters-Thesis-Code

For this project, I designed and completed the phenotyping of over 3000 cord blood samples using flow cytometry. I then did extensive data analysis on the results, and even a pilot Genome Wide Association Study with genotype data that was available for a subset of the samples. 
 
## 1 - Gating with AliGater

AliGater is a flow cytometry gating tool written in python. It allows for semi-automatic gating, making an otherwise tedious task relatively simple by applying pattern recognition apporaches to discern cell populations. AliGater can be downloaded here: https://github.com/LudvigEk/aligater

The gating strategy for cord blood samples was designed iteratively, with individual gates being first created in interactive python notebooks, and the complete strategy being implemented later in regular python scripts. The final gating script is described in the file `batch_gating.py`. An example of a notebook used to desing individual gates can be found in the file 'gating_strategy_notebook.ipynb'.

While ultimately failed and thus irrelevant to the overall analysis, the notebook 'CD38_exploration.ipynb' shows my attempts at trying to separate CD38+ events in a dynamic way instead of relying on a 30% fixed threshold.

## 2 - Quality Control and Repeat Analysis correlation

### Sample Quality Control 
The jupyter notebook `QC_of_images.ipynb` was used to perform Quality Control on the downsampled images stored during gating. A PCA was used to detect incorrecly gated/weird looking samples. A detailed description of each step can be found in the notebook. (Note that some of the paths in the file will need to be edited for it to work fully.)

### Repeat Measurement Correlation

The notebook 'Repeat_Analysis_Correlation.ipynb' was used to asses the robustness of AliGater when compared to manual gating. A detailed description of each step can be found in the notebook. (Note that some of the paths in the file will need to be edited for it to work fully.)

## 3 - Data Exploration: Replicating Mantri et al.

Mantri et al. reports no correlation between total CD34+ and HSC levels. 'Replicating Mantri et al.ipynb' explores the cord blood data and finds that this is not true. A detailed description of each step can be found in the notebook. (Note that some of the paths in the file will need to be edited for it to work fully.)

## 4 - Association Study

Small scale association study for 14 candidate SNPs suspected to have an effect on blood phenotypes. 694 samples were used to build linear regression models. The notebook 'association_study_800.ipynb' contains detailed, step by step explanation of the analysis.

### PPM1H - expanded genotyping

Genotype data was expanded upon for the SNP rs699585 in the hopes that the increased sample size would reveal a stronger signal. The notebook `association_study_2000.ipynb` contains details on the steps taken during the analysis. 

## 5 - GWAS

### Pre-processing: perform PCA and filter outlying samples
#### Steps to follow to perform a PCA in PLINK2 for genotype data stored in separate BGEN files

###### STEP1 - Install BGEN, to get 'cat-bgen'. Needed to merge all BGEN files into one.

 #Dowload
wget http://code.enkre.net/bgen/tarball/release/bgen.tgz

 #Un-tar
tar -xvzf bgen.tgz

 #Compile it
cd bgen
./waf configure
./waf

 #Test it
./build/test/unit/test_bgen
./build/apps/bgenix -g example/example.16bits.bgen -list

 #Install apps
./waf configure --prefix=/path/to/installation/directory
./waf install

###### STEP 2 - Merge all BGEN files using 'cat-bgen'. Needed to be able to do PCA in PLINK2

cat-bgen -g file1.bgen [file2.bgen...] -og concatenated.bgen  # In my case: 'cat-bgen -g $(cat mergelist.txt) -og merged.bgen',   where mergelist.txt contains the names of all .bgen files in order.

 #Index the merged BGEN file using 'bgenix'
 
bgenix -g merged.bgen -index
bgenix -g merged.bgen > merged_sorted.bgen

###### STEP 3 - Do PCA in Plink2, filtering for MAF and HWE and IBD?

plink --make-rel --bgen "/home/antton/TFM/PCA_for_GWAS/bgens/concatenated_sorted.bgen" --sample "/home/antton/TFM/PCA_for_GWAS/Sweden_CordBlood_wAliases_201130_ID2first(CATEGORICAL_VARIABLES).sample" --missing-code -9,NA --maf 0.05 --hwe 1e-6  --indep-pairwise 1000 0.3 --pca 20 --out sorted_merged_PCA 

### Explore PCs, MANUALLY remove outliers and perform GWAS

The jupyter notebook 'CD800_GWAS_notebook.ipynb' was used to remove the outlying samples and perform GWAS in Hail. A detailed description of each step can be found in the notebook itslef. The rank-based inverse normal transformation function used to normalize the phenotype data was taken from https://github.com/edm1/rank-based-INT

The GWAS results were visualized with the python tool `manhattan_generator`. It can be downloaded here: https://github.com/pgxcentre/manhattan_generator

Data exploration of the results was done in a separate notebook, called `chunk_read_GWAS_results.ipynb`. This notebook was used to load the resulst of the GWAS and filter through the variants to get those with the lowest p-values in each case. The candidate SNPs were then checked in HaploReg and the UCSC Genome Browser to look for related genes, chromatin accessibility, and tissues in which the genes got expressed. This was done in order to assess how believable the hits were.



 



