#!/usr/bin/perl

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
    next unless @array >= 2;
    my $index = $array[1];
    $hash{$index}++;
}
close IN;


open(OUT, ">", "${file_bn}_gene_mutation_count.txt") or die "Unable to write to output file: $!\n";
foreach my $index (sort keys %hash) {
    print OUT "$index\t$hash{$index}\n";
}
close OUT;
