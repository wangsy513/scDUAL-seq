#!/usr/bin/env python
# coding=utf-8

# Remove duplicates and retain only uniquely mapped reads for downstream analysis

import os
import argparse

parser = argparse.ArgumentParser(description='Extracting Digital Gene Expression (step1,cell selection finished) (fastq_remove_id_duplication.py, cell_selection.R are needed): \
                                              python DGE1.py \
                                              -p /path/to/picard.jar \
                                              -SM sample_name \
                                              -RG /path/to/REFERENCE_GTF \
                                              -n num/of/barcode')

parser.add_argument('-p', '--picard', type=str,
                    default='/home/disk/dy_student/wsy/softwares/picard/build/libs/picard.jar',
                    help='/path/to/picard.jar')
parser.add_argument('-SM', '--SAMPLE_NAME', type=str, required=True,
                    help='Sample name to insert into the read group header  Required.')
parser.add_argument('-RG', '--REFERENCE_GTF', type=str,
                    default='/home/disk/dy_student/wsy/reference/GRCh38/Homo_sapiens.GRCh38.98.gtf',
                    help='/path/to/REFERENCE_GTF')
parser.add_argument('-DD', '--Drop_seq_pipeline_direction', type=str,
                    default='/home/softwares/Drop-seq_tools-2.4.0/', help='/path/to/drop_seq_pipeline')
parser.add_argument('-T', '--TMP_DIR', type=str, default='./', help='Temporary directory for intermediate files')

args = parser.parse_args()


##SortSam
def SortSam(input, output):
    os.system("java -Xmx4g -jar %s SortSam I=%s O=%s SO=coordinate \
               TMP_DIR=%s" % (args.picard, input, output, args.TMP_DIR))

##RemoveDuplicates
def RemoveDuplicates():
    os.system("java -XX:ParallelGCThreads=2 -jar %s MarkDuplicates \
               I=%s_aligned.sorted.bam \
               O=%s_removeDupl.bam \
               M=%s_removeDuplMetrics.txt \
               REMOVE_DUPLICATES=true \
               TMP_DIR=%s" % (args.picard, args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME, args.TMP_DIR))

##Indexing
def Indexing(filename):
    os.system("samtools index %s" % (filename))

##Annotate
def Annotate():
    os.system("Rscript /home/disk/dy_student/wsy/BULK/scripts/mutation_tag/RsubReadFeatureCounts_bulk.R \
               %s %s_removeDupl.bam %s ." % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.REFERENCE_GTF))


SortSam(input = args.SAMPLE_NAME + "_L2Aligned.out.sam", output = args.SAMPLE_NAME + "_aligned.sorted.bam")
RemoveDuplicates()
Indexing(args.SAMPLE_NAME + "_removeDupl.bam")
Annotate()
SortSam(input = args.SAMPLE_NAME + "_removeDupl.bam.featureCounts.bam", output = args.SAMPLE_NAME + "_remvDupl_featCounts_sorted.bam")
Indexing(args.SAMPLE_NAME + "_remvDupl_featCounts_sorted.bam")







