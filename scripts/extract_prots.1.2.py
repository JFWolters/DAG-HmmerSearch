#V1.2 update
#removed sequence renaming to preserve compatbility with naming in CDS file

import sys

from Bio import SeqIO

inTable=sys.argv[1]
inProts = sys.argv[2]
species=sys.argv[3]
inFile = open(inTable,"r")

lines = inFile.readlines()

inFile.close()

lines = [line.split("\t") for line in lines]

gene_names = [line[1] for line in lines]

records = SeqIO.parse(inProts,"fasta")

outFileName = species + ".protein_hits.fasta"

outRecords = []

for record in records:
    if record.id in gene_names:
        # record.id = species+ "_x_" +record.id
        outRecords.append(record)
        
SeqIO.write(outRecords,outFileName,"fasta")
