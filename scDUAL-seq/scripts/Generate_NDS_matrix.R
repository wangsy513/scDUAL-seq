# usage: Rscript /home/disk/dy_student/wsy/WPS/scripts/Generate_mutation_matrix.R output_of_perl_script $num_core_barcode final_matrix.rds

args <- commandArgs(T)

require("reshape2")
require("tidyr")
require("dplyr")
require("Matrix")

my.count1 <- read.table(args[1], header = FALSE, stringsAsFactors = FALSE)

my.count1$gene <- gsub("--[CN]--[AN]", "", as.character(my.count1$V1))
cells.keep <- my.count1 %>% dplyr::distinct(V2, V3, gene) %>% group_by(V2) %>% summarize(count=n()) %>% arrange(desc(count)) %>% .$V2 %>% as.character 

print("before trim")
print(length(cells.keep))
inds <- as.numeric(args[2])
if (length(cells.keep) > inds) {
    cells.keep2 <- head(cells.keep, inds)
} else {
    cells.keep2 <- cells.keep
}
print("post trim")
print(length(cells.keep2))

my.count1 <- my.count1 %>% filter(V2 %in% cells.keep2) %>% droplevels
my.count1$type <- "N"
my.count1[grep("--N--A", my.count1$V1),]$type <- "D"
my.count1[grep("--C--[AN]", my.count1$V1),]$type <- "S"


# When gene + V2 + V3 and type are the same, the sum of V4 will be calculated, and the counts of "--C--[AN]" can be combined.
my.count2 <- dcast(my.count1, gene + V2 + V3 ~ type, value.var = "V4", fun.aggregate = sum, fill = 0)
# check whether there are 6 columns
if (ncol(my.count2) !=6) {
    stop("Error! Please verify the count data frame!\n");
}
my.count2 <- my.count2 %>% arrange(gene, V2, V3, S, D, N)
# Determine the type of umi
my.count2 <- my.count2 %>% mutate(
    type = case_when(
        S > 0 ~ "S",
        D > 0 ~ "D",
        N > 0 ~ "N"
    )
) ## this can be modified based on later cut-off


my.count3 <- my.count2 %>% group_by(gene, type, V2) %>% summarize(count = n(), .groups = 'drop')
my.count3$gene2 <- paste(my.count3$gene, my.count3$type, sep = "--")
my.count3$V2 <- as.factor(my.count3$V2)
my.count3$gene2 <- as.factor(my.count3$gene2)
data.sparse <- sparseMatrix(
  i = as.integer(my.count3$gene2),
  j = as.integer(my.count3$V2),
  x = my.count3$count
)
colnames(data.sparse) <- levels(my.count3$V2)
rownames(data.sparse) <- levels(my.count3$gene2)
ord <- sort(colSums(data.sparse), decreasing = TRUE)
data.sparse <- data.sparse[, names(ord)]

saveRDS(data.sparse, file = args[3])

