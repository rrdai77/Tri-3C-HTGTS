Find documentation and examples at https://github.com/rrdai77/Tri-3C-HTGTS/

For any question about Tri-3C-HTGTS, please contact dairrsmu@163.com or use the Tri-3C-HTGTS forum

# What is 3C-HTGTS assay?
 The 3C-HTGTS is a method combined the chromosome conformation capture (3C) and high-throughput genome-wide translocation sequencing (HTGTS), which provides high resolution and reproducible interaction profiles of a bait locale of interest with whole genome [Jain, S. et al., Cell, 2018](https://www.sciencedirect.com/science/article/pii/S009286741830566X?via%3Dihub).
 
# What is Tri-3C-HTGTS?
 This repository provides support for analyzing multi-way chromatin interactions of 3C-HTGTS data from raw fastq files (paired-end Illumina data) to normalized contact maps. For raw contact matrices correction, these interaction counts are normalized for a total of 1,000,000 interactions at the same resolutions. Similar to HiC-Pro, Tri-3C-HTGTS can use phasing data to build contact maps. It only supports the 3C-HTGTS protocols, including digestion protocol.
 Tri-3C-HTGTS is sequential and each step of the workflow can be run independantly.
