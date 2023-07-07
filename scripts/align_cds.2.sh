#!/bin/bash

# geneFileName=/mnt/bigdata/linuxhome/jwolters/katharina_busco_tree/20201006/all_species_complete_genes.txt
gene=$1
clustalo=/home/GLBRCORG/jwolters/packages/bin/clustalo-1.2.4-Ubuntu-x86_64
trimal=/home/GLBRCORG/jwolters/packages/trimal/source/trimal
fasttree=/home/glbrc.org/jwolters/packages/FastTree/FastTree
# echo $gene
# cd $gene
$clustalo -i $gene.prot.fasta -o $gene.prot.aligned.fasta

$trimal -in $gene.prot.aligned.fasta -out $gene.prot.aligned.trimmed.fasta -fasta -gappyout

outFileName=$gene.prot.aligned.trimmed.fasttree
$fasttree -lg -gamma -spr 4 -slownni -mlacc 2 -out $outFileName $gene.prot.aligned.trimmed.fasta

cat /mnt/bigdata/linuxhome/jwolters/hmmer_pipelines/v10/scripts/itol_header.txt > $gene.scores.iTOL.txt
cat $gene.score_table.tab >> $gene.scores.iTOL.txt
