#!/bin/bash

base_dir=$1
source $base_dir/vars.config

IFS=""

while read queryLine ; do
    gene=$(echo $queryLine | cut -f 1)
    echo $gene
    alignment=$(echo $queryLine | cut -f 2)
    echo $alignment
    $hmmer_path/hmmbuild $gene.profile.hmm $alignment
done < $queryFileName
