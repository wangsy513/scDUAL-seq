#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pysam
import sys
import os
import time


name = str(sys.argv[1])
samplename = name.split('.')[0]
mname = f'{samplename}_filter.sam'
folder_path = sys.argv[2]

sam = {}
TCmutation_ID = set()
GAmutation_ID = set()
sam_part1 = {}
sam_part2 = {}
output = {}


# get a dict including reads info: qname [cell_barcode, umi, gene]
with open(mname, 'w') as filtered_sam:
    with open(name, 'r') as original_sam:
        for line in original_sam:
            if line.startswith('@SQ') or line.startswith('@RG') or line.startswith('@PG') or 'GE:' in line:
                filtered_sam.write(line)

samfile = pysam.AlignmentFile(mname)
for r in samfile:
    qname = r.query_name
    tags = r.get_tags()
    tag_dict = {tag[0]: tag[1] for tag in tags if tag[0] in ('XC', 'XM', 'GE')}
    l = [tag_dict.get(tag) for tag in ('XC', 'XM', 'GE')]
    sam[qname] = l
samfile.close()

print("first record of sam:", next(iter(sam.items())))
print("nrow of sam:", len(sam))

# get all file names ending with corrected.tsv in folder_path and write them to the input.txt file
def find_and_write_files(folder_path, input_file):
    with open(input_file, 'w') as output:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith("corrected.tsv"):
                    file_path = os.path.join(root, file)
                    output.write(file_path + '\n')

input_file = 'input.txt'
find_and_write_files(folder_path, input_file)

# Extract two kinds of read ID with mutation and remove duplication
start_time = time.time()
with open(input_file, 'r') as file_list:
    for tsvfile in file_list:
        tsvfile = tsvfile.strip()
        filename = os.path.basename(tsvfile).split('.')[0]
        mutation_type = filename.split('_')[-1]  # mutation type: 'TC' or 'GA'
        
        with open(tsvfile, 'r') as deal_file:
            for line in deal_file:
                mutation = line.rstrip().split('\t')[0]
                if mutation_type == 'TC':
                    TCmutation_ID.add(mutation)
                elif mutation_type == 'GA':
                    GAmutation_ID.add(mutation)
end_time = time.time()
consume_time = (end_time - start_time) / 60
print('Divide two kinds of mutation:', consume_time)


# divide two kinds sam file
start_time = time.time()
mutation_ID = TCmutation_ID.union(GAmutation_ID)

for read in mutation_ID:
    if read in sam:
        cell_barcode, umi, gene = map(str, sam[read])
        sam_part1[read] = [cell_barcode, umi, gene]
        del sam[read]
print("nrow of sam:", len(sam_part1))

sam_part2 = sam
print("nrow of sam:", len(sam_part2))

end_time = time.time()
consume_time = (end_time - start_time) / 60
print('Divide two kinds of SAM file:', consume_time)

# determine two types of mutations
start_time = time.time()
for qname, values in sam_part1.items():
    cell_barcode, umi, gene = values
    gene += '--C' if qname in TCmutation_ID else '--N'
    gene += '--A' if qname in GAmutation_ID else '--N'
    output[qname] = [cell_barcode, umi, gene]

for qname, values in sam_part2.items():
    cell_barcode, umi, gene = values
    gene += '--N--N'
    output[qname] = [cell_barcode, umi, gene]

end_time = time.time()
consume_time = (end_time - start_time) / 60
print('Sort mutation:', consume_time)


# output file
outputname = os.path.join(folder_path, f'{samplename}_TC_GA.txt')
with open(outputname, 'w') as OUT:
    for k, v in output.items():
        OUT.write(f'{k}\t{v[0]}\t{v[1]}\t{v[2]}\n')

print('Done')
