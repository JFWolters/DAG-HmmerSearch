#MOVED TO RUN_ME.SH DONT USE

#!/bin/bash
base_dir=$1
sp=

grep ">" $sp.protein_hits.filtered.fasta  > seq_headers.txt


if [ -f score_table.tab ] ; then
    rm score_table.tab
fi
while read seq_header ; do
    seq_desc=$(echo $seq_header | cut -f 2)
    seq_header=$(echo $seq_header | cut -f 1)
    seq_header="${seq_header:1}" #removes the >
    score=$(grep $seq_desc $sp.table.fixed.tab | cut -f 4)
    echo -e "$seq_header\t$score" >> score_table.tab
done < seq_headers.txt

rm seq_headers.txt


