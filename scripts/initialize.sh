#!/bin/bash
hostname

export IFS=""
#read in the file containing the arbitary ID's as first command line input
subjectFileName=$1
queryFileName=$2
echo "Checking for presence of isr directory and deleting it if present"
if [ -d isr ]; then
    rm -r isr
fi
mkdir isr
#For each input line

while read queryLine ; do
    gene=$(echo $queryLine | cut -f 1)
    
    if [ ! -d isr/$gene ] ; then
        mkdir isr/$gene
    fi
    while read subjectLine ; do
        #Extract the arbitrary ID
        sp=$(echo $subjectLine | cut -f 1 )
        #make the directory to hold the results for that individual input data
        if [ ! -d isr/$gene/$sp ] ; then
            mkdir isr/$gene/$sp
        fi
        
    done < $subjectFileName
done < $queryFileName
