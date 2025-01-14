#!/bin/bash

## This script excludes the locus which has T->C or G->A mutations in sample
## Pre-install requirment: sam2tsv, samtools, perl

sample=$1 # sample name with chemistry treatment
control=$2 # sample name without chemistry treatment
bam_dir=$3 # bam file folder including bam file which was generated in step1
tsv_dir=$4 # sample tsv file folder including tsv file which was generated in step2
tsv_dir2=$5 # control tsv file dir

############ 1. Substract mutations from control samples
perl /home/disk/dy_student/wsy/WPS/scripts/background_correction.pl -bg ${tsv_dir2}/${control}_both_strand_all_TC.tsv_q27.tsv -in ${tsv_dir}/${sample}_both_strand_all_TC.tsv_q27.tsv
perl /home/disk/dy_student/wsy/WPS/scripts/background_correction.pl -bg ${tsv_dir2}/${control}_both_strand_all_GA.tsv_q27.tsv -in ${tsv_dir}/${sample}_both_strand_all_GA.tsv_q27.tsv

############ 2. Extract mutation information
python ~/wsy/WPS/other_scripts/extract_mutation_to_dge_wps.py ${tsv_dir}/${sample}_MAPQ20.sam ${tsv_dir}

### In the end you will get a txt file with two kinds of mutation tags. Each line contains: readID cellbarcode UMI gene--C--A
### The file format is "${sample}_MAPQ20_TC_GA.txt"

