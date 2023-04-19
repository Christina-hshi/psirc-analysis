# psirc-analysis
Analysis in the [Psirc](https://github.com/Christina-hshi/psirc) project. Our work has been published in Genome Research. \
**Ken Hung-On Yu\*, Christina Huan Shi\*, Bo Wang, Savio Ho-Chit Chow, Grace Tin-Yun Chung, Ke-En Tan, Yat-Yuen Lim, Anna Chi-Man Tsang, Kwok-Wai Lo, Kevin Y. Yip. Quantifying full-length circular RNAs in cancer. Genome Research 31.12 (2021): 2340-2353.** Available from: https://genome.cshlp.org/content/31/12/2340.short

## Simulation
### Data set 1
We simulated 11 groups of genes. Each group contained 500 genes with one linear isoform and one circular isoform having independent expression levels, leading to 1000 isoforms per group. The 11 groups differed by the degree of overlap between the linear and circular sequences, ranging from 0% to 100%. Then we applied psirc and Sailfish-cir to estimate expression levels (**Figure 3**).

#### Requirements
- [polyesterLC](https://github.com/Christina-hshi/polyester-LC.git) (A custom version of polyester for sequencing simulation of linear and circular transcripts jointly)\
A polyesterLC package is distributed inside this repo. You can install with the folllowing command in R.
```
install.packages("./simulation/polyesterLC_1.9.7.tar.gz", repos=NULL, type="source")
```
- [psirc-quant](https://github.com/Christina-hshi/psirc) (Our quantification method)
- [sailfish-cir](https://github.com/zerodel/sailfish-cir.git) (Quantification method to compare)

#### The pipeline
The pipeline can be run with the following commands to generate the simulation data, do the quantification, and compute statistics, which will be saved in log files.
```
cd ./simulation/500genes500trans
./genDataAndRun.sh <path to psirc-quant> <path to sailfish-cir> <k>
```
##### Simulation data generation
To generate the simulation data only, please run following commands.
```
cd ./simulation/500genes500trans
./gen_data.sh
```
##### Output files
```
./overlap.<per>/          #overlap percentage will be from 0-100
    trans.fa              #transcript sequences(linear + circular)
    trans.linear.fa       #linear transcript sequences only
    trans.circular.fa     #circular transcript sequences only
    trans.expr            #expression value of all transcripts.
    polyesterLC.9M.L100/  
        readPerTrans.num  #Number of reads sequenced from each transcript.
        sample_01_1.fasta #Paired-end read file #1
        sample_01_2.fasta #Paired-end read file #2
```

## Contact
For questions related to running the scripts, please raise issues in this GitHub repository.
