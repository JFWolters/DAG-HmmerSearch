from pydagman.dagfile import Dagfile
from pydagman.job import Job
import os
import sys

myDag = Dagfile()

cwd = os.getcwd()

#vars.config must be located in base directory
vars=open("vars.config","r")
vars_lines = vars.readlines()
vars.close()
vars_lines = [line for line in vars_lines if line != "\n"] #remove blank lines
vars_lines = [line for line in vars_lines if not line.startswith("#")] #remove commented lines
vars = [line.split(" ")[1].rstrip("\n") for line in vars_lines]
vars = [line.split("=") for line in vars]
varDict = {}
for var in vars:
    varDict[var[0]]=var[1]

pipeline_dir=varDict["pipeline_dir"]



queryFileName=varDict["queryFileName"]
inputFile = open(queryFileName,"r")
lines=inputFile.readlines()
lines = [line.rstrip("\n").split("\t") for line in lines]
# lines.pop(0) #assumes header, removes it
inputFile.close()

initialize_run = Job(submit_dir+'/initialize.submit', name='initialize')
initialize_run.add_var('run_folder', '.')
initialize_run.add_var('exec',scripts_dir + '/get_genes_initialize.sh')
initialize_run.add_var('param1',queryFileName)

myDag.add_job(initialize_run)


for line in lines:
    gene=line[0]

    get_genes_job = Job(pipeline_dir + '/submit_dir/get_genes.submit', name = "get_" + gene)
    get_genes_job.add_var('run_folder', cwd + '/gene_trees/' + gene )
    get_genes_job.add_var('exec',pipeline_dir + '/scripts_dir/get_genes.sh')
    get_genes_job.add_var('base','get_genes_')
    get_genes_job.add_var('param1',cwd)
    get_genes_job.add_var('param2',gene)
    get_genes_job.add_parent(initialize_run)
    myDag.add_job(get_genes_job)
    

myDag.save('get_genes.dag')
