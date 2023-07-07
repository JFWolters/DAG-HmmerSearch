#translates all sequences in a fasta file using the provided translation table

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import sys

inSeqFile = sys.argv[1]
table = int(sys.argv[2])

outFileName = inSeqFile.replace("fasta","translated.fasta")

records = SeqIO.parse(inSeqFile,"fasta")

out = []

for record in records:
    
    translated_record = record
    translated_record.seq = translated_record.seq.translate(table=table)
    
    out.append(translated_record)
    
SeqIO.write(out,outFileName,"fasta")