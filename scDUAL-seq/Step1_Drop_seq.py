#!/usr/bin/env python
# coding=utf-8

import os
import argparse

parser = argparse.ArgumentParser(description='Extracting Digital Gene Expression (step1,cell selection finished) (fastq_remove_id_duplication.py, cell_selection.R are needed): \
                                              python DGE1.py \
                                              -p /path/to/picard.jar \
                                              -F1 fastq_file \
                                              -F2 fastq_file \
                                              -SM sample_name \
                                              -SR /path/to/STAR_REFERENCE \
                                              -RF /path/to/REFERENCE_FASTQ \
                                              -RG /path/to/REFERENCE_GTF \
                                              -n num/of/barcode')

parser.add_argument('-p', '--picard', type=str,
                    default='/home/disk/dy_student/wsy/softwares/picard/build/libs/picard.jar',
                    help='/path/to/picard.jar')
parser.add_argument('-F1', '--FASTQ1', type=str, required=True,
                    help='Input fastq file (optionally gzipped) for single end data, or first read in paired end')
parser.add_argument('-F2', '--FASTQ2', type=str,
                    help='Input fastq file (optionally gzipped) for the second read of paired end data. Default value: null.')
parser.add_argument('-SM', '--SAMPLE_NAME', type=str, required=True,
                    help='Sample name to insert into the read group header  Required.')
parser.add_argument('-SR', '--STAR_REFERENCE', type=str, default='/home/disk/dy_student/wsy/reference/GRCh38/STAR',
                    help='/path/to/STAR_REFERENCE')
parser.add_argument('-RF', '--REFERENCE_FASTQ', type=str, default='/home/disk/dy_student/wsy/reference/GRCh38/Homo_sapiens.GRCh38.dna.primary_assembly.fa',
                    help='/path/to/REFERENCE_FASTQ')
parser.add_argument('-RG', '--REFERENCE_GTF', type=str,
                    default='/home/disk/dy_student/wsy/reference/GRCh38/Homo_sapiens.GRCh38.98.gtf',
                    help='/path/to/REFERENCE_GTF')
parser.add_argument('-DD', '--Drop_seq_pipeline_direction', type=str,
                    default='/home/softwares/Drop-seq_tools-2.4.0/', help='/path/to/drop_seq_pipeline')

args = parser.parse_args()


