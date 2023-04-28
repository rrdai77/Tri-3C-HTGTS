Find documentation and examples at https://github.com/rrdai77/Tri-3C-HTGTS/

For any question about Tri-3C-HTGTS, please contact dairrsmu@163.com

# Tri-3C-HTGTS
 Tri-3C-HTGTS is a analysis pipeline designed to process multi-way chromatin interactions of 3C-HTGTS data.
 
# Introduction
 The 3C-HTGTS is a method combined the chromosome conformation capture (3C) and high-throughput genome-wide translocation sequencing (HTGTS), which provides high resolution and reproducible interaction profiles of a bait locale of interest with whole genome ([Jain, S. et al., Cell, 2018](https://www.sciencedirect.com/science/article/pii/S009286741830566X?via%3Dihub)).
 This Tri-3C-HTGTS repository provides support for analyzing multi-way chromatin interactions of 3C-HTGTS data from raw fastq files (paired-end Illumina data) to normalized contact maps. For raw contact matrices correction, these interaction counts are normalized for a total of 1,000,000 interactions at the same resolutions. Similar to HiC-Pro, Tri-3C-HTGTS can use phasing data to build contact maps. It only supports the 3C-HTGTS protocols, including digestion protocol.
 Tri-3C-HTGTS is sequential and each step of the workflow can be run independantly.
 Its code contains several steps:
 1) 3CHTGTS-QC;
 2) 3CHTGTS-PrimerSort;
 3) 3CHTGTS-Merge;
 4) 3CHTGTS-LoopCut;
 5) 3CHTGTS-Map;
 6) 3CHTGTS-Filter;
 7) 3CHTGTS-Extract;
 8) 3CHTGTS-ToMatrix;
 9) 3CHTGTS-ContinueRemove;
 10) 3CHTGTS-Tri;
 11) 3CHTGTS-Report

# Citation
 If you use HiC-Pro, please cite :
 Ranran Dai, Yongchang Zhu, Zhaoqiang Li, Litao Qin, Nan Liu, Shixiu Liao, Bingtao Hao. High-order chromatin structure of the mouse Tcra-Tcrd locus reveals the
competition of the proximal Vα genes and the Jα genes for interacting with the enhancer Eα. Nucleic Acids Research 2023.

# How to install it ?
## Software
This pipeline has a number of dependencies including the following:
- python (3.7);
- fastp (0.20.0);
- Cutadapt (v1.18);
- Pear (v0.9.6);
- Bowtie2 (v2.4.5);
- SAMtools (v1.9);
- Bedtools (v2.29.2);

## Installation
### Linux / Mac
Open terminal and type following:
```
tar -zxvf 

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

- Copy and edit the configuration file 'config-hicpro.txt' in your local folder. See the manual for details about the configuration file










