#Given a set of protein sequences, extracts the matching sequence from a cds by matching the id
#note that this script is heavily customized for specific details of the 332 paper genome annotations
#run as follows
#python3 /path/to/extract_CDS.2.py 

#V2 update
#simplified name check, now assumes prots and cds are named consistently

#import necessary packages
from Bio import SeqIO #in/out sequence reading from Biopython
import sys #for reading input and minor operations
from os import path #for modifying file paths

#read in the command line arguments
proteinFileName = sys.argv[1]
cdsFileName = sys.argv[2]

proteins = SeqIO.parse(proteinFileName,"fasta") #read in protein sequences as SeqRecords

cds = list(SeqIO.parse(cdsFileName,"fasta")) #read in cds as SeqRecords, store as list for reuse

out_records = [] #initialize empty list to store cds matches

for protein in proteins:
    foundMatch=False #track whether a match was found for this protein
    
    for seq in cds:
        #compare sequence id's to check for matching
        if protein.id in seq.id: #compare record.id attributes to check for match (id is first space delimited field in seq header)
            foundMatch = True #record that a match was found
            out_records.append(seq) #add the matching sequence to the ouput list
            continue #skip to the next protein (assumes multiple matches are impossible, which should be the case)
    if not foundMatch:
        print("No matching record for", protein.id)

#generate the output file name
#the output file is generated in the folder in which the script is run

outFileName = path.basename(proteinFileName) #strip the file path
outFileName = path.splitext(outFileName)[0] #strip the file extension (useful since fasta file extensions are idiosyncratic)
#modify the file name to better reflect its contents
outFileName = outFileName.rstrip("protein_hits")
#add "CDS" and file extension
outFileName = outFileName + "CDS.fasta"

#write the CDS output
SeqIO.write(out_records,outFileName,"fasta")
            