#!/bin/bash


gene=$1
base_dir=$2

source $base_dir/vars.config

$clustalo -i $gene.prot.fasta -o $gene.prot.aligned.fasta

$trimal -in $gene.prot.aligned.fasta -out $gene.prot.aligned.trimmed.fasta -fasta -gappyout

outFileName=$gene.prot.aligned.trimmed.fasttree
$fasttree -lg -gamma -spr 4 -slownni -mlacc 2 -out $outFileName $gene.prot.aligned.trimmed.fasta

cat $itol_header > $gene.scores.iTOL.txt
cat $gene.score_table.tab >> $gene.scores.iTOL.txt
