# Count the number of reads aligned to each genomic feature (exons, genes, etc.) and retain only uniquely mapped reads for downstream analysis.
args <- commandArgs(trailingOnly=TRUE)
library(Rsubread)
samplename <- args[1]
obj <- featureCounts(args[2], annot.ext = args[3], reportReadsPath = args[4],
                     reportReads = 'BAM', isGTFAnnotationFile = TRUE, isPairedEnd = TRUE,
                     requireBothEndsMapped = TRUE, ignoreDup = TRUE, countChimericFragments = FALSE,
                     autosort = TRUE, isSamFile = FALSE)
saveRDS(obj,paste0(args[4],'/',samplename,'_featureCountsOutput.rds'))
