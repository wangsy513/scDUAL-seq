import os
import re

## Unzip the file and ulitize fastqc to quality control the file.
## Pre-install requirment: FastQC
## Usage: python raw_fastqc.py

os.system("mkdir fastqc_result")

os.system("ls *.gz > list_seq.txt")

file=open('list_seq.txt','r')
for i in file:
    gz=re.sub('\n','',i)
    os.system("gunzip %s" % (gz))
    print(f"{gz} complete")
    fq = gz.replace('.gz', '')
    os.system("fastqc -o ./fastqc_result -t 5 %s" %(fq))
    print(f"Quality analysis for {fq} complete")
file.close()
os.system("rm list_seq.txt")
