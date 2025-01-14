#!/usr/bin/env python
# coding=utf-8

import pysam
import pandas as pd
import sys

def addTags(bamfilename, outputname, strandednessfile):
    bamfile = pysam.AlignmentFile(bamfilename, 'rb')
    mod_bamfile = pysam.AlignmentFile(outputname, mode='wb',template=bamfile)
    strandedness = pd.read_csv(strandednessfile, header=None, index_col=0)
    for read in bamfile.fetch():
        try:
            read.set_tag('ST',strandedness.loc[read.get_tag('XT')][1])
            mod_bamfile.write(read)
        except (ValueError,KeyError):
            continue
    print('Wrote tags to {}'.format(outputname))


if __name__ == "__main__":
    ifile = sys.argv[1] + "_remvDupl_featCounts_sorted.bam"
    outdir = sys.argv[1] + "_remvDupl_featCounts_sorted_strandtag.bam"
    strandednessfile = sys.argv[2]
    addTags(ifile, outdir, strandednessfile)

