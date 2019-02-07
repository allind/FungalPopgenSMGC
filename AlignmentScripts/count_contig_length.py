#! /usr/bin/env python
#Author: Abigail Lind
from Bio import SeqIO
import sys
def main(argv):

	fasta = SeqIO.parse(sys.argv[1], 'fasta')
	for seq in fasta:
		print seq.description.split(' ')[0] + '\t' + str(len(str(seq.seq)))
if __name__ == "__main__":
    main(sys.argv)
