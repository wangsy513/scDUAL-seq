#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pysam
import pandas as pd

samplename = sys.argv[1]
samfilename = samplename + '_MAPQ20.sam'
csvfilename = samplename + '_ann_read_with_ST.csv'

# extract ReadID and corresponding ST tags information
reads_with_ST = {}
with pysam.AlignmentFile(samfilename, 'r') as samfile:
    for read in samfile.fetch():
        read_ID = read.qname
        ST_tag = read.get_tag('ST')
        reads_with_ST[read_ID] = ST_tag
df = pd.DataFrame(list(reads_with_ST.items()))
df.to_csv(csvfilename, index=False, header=False)
print(f'ReadID and corresponding ST tags written to {csvfilename}')

