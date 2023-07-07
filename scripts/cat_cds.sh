#########DONT USE!!!!!!!!!
base_dir=$1
gene=$2
source $base_dir/vars.config

IFS=""

outFileName=$gene.prots.fasta

while read line ; do
    sp=$(echo $line | cut -f 1)
    if [ -f $base_dir/isr/$sp/$sp.protein_hits.filtered.fasta ] ; then
        
        
    
done < $subjectFileName
