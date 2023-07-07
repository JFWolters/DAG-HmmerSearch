import sys
from os import path

inFileName = sys.argv[1]
species=sys.argv[2]
inFile = open(inFileName,"r")
outFileName = path.splitext(path.basename(inFileName))[0] + ".fixed.tab"
lines = inFile.readlines()

inFile.close()

lines = [ line for line in lines if not line.startswith("#")]

lines = [line.split(" ") for line in lines]
fixed_lines = []

for line in lines:
    line[:] = [x for x in line if x != '']
    fixed_lines.append(line)
outFile = open(outFileName,"w")
for line in fixed_lines:
    # print(line)
    # sys.exit(0)
    
    prot=line[0]
    evalue=line[4]
    score=line[5]
    outFile.write(species+"\t"+prot+"\t"+evalue+"\t"+score+"\n")
    
outFile.close()

# augustus_masked-NODE_52_length_101915_cov_36.2178_ID_103-processed-gene-0.38-mRNA-1_1
# -
# Nu_sequences_xyl.translated.aligned
# -
# 5.2e-167 evalue
# 553.4 score
# 0.0  5.8e-167  553.2   0.0   1.0   1   0   0   1   1   1   1 gene=augustus_masked-NODE_52_length_101915_cov_36.2178_ID_103-processed-gene-0.38 CDS=1-957
