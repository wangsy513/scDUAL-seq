#!/bin/bash

## Align high-quality reads using STAR (v2.7.3a) and add strandedness tag to the sam file.
## Usage: sh Step3_star_and_annotation.sh fq_dir sample_name

fq_dir=$1 # file folder including repaired sequencing file file
i=$2 # sample names: including chemical treated and untreated samples (control)

star_dir=${fq_dir}/star_out

############ 1. STAR
cd ${fq_dir}
python ~/wsy/BULK/scripts/star_map_ver0.02.py

############ 2. Remove duplicates and retain only uniquely mapped reads for downstream analysis
cd ${star_dir}
python ~/wsy/BULK/scripts/mutation_tag/Gene_Tag_v2.py -SM ${i}

############ 3. Add strandedness tag to the sam file. The strandedness.csv file should be changed when the gtf is changed.
python ~/wsy/BULK/scripts/mutation_tag/add_strand_tag.py ${i} ~/wsy/BULK/scripts/strandedness.csv