##FastqToSam docu
def FastqToSamTag():
    if args.FASTQ2:
        if args.FASTQ1.split('.')[-1] == 'gz':
            os.system("gunzip %s" % (args.FASTQ1))
            F1_raw = args.FASTQ1.replace('.gz', '')
        else:
            F1_raw = args.FASTQ1
        if args.FASTQ2.split('.')[-1] == 'gz':
            os.system("gunzip %s" % (args.FASTQ2))
            F2_raw = args.FASTQ2.replace('.gz', '')
        else:
            F2_raw = args.FASTQ2
        os.system("python /home/disk/dy_student/wsy/WPS/scripts/fastq_remove_id_duplication.py -F1 %s -F2 %s" % (F1_raw, F2_raw))
        F1 = F1_raw.split('/')[-1].split('.')[0] + '_remove_id_duplication.' + F1_raw.split('/')[-1].split('.')[-1]
        F2 = F2_raw.split('/')[-1].split('.')[0] + '_remove_id_duplication.' + F2_raw.split('/')[-1].split('.')[-1]
        os.system("java -jar %s FastqToSam \
                   F1=%s \
                   F2=%s \
                   O=%s_unaligned_read_pairs.bam \
                   SM=%s \
                   TMP_DIR=./" % (args.picard, F1, F2, args.SAMPLE_NAME, args.SAMPLE_NAME))

        ##TagBamWithReadSequenceExtended
        ##Cell Barcode
        os.system("/home/softwares/Drop-seq_tools-2.4.0/TagBamWithReadSequenceExtended \
                   INPUT=%s_unaligned_read_pairs.bam \
                   OUTPUT=%s_unaligned_tagged_Cell.bam \
                   SUMMARY=%s_unaligned_tagged_Cellular.bam_summary.txt \
                   BASE_RANGE=26-37 \
                   BASE_QUALITY=10 \
                   BARCODED_READ=1 \
                   DISCARD_READ=False \
                   TAG_NAME=XC \
                   NUM_BASES_BELOW_QUALITY=1" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))

    else:
        if args.FASTQ1.split('.')[-1] == 'gz':
            os.system("gunzip %s" % (args.FASTQ1))
            F1_raw = args.FASTQ1.replace('.gz', '')
        else:
            F1_raw = args.FASTQ1
        os.system("python /home/disk/dy_student/wsy/WPS/scripts/fastq_remove_id_duplication.py -F1 %s" % (F1_raw))
        F1 = F1_raw.split('/')[-1].split('.')[0] + '_remove_id_duplication.' + F1_raw.split('/')[-1].split('.')[-1]
        os.system("java -jar %s FastqToSam \
                   F1=%s \
                   O=%s_unaligned_read.bam \
                   SM=%s \
                   TMP_DIR=./" % (args.picard, F1, args.SAMPLE_NAME, args.SAMPLE_NAME))

        ##TagBamWithReadSequenceExtended
        ##Cell Barcode
        os.system("/home/softwares/Drop-seq_tools-2.4.0/TagBamWithReadSequenceExtended \
                   INPUT=%s_unaligned_read.bam \
                   OUTPUT=unaligned_tagged_Cell.bam \
                   SUMMARY=unaligned_tagged_Cellular.bam_summary.txt \
                   BASE_RANGE=26-37 \
                   BASE_QUALITY=10 \
                   BARCODED_READ=1 \
                   DISCARD_READ=False \
                   TAG_NAME=XC \
                   NUM_BASES_BELOW_QUALITY=1" % (args.SAMPLE_NAME))


##Molecular Barcode
def TagMolecularBarcode():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/TagBamWithReadSequenceExtended \
               INPUT=%s_unaligned_tagged_Cell.bam \
               OUTPUT=%s_unaligned_tagged_CellMolecular.bam \
               SUMMARY=%s_unaligned_tagged_Molecular.bam_summary.txt \
               BASE_RANGE=38-45 \
               BASE_QUALITY=10 \
               BARCODED_READ=1 \
               DISCARD_READ=True \
               TAG_NAME=XM \
               NUM_BASES_BELOW_QUALITY=1" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))


##FilterBam
def FilterBam():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/FilterBam \
               TAG_REJECT=XQ \
               INPUT=%s_unaligned_tagged_CellMolecular.bam \
               OUTPUT=%s_unaligned_tagged_filtered.bam " % (args.SAMPLE_NAME, args.SAMPLE_NAME))


##TrimStartingSequence
def TrimStartingSequence():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/TrimStartingSequence \
               INPUT=%s_unaligned_tagged_filtered.bam \
               OUTPUT=%s_unaligned_tagged_trimmed_smart.bam \
               OUTPUT_SUMMARY=%s_adapter_trimming_report.txt \
               SEQUENCE=AAGCAGTGGTATCAACGCAGAGTGAATGGG \
               MISMATCHES=0 \
               NUM_BASES=5" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))


##PolyATrimmer
def PolyATrimmer():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/PolyATrimmer \
               INPUT=%s_unaligned_tagged_trimmed_smart.bam \
               OUTPUT=%s_unaligned_mc_tagged_polyA_filtered.bam \
               OUTPUT_SUMMARY=%s_polyA_trimming_report.txt \
               MISMATCHES=0 \
               NUM_BASES=6 \
               USE_NEW_TRIMMER=true" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))


##SamToFastq
def SamToFastq():
    os.system("java -Xmx4g -jar %s SamToFastq \
               INPUT=%s_unaligned_mc_tagged_polyA_filtered.bam \
               FASTQ=%s_unaligned_mc_tagged_polyA_filtered.fastq \
               TMP_DIR=./" % (args.picard, args.SAMPLE_NAME, args.SAMPLE_NAME))


