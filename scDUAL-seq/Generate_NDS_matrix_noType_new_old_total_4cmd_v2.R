#Attention:This script does not distinguish between new RNA and old RNA
#usage:Rscript Generate_NDS_matrix_NoType_new_old_total_4cmd_v2.R <sample_gene_cell_UMI_count.txt> <sample_NDS_matrix_cb.txt> <sample_name> <data_type>

args <- commandArgs(T)

require("reshape2")
require("tidyr")
require("dplyr")
require("Matrix")

my.count1 <- read.table(args[1], h = F)
my.count1$gene <- gsub("--[CN]--[AN]", "", as.character(my.count1$V1))


# Filter cells by specified cell number
cells.keep <- my.count1 %>% dplyr::distinct(V2, V3, gene) %>% group_by(V2) %>% summarize(count=n()) %>% arrange(desc(count)) %>% .$V2 %>% as.character 
print("before trim")
print(length(cells.keep))

cells.keep2 <- read.table(args[2], h = F)
cells.keep2 <- cells.keep2$V1
print("post trim")
print(length(cells.keep2))

my.count1 <- my.count1 %>% filter(V2 %in% cells.keep2) %>% droplevels


# check whether there are 5 columns
if (ncol(my.count1) !=5) {
  stop("Error! Please verify the count data frame!\n");
}
my.count2 <- my.count1 %>% arrange(gene, V2, V3)

# count the expression of each gene in each cell
my.count3 <- my.count2 %>% group_by(gene, V2) %>% summarize(count=n())

# convert to rds
my.count3$V2 <- as.factor(my.count3$V2)
my.count3$gene <- as.factor(my.count3$gene)
data.sparse <- sparseMatrix(as.integer(my.count3$gene), as.integer(my.count3$V2), x = my.count3$count)
colnames(data.sparse) <- levels(my.count3$V2)
rownames(data.sparse) <- levels(my.count3$gene)
ord <- sort(colSums(data.sparse), decreasing = T)
data.sparse <- data.sparse[,names(ord)]
dim(data.sparse)

sample_name <- args[3]
data_type <- args[4] #new, old or total
outfile <- paste0(sample_name, '_NDS_matrix_NoType_', data_type, '_', length(cells.keep2), '.rds')
saveRDS(data.sparse, outfile)
