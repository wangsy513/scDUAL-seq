#!/bin/bash

## Count gene mutations.
## Usage: sh Step6_mutation_count.sh csv_dir sample_name

csv_dir=$1 # file folder including the corrected csv file
i=$2 # sample name with chemical treatment

############ 1. Add TC/GA mutation tags to the gene and readID.
cd ${csv_dir}
python ~/wsy/BULK/scripts/mutation_tag/extract_mutation.py ${i}_MAPQ20.sam ${csv_dir}

############ 2. Statistics of gene mutations based on the _MAPQ20_TC_GA.txt file generated in the previous step.
perl ~/wsy/BULK/scripts/mutation_tag/count_gene_mutations.pl ${i}_MAPQ20_TC_GA.txt
