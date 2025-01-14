# scDUAL-seq
Source code of the manuscript **scDUAL-seq Simultaneously Measures RNA Synthesis and Degradation Rates in Single Cells**.

# Content
### TC&GA calling pipeline for bulk assays includes the following steps:
+ Step1_raw_fastqc.py: unzip the file and ulitize fastqc to quality control the file.

+ Step2_trim_fastqc_ver0.02.py: organize adapters_RNA.fasta based on the FastQC results and known adapters. Then perform quality control on the original sequencing file based on the adapter file.

+ Step3_star_and_annotation.sh: align high-quality reads using STAR (v2.7.3a) and add strandedness tag to the sam file.

+ Step4_extract_alignment_info_GRChg38_bulk_v4.sh: sam2tsv (https://github.com/lindenb/jvarkit/; version ec2c2364) is used to extract detailed alignment information from bam files and then T-to-C and G-to-A substitutions are identified in both experimental and control samples (double metabolic RNA labeling without Dual TimeLapse chemistry treatment, as a control for background mutations).

+ Step5_background_correction.pl: exclude the genomic sites with background T-to-C and G-to-A substitutions from the downstream analysis.

+ Step6_mutation_count.sh: count gene mutations.

### TC&GA calling pipeline for scDUAL-seq data includes the following steps:
+ Step1_Drop_seq.py: utilize the Drop-seq computational pipeline (James Nemesh, McCarroll Lab, version 1.12; Macosko et al., 2015) to map the reads to the genome and tag the reads with cell barcode, UMI barcode, and gene annotation in bam files. Next, we extracted intronic reads in the bam file because the legacy Drop-seq computational pipeline (version 1.12) only considers exonic reads.

+ Step2_extract_alignment_info_GRChg38_MAPQ.sh: sam2tsv is used to extract detailed alignment information from bam files and then T-to-C and G-to-A substitutions are identified in both experimental and control samples (double metabolic RNA labeling without Dual TimeLapse chemistry treatment, as a control for background mutations).

+ Step3_substract_background_locus_v2.sh: exclude the genomic sites with background T-to-C and G-to-A substitutions from the downstream analysis.

+ Step4_generate_NDS_matrix.sh: generate labeled and unlabeled gene expression matrix.

+ Generate_NDS_matrix_noType_new_old_total_4cmd_v2.R and select_deg_sys_RNA_fromCountFile.py: work together to extract three kinds of digital gene-cell expression matrices (one for the GA reads, one for the sum of TC and GA&TC reads, and one for the total reads) from the matrix generated in Step4.

# Data
+ Raw data files are available at NCBI Gene Expression Omnibus (GEO) (https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE286521).
