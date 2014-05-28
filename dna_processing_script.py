#

#input: files with dna sequences (fasta or genbank)
#operations list:
# GC-content for each file
# DNA to RNA translation
# RNA to aminoacids translation
# multiple alignment for resulting sequences (using BLOSUM62)
#save resulting multiple alignment to PHYLIP file
from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio.Seq import transcribe
from Bio.Seq import translate

res = [ x for x in SeqIO.parse(open("test_dataset/gene3.gb", "rU"), "genbank")] + [x for x in SeqIO.parse(open("test_dataset/gene1.fasta", "rU"), "fasta")] + [x for x in SeqIO.parse(open("test_dataset/gene2.fasta", "rU"), "fasta")]

from Bio.Align.Applications import MuscleCommandline

for x in res:
  print GC(x.seq)
  print transcribe(x.seq)
  print translate(x)
  x.seq = translate(x.seq)

records = [x for x in res]

muscle_cline = MuscleCommandline(clw=True)
import subprocess
import sys
child = subprocess.Popen(str(muscle_cline) + " -matrix BLOSUM62",
stdin=subprocess.PIPE,
stdout=subprocess.PIPE,
stderr=subprocess.PIPE,
shell=(sys.platform!="win32"))


SeqIO.write(records, child.stdin, "fasta")
child.stdin.close()


from Bio import AlignIO
align = AlignIO.read(child.stdout, "clustal")
print(align)
AlignIO.write(align, "my_example.phy", "phylip-relaxed")
