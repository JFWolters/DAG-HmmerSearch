#!/bin/bash

# IFS=""

species=$1
gene=$2
prots=$3
cds_file=$4
score_cutoff=$5
base_dir=$6
source $base_dir/vars.config

$conda init bash
source ~/.bashrc
unset PYTHONPATH


conda activate /mnt/bigdata/linuxhome/jwolters/conda_envs/biopython

$hmmer_path/hmmsearch --tblout $species.table.txt -o $species.hmmer_results.txt -A $species.hmmer_results.aligned.txt -E $evalue $base_dir/$gene.profile.hmm $prots

python $scripts_dir/fix_table.1.py $species.table.txt $species

python $scripts_dir/extract_prots.1.2.py $species.table.fixed.tab $prots $species

python $scripts_dir/extract_CDS.2.py $species.protein_hits.fasta $cds_file

python $scripts_dir/filterHits.1.py $species.protein_hits.fasta $species.CDS.fasta $species.table.fixed.tab $score_cutoff

###Add the species name to the fasta headers

python $scripts_dir/add_species_to_ID.py $species.protein_hits.filtered.fasta $species

python $scripts_dir/add_species_to_ID.py $species.CDS.filtered.fasta $species

####make score table
#may need to make a parallel version for cds?
grep ">" $species.protein_hits.filtered.species_id.fasta  > seq_headers.txt

if [ -f $species.score_table.tab ] ; then
    rm $species.score_table.tab
fi
while read seq_header ; do
    seq_desc=$(echo $seq_header | cut -f 2 -d " ")
    seq_header=$(echo $seq_header | cut -f 1 -d " ")
    seq_header="${seq_header:1}" #removes the >
    score=$(grep "$seq_desc" $species.table.fixed.tab | cut -f 4)
    echo -e "$seq_header\t$score" >> $species.score_table.tab
done < seq_headers.txt

rm seq_headers.txt



####Get Sequence lengths

python $scripts_dir/getSeqSizes.py $species.CDS.filtered.fasta
mv Sequence_sizes.tab $species.CDS.filtered.sequence_sizes.tab
python $scripts_dir/getSeqSizes.py $species.protein_hits.filtered.species_id.fasta
mv Sequence_sizes.tab $species.protein_hits.filtered.species_id.sequence_sizes.tab

conda deactivate


