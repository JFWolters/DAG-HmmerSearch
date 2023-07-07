#filter the resulting hits based on score

from Bio import SeqIO
from os import path
from sys import argv


protFileName=argv[1]
cdsFileName=argv[2]
scoreFileName=argv[3]
scoreCutoff=float(argv[4])

prots = SeqIO.parse(protFileName,"fasta")

cds = SeqIO.parse(cdsFileName,"fasta")

scoreFile = open(scoreFileName,"r")

scoreLines = scoreFile.readlines()

scoreFile.close()

scoreLines = [ line.rstrip("\n").split("\t") for line in scoreLines]

hits_to_keep = []

for line in scoreLines:
    contig = line[1]
    
    score=float(line[3])
    
    if score > scoreCutoff:
        hits_to_keep.append(contig)
        
outProts=[]
for record in prots:
    for contig in hits_to_keep:
        if record.id == contig:
            outProts.append(record)

outCDS=[]
for record in cds:
    for contig in hits_to_keep:
        if record.id == contig:
            outCDS.append(record)
            
outProtFileName = path.splitext(path.basename(protFileName))[0] + ".filtered.fasta"

outCDSFileName = path.splitext(path.basename(cdsFileName))[0] + ".filtered.fasta"

SeqIO.write(outProts,outProtFileName,"fasta")

SeqIO.write(outCDS,outCDSFileName,"fasta")

