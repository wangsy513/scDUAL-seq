#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pysam
import pandas as pd
import sys
import os
import time
from collections import defaultdict


name = sys.argv[1]
samplename = name.split('.')[0]
folder_path = sys.argv[2]


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


sam = {}
TCmutation_ID = {}
GAmutation_ID = {}


# get a dict including reads info: qname [readID gene]
samfile = pysam.AlignmentFile(name)
for r in samfile:
    qname = r.query_name
    tags = r.get_tags()
    for tag in tags:
        if tag[0] == 'XT':
            sam[qname] = [tag[1]]
samfile.close()


# Extract two kinds of read ID with mutation and remove duplication
start_time = time.time()
with open(input_file, 'r') as file_list:
    for tsvfile in file_list:
        tsvfile = tsvfile.strip()
        filename = os.path.basename(tsvfile).split('.')[0]
        type = filename.split('_')[-1] # mutation type: 'TC' or 'GA'
        
        with open(tsvfile, 'r') as deal_file:
            if type == 'TC':
                for line in deal_file:
                    line = line.rstrip()
                    mutation = line.split('\t')
                    TCmutation_ID[mutation[0]] = None
            elif type == 'GA':
                for line in deal_file:
                    line = line.rstrip()
                    mutation = line.split('\t')
                    GAmutation_ID[mutation[0]] = None              
end_time = time.time()
consume_time = (end_time - start_time) / 60
print('divide two kinds of mutation:', consume_time)


# divide two kinds sam file
start_time = time.time()

mutation_ID = {**TCmutation_ID, **GAmutation_ID}
readID = list(mutation_ID.keys())

sam_part1 = {read: sam.pop(read) for read in readID if read in sam}
sam_part2 = sam

end_time = time.time()
consume_time = (end_time - start_time) / 60
print('divide two kinds sam file:', consume_time)


start_time = time.time()

output = {}
for qname in sam_part1.keys():
    gene = sam_part1[qname][0]
    gene += '--C' if qname in TCmutation_ID else '--N'
    gene += '--A' if qname in GAmutation_ID else '--N'
    output[qname] = [gene]

for qname, gene in sam_part2.items():
    gene = gene[0] + '--N--N'
    output[qname] = [gene]

end_time = time.time()
consume_time = (end_time - start_time) / 60
print('sort mutation:', consume_time)


outputname = os.path.join(folder_path, f'{samplename}_TC_GA.txt')
with open(outputname, 'w') as OUT:
    for k, v in output.items():
        str_write = k + '\t' + v[0] + '\n'
        OUT.write(str_write)

print('Done')

