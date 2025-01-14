# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:56:04 2020

@author: cyclopenta
"""

import sys
import os
import re

source_star_path = '/home/disk/dy_student/wsy/reference/GRCh38/STAR'
gtf_file_path = '/home/disk/dy_student/wsy/reference/GRCh38/Homo_sapiens.GRCh38.98.gtf'

star_out_path = 'star_out'
log_out_path = 'log_final_out'
os.system('''  mkdir -p ./{path1}/{path2}'''.format(path1 = star_out_path,path2 = log_out_path))

os.system(' ls *_1_repair_1.fq > clean_file_star_temp.txt')

raw_file = open ('clean_file_star_temp.txt')
for f1 in raw_file:
    f1 = f1.rstrip()
    f2 = re.sub('_1_repair_1.fq','_2_repair_2.fq',f1)
    r1 = f1.split('.')[0]
    r2 = f2.split('.')[0]
    out_prefix = re.sub('_1_repair_1.fq','',f1)
    print('now processing: %s and %s'%(r1,r2))
    os.system('''
STAR --runThreadN 10 --genomeDir {starpath} --outFileNamePrefix {prefix} --sjdbGTFfile {gtf} --outSAMunmapped Within --readFilesIn {read1}.fq {read2}.fq;
mv {prefix}Log.final.out ./{path1}/{path2};
mv {prefix}Aligned.out.sam {prefix}Log.out {prefix}Log.progress.out {prefix}SJ.out.tab {prefix}_STARgenome ./{path1};
'''.format(starpath = source_star_path,read1 = r1,read2 = r2,prefix = out_prefix,gtf = gtf_file_path,path1 = star_out_path,path2 = log_out_path)) 
raw_file.close()

os.system('''rm clean_file_star_temp.txt''')

print('star map done!!!')
