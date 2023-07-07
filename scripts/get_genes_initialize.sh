#!/bin/bash
hostname

export IFS=""
#read in the file containing the arbitary ID's as first command line input
queryFileName=$1
echo "Checking for presence of isr directory and deleting it if present"
if [ -d gene_trees ]; then
    rm -r gene_trees
fi
mkdir gene_trees
#For each input line

while read queryLine ; do
    gene=$(echo $queryLine | cut -f 1)
    
    if [ ! -d gene_trees/$gene ] ; then
        mkdir gene_trees/$gene
    fi
done < $queryFileName
