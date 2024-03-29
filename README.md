Find documentation and examples at https://github.com/rrdai77/Tri-3C-HTGTS/

For any question about Tri-3C-HTGTS, please contact haobt123@smu.edu.com or dairrsmu@163.com

# Tri-3C-HTGTS
 Tri-3C-HTGTS is a analysis pipeline designed to process multi-way chromatin interactions of 3C-HTGTS data.
 
# Introduction
 The 3C-HTGTS is a method combined the chromosome conformation capture (3C) and high-throughput genome-wide translocation sequencing (HTGTS), which provides high resolution and reproducible interaction profiles of a bait locale of interest with whole genome ([Jain, S. et al., Cell, 2018](https://www.sciencedirect.com/science/article/pii/S009286741830566X?via%3Dihub)).   
 This Tri-3C-HTGTS repository provides support for analyzing multi-way chromatin interactions of 3C-HTGTS data from raw fastq files (paired-end Illumina data) to normalized contact maps. For raw contact matrices correction, these interaction counts are normalized for a total of 1,000,000 interactions at the same resolutions. Similar to HiC-Pro, Tri-3C-HTGTS can use phasing data to build contact maps. It only supports the 3C-HTGTS protocols, including digestion protocols.  
 Tri-3C-HTGTS is sequential and each step of the workflow can be run independantly.  
 Its code contains several steps:  
 1\) 3CHTGTS-QC;  
 2\) 3CHTGTS-PrimerSort;  
 3\) 3CHTGTS-Merge;  
 4\) 3CHTGTS-LoopCut;  
 5\) 3CHTGTS-Map;  
 6\) 3CHTGTS-Filter;  
 7\) 3CHTGTS-Extract;  
 8\) 3CHTGTS-ToMatrix;  
 9\) 3CHTGTS-ContinueRemove;  
 10\) 3CHTGTS-Tri;  
 11\) 3CHTGTS-Report

# Citation
 If you use HiC-Pro, please cite :  
 Ranran Dai, Yongchang Zhu, Zhaoqiang Li, Litao Qin, Nan Liu, Shixiu Liao, Bingtao Hao. Three-way contact analysis characterizes the higher-order organization of the Tcra locus.

# How to install it ?
## Software
This pipeline has a number of dependencies including the following:
- python (v3.7);
- seqtk (v1.3-r106);
- fastp (v0.20.0);
- Cutadapt (v1.18);
- Pear (v0.9.6);
- Bowtie2 (v2.4.5);
- SAMtools (v1.9);
- Bedtools (v2.29.2)

## Installation
### Linux / Mac
Open terminal and type following:
```
tar -zxvf Tri-3C-HTGTS-1.0.0.tar.gz
## Edit .bashrc file for environment configuration
echo 'export PATH=$PATH:MY_INSTALL_PATH/Tri-3C-HTGTS-1.0.0' >> ~/.bashrc 
echo 'export PATH=$PATH:MY_INSTALL_PATH/Tri-3C-HTGTS-1.0.0/bin' >> ~/.bashrc 
echo 'export PATH=$PATH:MY_INSTALL_PATH/Tri-3C-HTGTS-1.0.0/scripts' >> ~/.bashrc 
echo 'export PATH=$PATH:MY_INSTALL_PATH/Tri-3C-HTGTS-1.0.0/bin/utils' >> ~/.bashrc
## Activate .bashrc file 
source ~/.bashrc
```

# How to use it ?
## First have a look at the help message !
```
Tri-3C-HTGTS_pro --help
Tri-3C-HTGTS_pro
Copyright (c) 2020
Author(s): Ranran Dai
Description: Main script for mining multi-way chromatin interactions from 3C-HTGTS data.


Usage : Tri-3C-HTGTS_pro -i INPUT -o OUTPUT -c CONFIG [-s ANALYSIS_STEP] [-h] [-v]
Usage option -h|--help for more information

Tri-3C-HTGTS_pro 1.0.0
--------------
OPTIONS

         -i|--input INPUT : input data folder; each sub-folder for per sample;
         -o|--output OUTPUT : output folder;
         -c|--Conf CONFIG : configuration file for Tri-3C-HTGTS;
         [-s|--step ANALYSIS_STEP] : run only a subset of the Tri-3C-HTGTS_pro workflow:
                        s1_QC, s2_PrimerSort, s3_Merge, s4_LooPCut, s5_Map, s6_Filter, s7_Extract, s8_ToMatrix, s9_ContinueRemove, s10_Tri, s11_Report;
         [-h|--help]: help;
         [-v|--version]: version
--------------

Example:


                 Tri-3C-HTGTS_pro -i rawdata -c Config.txt -o Result
                 Tri-3C-HTGTS_pro -i rawdata -c Config.txt -o Result -s s8_ToMatrix s9_ContinueRemove s10_Tri
                 
```

