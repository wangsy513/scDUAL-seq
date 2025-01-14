#!/bin/bash

## Pre-install requirment: perl, Rscript

txt_dir=$1 # txt file folder including txt file which was generated in step3
sample=$2 # sample name to deal with, which has been chemically treated
num_core_barcode=$3 # number of cells to contain

############ 1. Count mutation
cd ${txt_dir}
perl /home/disk/dy_student/wsy/WPS/scripts/extract_digital_expression_matrix_v2.pl ${sample}_MAPQ20_TC_GA.txt

############ 2. Generate NDS matrix with rds format
Rscript  /home/disk/dy_student/wsy/WPS/scripts/Generate_NDS_matrix.R ${sample}_gene_cell_UMI_count.txt ${num_core_barcode} ${sample}_NDS_matrix.rds

### In the end you will get a rds file: ${sample}_NDS_matrix.rds
