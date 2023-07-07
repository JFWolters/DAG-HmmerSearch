###V.2 notes
#Same as V.1
#except as input, all sequences are in one file instead of separate files
#so the input is the sequence file, not a file listing the file names to be analyzed 

import sys
from Bio import SeqIO

records = list(SeqIO.parse(sys.argv[1],"fasta"))

sizes = []

names = []

for record in records:

    name = record.id
    
    seq_length = len(record.seq)
    
    sizes.append(seq_length)
    
    names.append(name)
    
outputFileName = "Sequence_sizes.tab"

out = open(outputFileName,"w")

out.write("Sequence\tSize\n")

for i in range(len(names)):

    outString = names[i] + "\t" + str(sizes[i]) + "\n"
    
    out.write(outString)
    
out.close()