## Data Preparation
### Annotation Files
In order to process the raw data, Tri-3C-HTGTS requires six annotation files. 
- A fasta reference genome file from the UCSC genome browser.
- A BED file of the restriction fragments after digestion. This file depends both of the restriction enzyme and the reference genome. See the 'reduced_genome' command of Tri-3C-HTGTS utilities for details about how to generate this file. This bed file is provided with the Tri-3C-HTGTS sources as examples.
```
chr1    0       3000190 HIC_chr1_1      0       +
chr1    3000190 3000812 HIC_chr1_2      0       +
chr1    3000812 3001047 HIC_chr1_3      0       +
chr1    3001047 3001118 HIC_chr1_4      0       +
chr1    3001118 3001794 HIC_chr1_5      0       +
chr1    3001794 3003208 HIC_chr1_6      0       +
chr1    3003208 3003262 HIC_chr1_7      0       +
(...)
```
- A fasta file of the restriction fragments after digestion. This file can be created from the enzyme-digested BED file by using 'bedtools getfasta' command.
- The bowtie2 indexes of this fasta file of the restriction fragments after digestion. See the [bowtie2 manual page](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) for details about how to create such indexes.
- A BED file contained the first three columns of BED file of restriction fragments after digestion. This BED file is given as examples.
```
chr1    0       3000190
chr1    3000190 3000812
chr1    3000812 3001047
chr1    3001047 3001118
chr1    3001118 3001794
chr1    3001794 3003208
chr1    3003208 3003262
(...)
```
- A table file of chromosomes' size. This file can be easily find on the UCSC genome browser.
```
chr1    195471971
chr2    182113224
chr3    160039680
chr4    156508116
chr5    151834684
chr6    149736546
chr7    145441459
(...)
```

### Configuration file information
- Copy and edit the configuration file 'Config.txt' in your local folder. An example, the details about the configuration file are as follows:
```
## Config information for Tri-3C-HTGTS


######## Part one: Genome file check ########

## Common dna restriction enzyme name: MboI, NlaIII
First_enzyme_name = MboI

## Enzyme cut site lable as "^"
EnzymeSite = ^GATC

## Reference genome name
Ref_nam = mm10

## Reference genome fasta file
Ref_Fa = MY_LOCAL_PATH/genome.fasta

## Path of fasta file of genome enzyme-digested and BED file
Reduced_genome_Fa = MY_LOCAL_PATH/genome-MboI.fasta
FRAGID = MY_LOCAL_PATH/genome-MboI.bed

## Path of the first three columns of BED file of enzyme-digested DNA fragments
ENFRAG = MY_LOCAL_PATH/genome-MboI_Loci.bed

## Bowtie2 index path
RefIndex = MY_LOCAL_PATH/genome-MboI_Index 

## Path of chromosome size file
CHROMSIZE = MY_LOCAL_PATH/genome.sizes.txt


######## Part two: Input ########

## Nest Primer sequence
NestPrimer = CTTGTTCTGATTGGATGGCGA

## Adapter Primer sequence
AdapterPrimer = GACTATAGGGCACGCGTGG

## Max cpus numbers used in this software
Thread = 16


######## Part three: Output ########

## Type of Analysis : 1D_PerCell, 1D_PerFragment, 2D_PerCell or 2D_PerFragment
TYPES =  1D_PerCell 1D_PerFragment 2D_PerCell 2D_PerFragment

## Resolution for triplet-interaction sparse matrix
BIN_SIZE = 1000 3000 5000 10000 

## Start coordinate and stop coordinate for local plot
START = 52420000
STOP = 55030000


######## Data ########
PAIR1_EXT = _1
PAIR2_EXT = _2


####### Rawdata ######
RAW_DIR = rawdata
```

### Put all input files in a named rawdata folder. The input files have to be organized with one folder per sample, such as:
```
Config.txt
rawdata
    sample1
        sample1_R1.fastq.gz
        sample1_R2.fastq.gz
    sample2
        sample2_R1.fastq.gg
        sample2_R2.fastq.gz
    *   ...
```

### Run Tri-3C-HTGTS
```
    MY_INSTALL_PATH/bin/Tri-3C-HTGTS_pro -i FULL_PATH_TO_DATA_FOLDER -o FULL_PATH_TO_OUTPUTS -c MY_LOCAL_CONFIG_FILE
```








