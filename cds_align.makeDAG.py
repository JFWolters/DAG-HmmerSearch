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

scripts_dir=varDict["scripts_dir"]
submit_dir=varDict["submit_dir"]


queryFileName=varDict["queryFileName"]
inputFile = open(queryFileName,"r")
lines=inputFile.readlines()
lines = [line.rstrip("\n").split("\t") for line in lines]

# lines.pop(0) #assumes header, removes it
inputFile.close()



for line in lines:
    gene=line[0]
    #run alignment
    run_alignment_job = Job(submit_dir+'/align.submit', name = "align_cds_" + gene)
    run_alignment_job.add_var('run_folder', cwd + '/gene_trees/' + gene )
    run_alignment_job.add_var('exec',scripts_dir+'/align_cds.2.sh')
    run_alignment_job.add_var('base','run_alignment_')
    run_alignment_job.add_var('param1',gene)
    run_alignment_job.add_var('param2',cwd)   
    myDag.add_job(run_alignment_job)
    

myDag.save('align_cds.dag')
