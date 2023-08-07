makeDAG_path=/path/to/main_pipeline_directory

#fix your pythonpath to include pydagman
export PYTHONPATH=$PYTHONPATH:/mnt/bigdata/linuxhome/jwolters/packages

python=/path/to/python2.7
#for use on scarcity, you can use/opt/bifxapps/python/bin/python2.7 
$python $makeDAG_path/makeDAG.py

$python /opt/bifxapps/python/bin/python2.7 $makeDAG_path/cds_align.makeDAG.py

$python /opt/bifxapps/python/bin/python2.7 $makeDAG_path/get_genes.makeDAG.py
