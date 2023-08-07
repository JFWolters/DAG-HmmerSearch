from pydagman.dagfile import Dagfile
from pydagman.job import Job
import os
import sys

myDag = Dagfile()

cwd = os.getcwd()

vars=open("vars.config","r")
vars_lines = vars.readlines()
vars.close()
vars_lines = [ line for line in vars_lines if not line.startswith("#") ] #remove comment lines
vars_lines = [ line for line in vars_lines if line != "\n"] #remove blank lines
vars = [line.split(" ")[1].rstrip("\n") for line in vars_lines]
vars = [line.split("=") for line in vars]
varDict = {}


for var in vars:
    varDict[var[0]]=var[1]

scripts_dir=varDict["scripts_dir"]
submit_dir=varDict["submit_dir"]

subjectFileName=varDict["subjectFileName"]
inputFile = open(subjectFileName,"r")
lines=inputFile.readlines()
inputFile.close()
lines=[line.rstrip('\n') for line in lines]
lines=[line.split('\t') for line in lines]

queryFileName=varDict["queryFileName"]
queryFile=open(queryFileName,"r")
queryLines=queryFile.readlines()
queryFile.close()
queryLines=[line.rstrip('\n') for line in queryLines]
queryLines=[line.split('\t') for line in queryLines]

initialize_run = Job(pipeline_dir + '/submit_dir/generalized_submit.pass2.submit', name='initialize')
initialize_run.add_var('run_folder', '.')
initialize_run.add_var('exec',pipeline_dir + '/scripts_dir/initialize.sh')
initialize_run.add_var('param1',subjectFileName)
initialize_run.add_var('param2',queryFileName)
initialize_run.add_var('base',"initialize")

myDag.add_job(initialize_run)

make_profile_job = Job(pipeline_dir + '/submit_dir/generalized_submit.pass2.submit', name='make_hmmer_db')
make_profile_job.add_var('run_folder', '.')
make_profile_job.add_var('exec',pipeline_dir + '/scripts_dir/make_hmmer_db.sh')
make_profile_job.add_var('param1',cwd)
make_profile_job.add_var('param2',queryFileName)
make_profile_job.add_var('base',"make_hmmer_db")

myDag.add_job(make_profile_job)

for queryLine in queryLines:
    gene=queryLine[0]
    geneFileName=queryLine[1]
    score_cutoff=queryLine[2]
    for line in lines:
        species = line[0]
        prots=line[1]
        cds=line[2]
        prot_search_job = Job(submit_dir + '/prot_search.submit', name = "annot_prot_search_" + gene + "_" + species)
        prot_search_job.add_var('run_folder', cwd + '/isr/' + gene + "/" + species )
        prot_search_job.add_var('exec',scripts_dir + '/run_me.sh')
        prot_search_job.add_var('param1',species)
        prot_search_job.add_var('param2',gene)
        prot_search_job.add_var('param3',prots)
        prot_search_job.add_var('param4',cds)
        prot_search_job.add_var('param5',score_cutoff)
        prot_search_job.add_var('param6',cwd)
        prot_search_job.add_parent(initialize_run)
        prot_search_job.add_parent(make_profile_job)
        myDag.add_job(prot_search_job)
    
myDag.save('annot_prot_search.dag')
