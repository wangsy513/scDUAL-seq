#!/usr/bin/perl

# This version is suitable for the subsequent processing of step3_v2.

use strict;
use warnings;
use File::Basename;

my $in = shift @ARGV;
my %hash;

my $bn = basename($in);

# extract sample name
my $file_bn;
if ($bn =~ /(.*)\_MAPQ20_TC_GA.txt$/) {
    $file_bn = $1;
} else {
    die "Filename $bn does not match the expected pattern\n";
}


open(IN, "<", "$in") or die "Unable to read from file $in: $!\n";
while (<IN>) {
    chomp;
    my @array = split "\t";
    next unless @array >= 4;
    my $cell_barcode = $array[1];
    my $umi = $array[2];
    my $gene = $array[3];
    my $index = join "\t", ($gene, $cell_barcode, $umi);
    $hash{$index}++;
}
close IN;


open(OUT, ">", "${file_bn}_gene_cell_UMI_count.txt") or die "Unable to write to output file: $!\n";
foreach my $index (keys %hash) {
    print OUT "$index\t$hash{$index}\n";
}
close OUT;
