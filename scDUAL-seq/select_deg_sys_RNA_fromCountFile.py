#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
I1:SM_gene_cell_UMI_count.txt
O1:SM_gene_cell_UMI_count_deg.txt
O2:SM_gene_cell_UMI_count_sys.txt
"""

import sys
import os
import argparse
import re
from collections import defaultdict

my_parse = argparse.ArgumentParser(description='rate of three type marks for specific gene')
my_parse.add_argument('-p1', '--PATH1', type = str, required = True,
                      help = 'the directory for raw_count.txt ') #eg, path/to/you
my_parse.add_argument('-p2', '--PATH2', type = str, required = True,
                      help = 'the directory where the save file in ') #eg, path/to/you
my_parse.add_argument('-s', '--SAMPLE', type = str, nargs='+', required=True, 
                      help='input the sample name')

args = my_parse.parse_args()

os.chdir('%s' % args.PATH2)


def selecet_newRNA():
    sample_list = args.SAMPLE
    infile1_list = []
    outfile1_list = []
    file_count = 0
    for filename in sample_list:
        filename = filename.rstrip()
        infile1 = str('%s'%args.PATH1)+'/'+str(filename)+'/'+'Step2'+'/'+str(filename)+'_gene_cell_UMI_count.txt'
        outfile1 = str(filename)+'_gene_cell_UMI_count_sys.txt'
        infile1_list.append(infile1)
        outfile1_list.append(outfile1)
    for infile1 in infile1_list:
        newRNA = []
        file_count += 1
        infile1 = infile1.rstrip()
        with open(infile1, 'r') as if1:
            for line in if1:
                line = line.rstrip()
                pattern1 = re.compile('--C--[AN]\s')
                flag1 = re.search(pattern1, line)
                if flag1:
                    newRNA.append(line)
            print(str(sample_list[file_count - 1]) + '_the_newRNA_count:' + str(len(newRNA)), flush=True)
        outfileName = outfile1_list[file_count-1]
        with open(outfileName, 'w') as of1:
            for line in newRNA:
                line = line.rstrip()
                of1.write(str(line)+'\n')

def selecet_oldRNA():
    sample_list = args.SAMPLE
    infile1_list = []
    outfile1_list = []
    file_count = 0
    for filename in sample_list:
        filename = filename.rstrip()
        infile1 = str('%s'%args.PATH1)+'/'+str(filename)+'/'+'Step2'+'/'+str(filename)+'_gene_cell_UMI_count.txt'
        outfile1 = str(filename)+'_gene_cell_UMI_count_deg.txt'
        infile1_list.append(infile1)
        outfile1_list.append(outfile1)
    for infile1 in infile1_list:
        oldRNA = []
        file_count += 1
        infile1 = infile1.rstrip()
        with open(infile1, 'r') as if1:
            for line in if1:
                line = line.rstrip()
                pattern1 = re.compile('--N--A\s')
                flag1 = re.search(pattern1, line)
                if flag1:
                    oldRNA.append(line)
            print(str(sample_list[file_count - 1]) + '_the_oldRNA_count:' + str(len(oldRNA)), flush=True)
        outfileName = outfile1_list[file_count-1]
        with open(outfileName, 'w') as of1:
            for line in oldRNA:
                line = line.rstrip()
                of1.write(str(line)+'\n')


selecet_newRNA()
selecet_oldRNA()
