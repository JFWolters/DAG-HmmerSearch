#!/bin/bash
hostname
# inFileName=/mnt/bigdata/linuxhome/jwolters/katharina_busco_tree/20210715/genomes.tab
base_dir=$1
gene=$2
IFS=""

source $base_dir/vars.config

/opt/bifxapps/miniconda3/condabin/conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate /home/glbrc.org/jwolters/conda_envs/biopython

if [ -f $gene.prot.fasta ] ; then
    rm $gene.prot.fasta
fi
if [ -f $gene.cds.fasta ] ; then
    rm $gene.cds.fasta
fi
if [ -f $gene.score_table.tab ] ; then
    rm $gene.score_table.tab
fi
if [ -f $gene.CDS.sizes.tab ] ; then
    rm $gene.CDS.sizes.tab
fi
if [ -f $gene.protein_hits.sizes.tab ] ; then
    rm $gene.protein_hits.sizes.tab
fi
IFS=""

###prepre gene lengths files
echo -e "Species\tHit\tSize" > $gene.CDS.sizes.tab
echo -e "Species\tHit\tSize" > $gene.protein_hits.sizes.tab


###copy over relevant info from individual species results
while read line ; do
    species=$(echo $line | cut -f 1)
    if [ -s $base_dir/isr/$gene/$species/$species.protein_hits.filtered.fasta ] ; then
        
        
        cat $base_dir/isr/$gene/$species/$species.protein_hits.filtered.species_id.fasta >> $gene.prot.fasta
        
        # cp ../../isr/$gene/$species/$species.CDS.filtered.fasta temp.cds.fasta
        # python $scripts_dir/add_species_to_ID.py temp.cds.fasta $species
        cat $base_dir/isr/$gene/$species/$species.CDS.filtered.species_id.fasta >> $gene.cds.fasta
        
                
        # rm temp*
        
        cat $base_dir/isr/$gene/$species/$species.score_table.tab >> $gene.score_table.tab
        
        tail -n +2 $base_dir/isr/$gene/$species/$species.CDS.filtered.sequence_sizes.tab > temp
        while read size_line ; do
            echo -e "$species\t$size_line" >> $gene.CDS.sizes.tab
        done < temp
        tail -n +2 $base_dir/isr/$gene/$species/$species.protein_hits.filtered.species_id.sequence_sizes.tab > temp
        while read size_line ; do
            echo -e "$species\t$size_line" >> $gene.protein_hits.sizes.tab
        done < temp
        rm temp 
    else
        echo "Missing $gene for $species"
    fi
done < $subjectFileName


conda deactivate

####Make histogram of scores
unset R_LIBS
unset R_LIBS_USER
conda activate /mnt/bigdata/linuxhome/jwolters/conda_envs/R_env

Rscript $scripts_dir/make_score_histogram.R $gene.score_table.tab

conda deactivate

####Count number of hits


outFileName=$gene.hit_counts.txt
rm $outFileName
echo -e "Species\tUnfiltered\tFiltered" > $outFileName

while read line ; do
    sp=$(echo $line | cut -f 1)
    unfiltered_count=$(grep ">" $base_dir/isr/$gene/$sp/$sp.protein_hits.fasta | wc -l)
    filtered_count=$(grep ">" $base_dir/isr/$gene/$sp/$sp.protein_hits.filtered.fasta | wc -l)

    echo -e "$sp\t$unfiltered_count\t$filtered_count" >> $outFileName
done < $subjectFileName



###Generate gene count file for itol
cp /mnt/bigdata/linuxhome/jwolters/hmmer_pipelines/v10.1/gene_count_iTOL_header.txt $gene.gene_count_iTOL.txt
tail -n +2 $gene.hit_counts.txt | cut -f 1,3 >> $gene.gene_count_iTOL.txt

sed -i "s/GENENAME/$gene/g" $gene.gene_count_iTOL.txt