##Alignment
##STAR
def STAR():
    os.system("/home/softwares/STAR-2.7.3a/bin/Linux_x86_64/STAR \
               --genomeDir %s \
               --readFilesIn %s_unaligned_mc_tagged_polyA_filtered.fastq \
               --outFileNamePrefix %s_star \
               --limitOutSJcollapsed 5000000" % (args.STAR_REFERENCE, args.SAMPLE_NAME, args.SAMPLE_NAME))


##SortSam
def SortSam():
    os.system("java -Xmx4g -jar %s SortSam \
               I=%s_starAligned.out.sam \
               O=%s_aligned.sorted.bam \
               SO=queryname \
               TMP_DIR=./" % (args.picard, args.SAMPLE_NAME, args.SAMPLE_NAME))


##MergeBamAlignment
def MergeBamAlignment():
    os.system("java -Xmx4g -jar %s MergeBamAlignment \
               REFERENCE_SEQUENCE=%s \
               UNMAPPED_BAM=%s_unaligned_mc_tagged_polyA_filtered.bam \
               ALIGNED_BAM=%s_aligned.sorted.bam \
               OUTPUT=%s_merged.bam \
               INCLUDE_SECONDARY_ALIGNMENTS=false \
               PAIRED_RUN=false \
               TMP_DIR=./" % (args.picard, args.REFERENCE_FASTQ, args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))


##TagReadWithGeneExonFunction
def TagReadWithGeneExonFunction():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/TagReadWithGeneExonFunction \
               I=%s_merged.bam \
               O=%s_star_gene_exon_tagged_m.bam \
               ANNOTATIONS_FILE=%s \
               TAG=GE" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.REFERENCE_GTF))


##TagReadWithGeneFunction
def TagReadWithGeneFunction():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/TagReadWithGeneFunction \
               I=%s_star_gene_exon_tagged_m.bam \
               O=%s_star_gene_exon_tagged.bam \
               ANNOTATIONS_FILE=%s" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.REFERENCE_GTF))


##ReterivetheIntronicReadsFunction
def ReterivetheIntronicReadsFunction():
    os.system("perl /home/disk/dy_student/wsy/WPS/scripts/TagIntronicRead_V3.pl -gtf %s -bam %s_star_gene_exon_tagged.bam" % (args.REFERENCE_GTF, args.SAMPLE_NAME))


##DetectAndRepairBarcodeSynthesisErrorFunction
def DetectAndRepairBarcodeSynthesisErrorFunction():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/DetectBeadSynthesisErrors \
               INPUT=%s_star_gene_exon_tagged.TagIntronic.bam \
               O=%s_star_gene_exon_tagged_TagIntronic_clean.bam \
               OUTPUT_STATS=%s_exonic_intronic_synthesis_stats.txt \
               SUMMARY=%s_exonic_intronic_synthesis_stats_summary.txt \
               PRIMER_SEQUENCE=AAGCAGTGGTATCAACGCAGAGTAC \
	           TMP_DIR=%s_tmp" % (args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME, args.SAMPLE_NAME))

##Cell Selection
def CellSelection():
    os.system("/home/softwares/Drop-seq_tools-2.4.0/BamTagHistogram \
               I=%s_star_gene_exon_tagged_TagIntronic_clean.bam \
               O=%s_out_cell_readcounts.txt.gz \
               TAG=XC"%(args.SAMPLE_NAME, args.SAMPLE_NAME))
    os.system('gzip -d %s_out_cell_readcounts.txt.gz'%(args.SAMPLE_NAME))
    os.system("Rscript /home/disk/dy_student/wsy/WPS/scripts/cell_selection_3.R %s_out_cell_readcounts.txt %s" %(args.SAMPLE_NAME, args.SAMPLE_NAME))


FastqToSamTag()
TagMolecularBarcode()
FilterBam()
TrimStartingSequence()
PolyATrimmer()
SamToFastq()
STAR()
SortSam()
MergeBamAlignment()
TagReadWithGeneExonFunction()
TagReadWithGeneFunction()
ReterivetheIntronicReadsFunction()
DetectAndRepairBarcodeSynthesisErrorFunction()
CellSelection()
