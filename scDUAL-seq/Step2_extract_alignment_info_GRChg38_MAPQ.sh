#!/bin/bash

## This script ulitizes sam2tsv (https://github.com/lindenb/jvarkit/; version ec2c2364) to extract aligment details from bam files and then T->C and G->A mutations were identified in both with and without Dual TimeLapse chemistry treatment (served as control) libraries.
## Pre-install requirment: sam2tsv, samtools, perl
## Usage: sh Step2_extract_alignment_info_GRChg38_MAPQ.sh bam_dir sample_name

bam_dir=$1 # bam file folder including bam file which was generated in step1
i=$2 # sample names: including chemical treated and untreated samples (control)
genome_fa='/home/disk/dy_student/wsy/reference/GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly.fa' # genome fasta file (mm10 or hg38)

analysis_dir=${bam_dir}/Step2
mkdir -p ${analysis_dir}

output_dir=${analysis_dir} 

TMP_dir=${analysis_dir}/tmp/
mkdir -p ${TMP_dir}


############ 0. check the avalibality of bam file
bam_file_prex=${i}_star_gene_exon_tagged_TagIntronic_clean

if [ ! -f ${bam_dir}/${bam_file_prex}.bam ]; then
   echo "Please verify that bam file ${bam_dir}/${bam_file_prex}.bam exists!"
   exit
fi

############ 1. bam to sam
samtools view -@ 10 -h ${bam_dir}/${bam_file_prex}.bam > ${output_dir}/${i}.sam

############ 2. filter MAPQ > 20
cd ${output_dir}
samtools view -S -h -q 20 ${i}.sam > ${i}_MAPQ20.sam

############ 3. extract read ID with GE:Z annotation (get read ID with gene annotation)
grep "GE:Z" ${i}_MAPQ20.sam | awk '{print $1}' >  ${i}_ann_read.txt

############ 4. sam to tsv by sam2tsv 
sam2tsv --reference ${genome_fa} ${i}_MAPQ20.sam | awk '{if ($9 ~/M|=|X/ ) print $0}'  > ${i}_both_strand_all.tsv

############ 5. Extract G->A mutation and T->C mutation from _all.tsv considering both strands
awk -v i="${i}" '{if ($2==0 && $5=="C" && $8=="T") {print $0 > i "_both_strand_all_TC.tsv"} \
else if ($2==16 && $5=="G" && $8=="A") {print $0 > i "_both_strand_all_TC.tsv"} \
else if ($2==0 && $5=="A" && $8=="G") {print $0 > i "_both_strand_all_GA.tsv"} \
else if ($2==16 && $5=="T" && $8=="C") {print $0 > i "_both_strand_all_GA.tsv"}}' "${i}_both_strand_all.tsv"

############ 6. Retain T-to-C substitutions with a base Phred quality score of > 27 分别质控
perl /home/disk/dy_student/wsy/WPS/scripts/extrac_refT_readC.pl -tsv ${i}_both_strand_all_GA.tsv -qual 27 
perl /home/disk/dy_student/wsy/WPS/scripts/extrac_refT_readC.pl -tsv ${i}_both_strand_all_TC.tsv -qual 27

############ 7. QC output: summarise the all types of mutation rate
perl /home/disk/dy_student/wsy/WPS/scripts/extrac_conversion_frequency_gene_annotate.pl -read ${i}_ann_read.txt -tsv ${i}_both_strand_all.tsv -qual 27




