from Bio import SeqIO

from sys import argv

from os import path

seqFileName=argv[1]

species=argv[2]

out_records = []

outFileName = path.splitext(path.basename(seqFileName))[0] + ".species_id.fasta"

records = SeqIO.parse(seqFileName,"fasta")

for record in records:
    record.id = species + "_" + record.id
    out_records.append(record)
    
SeqIO.write(out_records,outFileName,"fasta")
